from __future__ import annotations

import argparse
import json
import os
import random
import re
import time
from dataclasses import dataclass
from pathlib import Path
from statistics import StatisticsError, mode
from typing import Iterable, List, Optional

import numpy as np
import pandas as pd
import requests

MODEL_NAME = os.environ.get("LLMUSIC_MODEL", "llama3:8b")
N_INFERENCIAS = int(os.environ.get("LLMUSIC_INFERENCIAS", 5))
TEMPERATURAS = [float(t) for t in os.environ.get("LLMUSIC_TEMPERATURAS", "0.1,0.4,0.7,0.9,1.0").split(",")]
NUM_PREDICT = int(os.environ.get("LLMUSIC_NUM_PREDICT", 5))  # mantém respostas curtas


class DualLogger:
    def __init__(self, path: Path):
        self.path = path
        self._fh = path.open("w", encoding="utf-8")

    def log(self, msg: str) -> None:
        print(msg)
        self._fh.write(msg + "\n")
        self._fh.flush()

    def close(self) -> None:
        try:
            self._fh.close()
        except Exception:
            pass


@dataclass
class Trecho:
    id: str
    texto: str


@dataclass
class Topico:
    id: int | str
    nome: str


def carregar_trechos(path_csv: Path, sample: Optional[int], log: DualLogger) -> List[Trecho]:
    df = pd.read_csv(path_csv)
    col_tag = "tag_trecho" if "tag_trecho" in df.columns else ("tag_musica" if "tag_musica" in df.columns else None)
    if col_tag is None:
        col_tag = "ranking_posicao" if "ranking_posicao" in df.columns else None
    if col_tag is None:
        raise ValueError("Nao foi possivel identificar a coluna de ID (esperado tag_trecho/tag_musica/ranking_posicao).")
    if "letra" not in df.columns:
        raise ValueError("Coluna 'letra' nao encontrada no CSV de trechos.")

    if sample is not None and sample > 0:
        df = df.sample(sample, random_state=42).reset_index(drop=True)

    trechos: List[Trecho] = []
    for _, row in df.iterrows():
        texto = str(row["letra"]).strip()
        if not texto:
            continue
        trechos.append(Trecho(id=str(row[col_tag]), texto=texto))

    log.log(f"Trechos carregados: {len(trechos)} (de {len(df)}) usando coluna '{col_tag}'.")
    return trechos


def carregar_topicos(path_csv: Path, log: DualLogger) -> List[Topico]:
    df = pd.read_csv(path_csv)
    col_id = next((c for c in df.columns if c.strip().lower() == "id"), None)
    col_nome = next(
        (
            c
            for c in df.columns
            if c.strip().lower().replace(" ", "") in {"topicos_temas", "topicos_tema", "tema", "temas"}
        ),
        None,
    )
    if not col_nome:
        # fallback para primeira coluna se nada encontrado
        col_nome = df.columns[0]
    if not col_id:
        # se nao houver id, cria sequencia 1..n
        df = df.reset_index().rename(columns={"index": "id"})
        col_id = "id"

    topicos: List[Topico] = []
    for _, row in df.iterrows():
        nome = str(row[col_nome]).strip()
        if not nome or nome.lower() == "nan":
            continue
        raw_id = row[col_id]
        try:
            topico_id = int(raw_id)
        except (TypeError, ValueError):
            topico_id = str(raw_id).strip()
        topicos.append(Topico(id=topico_id, nome=nome))

    if not topicos:
        raise ValueError("Nenhum topico carregado a partir do CSV informado.")

    log.log(f"Topicos carregados: {len(topicos)} (colunas usadas: id='{col_id}', nome='{col_nome}').")
    return topicos


def montar_prompt(trecho: str, nome_topico: str) -> str:
    return (
        "Avaliacao da Relacao Semantica.\n"
        f"Topico: {nome_topico}\n"
        f"Trecho: \"{trecho}\"\n\n"
        "Classifique a relacao entre o trecho e o topico na escala:\n"
        "1: Nenhuma relacao.\n"
        "2: Relacao fraca.\n"
        "3: Relacao moderada.\n"
        "4: Relacao forte.\n"
        "5: Relacao muito forte.\n\n"
        "Responda EXCLUSIVAMENTE com um unico numero (1, 2, 3, 4 ou 5)."
    )


def consultar_llm(trecho: Trecho, topico: Topico, temperatura: float) -> Optional[int]:
    payload = {
        "model": MODEL_NAME,
        "prompt": montar_prompt(trecho.texto, topico.nome),
        "stream": False,
        "options": {"temperature": temperatura, "num_predict": NUM_PREDICT},
    }
    resp = requests.post("http://localhost:11434/api/generate", json=payload)
    resp.raise_for_status()
    raw = resp.json().get("response", "").strip()
    if not raw:
        return None
    match = re.search(r"[1-5]", raw)
    return int(match.group(0)) if match else None


def consolidar_scores(scores: List[int]) -> tuple[float, int, float, int, str]:
    media = float(np.mean(scores))
    try:
        moda_val = mode(scores)
    except StatisticsError:
        moda_val = int(np.median(scores))
    desvio = float(np.std(scores))
    classificado = 1 if (moda_val >= 4 and desvio <= 1.5) else 0
    if desvio <= 0.5:
        confianca = "alta"
    elif desvio <= 1.0:
        confianca = "media"
    else:
        confianca = "baixa"
    return media, moda_val, desvio, classificado, confianca


def gerar_relatorio(trechos: List[Trecho], topicos: List[Topico], log: DualLogger) -> pd.DataFrame:
    log.log(f"\nIniciando classificacao de {len(trechos)} trechos contra {len(topicos)} topicos...")
    total_chamadas = len(trechos) * len(topicos) * N_INFERENCIAS
    log.log(f"Total estimado de chamadas ao LLM: {total_chamadas}")

    resultados = []
    inicio = time.time()
    for idx_trecho, trecho in enumerate(trechos, start=1):
        log.log(f"\nProcessando trecho {idx_trecho}/{len(trechos)} (id={trecho.id})")
        for topico in topicos:
            scores: List[int] = []
            temps = TEMPERATURAS if TEMPERATURAS else [0.0]
            for k in range(N_INFERENCIAS):
                temp = temps[k % len(temps)]
                try:
                    score = consultar_llm(trecho, topico, temp)
                    if score:
                        scores.append(score)
                    else:
                        log.log(f"  aviso: resposta vazia para topico {topico.id} na inferencia {k+1}")
                except Exception as exc:
                    log.log(f"  falha na chamada (topico {topico.id}, temp {temp}): {exc}")
                time.sleep(0.1)

            if scores:
                media, moda_val, desvio, classificado, confianca = consolidar_scores(scores)
                resultados.append(
                    {
                        "trecho_id": trecho.id,
                        "trecho_texto": (trecho.texto[:50] + "...") if len(trecho.texto) > 53 else trecho.texto,
                        "topico_id": topico.id,
                        "topico_nome": topico.nome,
                        "scores_raw": json.dumps(scores),
                        "n_validos": len(scores),
                        "media_score": round(media, 2),
                        "moda_score": moda_val,
                        "desvio_padrao": round(desvio, 2),
                        "classificado_positivo": classificado,
                        "confianca": confianca,
                    }
                )
            else:
                log.log(f"  -> nenhuma resposta valida para topico {topico.id} ({topico.nome})")

    log.log(f"\nConcluido em {round(time.time() - inicio, 2)} segundos.")
    return pd.DataFrame(resultados)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera relatorio final classificando trechos por topicos com autoconsistencia."
    )
    parser.add_argument("trechos_csv", help="CSV com colunas 'letra' e tag_trecho/tag_musica/ranking_posicao.")
    parser.add_argument("topicos_csv", help="CSV de topicos (ex: Topicos_tema.csv).")
    parser.add_argument(
        "--sample",
        type=int,
        default=None,
        help="Opcional: quantidade de trechos para amostragem aleatoria (padrao: todos).",
    )
    parser.add_argument(
        "--saida",
        type=str,
        default=None,
        help="CSV de saida (padrao: <trechos>_relatorio_final.csv).",
    )
    parser.add_argument(
        "--log",
        type=str,
        default=None,
        help="Arquivo de log (padrao: <trechos>_relatorio_final.log).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    trechos_path = Path(args.trechos_csv)
    topicos_path = Path(args.topicos_csv)
    if not trechos_path.exists():
        raise FileNotFoundError(f"Arquivo de trechos nao encontrado: {trechos_path}")
    if not topicos_path.exists():
        raise FileNotFoundError(f"Arquivo de topicos nao encontrado: {topicos_path}")

    log_path = Path(args.log) if args.log else trechos_path.with_name(f"{trechos_path.stem}_relatorio_final.log")
    logger = DualLogger(log_path)

    logger.log("--- ETAPA 2: Classificacao com Autoconsistencia (LLMusic) ---")
    logger.log(
        f"Configuracao: modelo={MODEL_NAME}, inferencias={N_INFERENCIAS}, temperaturas={TEMPERATURAS}, num_predict={NUM_PREDICT}"
    )
    try:
        trechos = carregar_trechos(trechos_path, args.sample, logger)
        topicos = carregar_topicos(topicos_path, logger)
        df_resultados = gerar_relatorio(trechos, topicos, logger)
        out_path = Path(args.saida) if args.saida else trechos_path.with_name(f"{trechos_path.stem}_relatorio_final.csv")
        df_resultados.to_csv(out_path, index=False)
        logger.log(f"Resultados salvos em: {out_path}")
        logger.log("\nExemplo dos primeiros resultados:")
        logger.log(df_resultados.head().to_string(index=False))
    finally:
        logger.close()


if __name__ == "__main__":
    main()
