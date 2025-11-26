from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pandas as pd
import requests

MODEL_NAME = os.environ.get("LLMUSIC_MODEL", "llama3:8b")
TEMAS_POR_REGISTRO = int(os.environ.get("LLMUSIC_TEMAS_POR_REGISTRO", os.environ.get("LLMUSIC_TEMAS_POR_GRUPO", 1)))
N_ITERACOES = int(os.environ.get("LLMUSIC_ITERACOES", 3))
EMBEDDING_DEVICE = os.environ.get("LLMUSIC_EMBEDDING_DEVICE", "cpu")


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
    idx: int
    tag: str
    letra: str
    titulo: Optional[str] = None
    artista: Optional[str] = None
    ano: Optional[str] = None


@dataclass
class TemaSelecionado:
    iteracao: int
    idx: int
    tema: str
    score: float
    tags: str
    topico_id: Optional[int] = None
    tag_trecho: Optional[str] = None
    letra: Optional[str] = None
    titulo: Optional[str] = None
    artista: Optional[str] = None
    ano: Optional[str] = None


def ler_registros(path_csv: Path, log: DualLogger) -> List[Trecho]:
    df = pd.read_csv(path_csv)
    col_tag = "tag_trecho" if "tag_trecho" in df.columns else ("tag_musica" if "tag_musica" in df.columns else None)
    if col_tag is None:
        raise ValueError("Coluna de tag nao encontrada (esperado 'tag_trecho' ou 'tag_musica').")
    if "letra" not in df.columns:
        raise ValueError("Coluna 'letra' nao encontrada no CSV de trechos.")

    registros: List[Trecho] = []
    for idx, linha in df.iterrows():
        tag = str(linha[col_tag]).strip()
        letra = str(linha["letra"]).strip()
        if not letra:
            continue
        registros.append(
            Trecho(
                idx=idx + 1,
                tag=tag,
                letra=letra,
                titulo=str(linha.get("titulo", "")).strip() or None,
                artista=str(linha.get("artista", "")).strip() or None,
                ano=str(linha.get("ano", "")).strip() or None,
            )
        )

    log.log(f"Carregados {len(registros)} registros para classificacao.")
    return registros


def ler_temas_candidatos(path_csv: Path, log: DualLogger) -> tuple[List[str], dict[str, int | str]]:
    df = pd.read_csv(path_csv)
    col_temas = [c for c in df.columns if c.startswith("tema_")]
    col_id = next((c for c in df.columns if c.strip().lower() == "id"), None)

    if not col_temas:
        # Suporta formato Topicos_tema.csv (coluna unica com os temas)
        col_temas = [
            c
            for c in df.columns
            if c.strip().lower().replace(" ", "") in {"topicos_temas", "topicos_tema", "tema", "temas"}
        ]

    if not col_temas and df.shape[1] == 1:
        col_temas = [df.columns[0]]

    if not col_temas:
        raise ValueError("Nenhuma coluna de temas encontrada (esperado 'tema_*' ou similar a 'Topicos_tema').")

    log.log(f"Colunas de temas identificadas: {col_temas}")
    temas_set = set()
    tema_para_id: dict[str, int | str] = {}
    for _, linha in df.iterrows():
        for c in col_temas:
            valor = str(linha.get(c, "")).strip().strip('"')
            if valor and valor.lower() != "nan":
                temas_set.add(valor)
                if col_id:
                    raw_id = linha.get(col_id)
                    if pd.notna(raw_id) and valor not in tema_para_id:
                        try:
                            tema_para_id[valor] = int(raw_id)
                        except (TypeError, ValueError):
                            tema_para_id[valor] = str(raw_id).strip()

    temas = sorted(temas_set)
    log.log(f"Carregados {len(temas)} temas candidatos (globais).")
    return temas, tema_para_id


def montar_prompt_classificacao(temas: List[str], trecho: Trecho) -> str:
    temas_txt = "\n".join([f"- {t}" for t in temas])
    prompt = (
        "Você receberá TEMAS candidatos e um único TRECHO de música (Português do Brasil).\n"
        "Marque quais temas fazem sentido para esse trecho. Pode ser nenhum, um ou vários.\n"
        "Regras:\n"
        "- Use APENAS temas fornecidos. É proibido inventar novos temas.\n"
        "- Não repita temas na resposta.\n"
        "- Retorne SOMENTE JSON com este formato: [\"<tema fornecido>\", ...].\n"
        "- Se nenhum tema se aplica, retorne [].\n"
        "- Não adicione nenhum texto fora do JSON.\n\n"
        f"TEMAS CANDIDATOS:\n{temas_txt}\n\n"
        f"TRECHO:\n[{trecho.tag}] {trecho.letra}\n"
    )
    return prompt


def classificar_temas_para_trecho(trecho: Trecho, temas: List[str]) -> set[str]:
    prompt = montar_prompt_classificacao(temas, trecho)
    data = {"model": MODEL_NAME, "prompt": prompt, "stream": False, "options": {"temperature": 0.0}}
    resp = requests.post("http://localhost:11434/api/generate", json=data)
    resp.raise_for_status()
    raw = resp.json().get("response", "").strip()
    if not raw:
        raise ValueError("Resposta vazia do Ollama.")
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Falha ao decodificar JSON: {raw[:200]}") from exc

    if isinstance(parsed, dict):
        parsed = [parsed]
    if not isinstance(parsed, list):
        raise ValueError(f"Formato inesperado na resposta: {parsed}")

    selecionados: set[str] = set()
    for item in parsed:
        if isinstance(item, dict):
            tema = str(item.get("theme", "")).strip()
        else:
            tema = str(item).strip()

        if not tema:
            continue
        if tema not in temas:
            raise ValueError(f"Tema '{tema}' nao esta na lista de temas permitidos.")
        selecionados.add(tema)

    return selecionados


def processar(trechos_csv: Path, temas_csv: Path, log_path: Path | None = None) -> pd.DataFrame:
    log_path = log_path or trechos_csv.with_name(f"{trechos_csv.stem}_processar_temas.log")
    logger = DualLogger(log_path)
    logger.log("=== Processar Temas com Base em Lista (Versao 2.0) ===")
    logger.log(
        f"Configuracao: modelo={MODEL_NAME}, iteracoes={N_ITERACOES}, device={EMBEDDING_DEVICE}"
    )
    logger.log(f"Trechos: {trechos_csv}")
    logger.log(f"Temas base: {temas_csv}")

    registros = ler_registros(trechos_csv, logger)
    temas_global, tema_para_id = ler_temas_candidatos(temas_csv, logger)

    selecionados: List[TemaSelecionado] = []
    total_registros = len(registros)
    inicio = time.time()
    try:
        for iteracao in range(1, N_ITERACOES + 1):
            logger.log(f"\n=== ITERACAO {iteracao}/{N_ITERACOES} ===")
            for idx, trecho in enumerate(registros, start=1):
                ts = datetime.now().isoformat(timespec="milliseconds")
                largura = len(str(total_registros))
                logger.log(
                    f"{ts} | Registro [{idx:0{largura}d}/{total_registros}] | tag={trecho.tag} | temas_candidatos={len(temas_global)}"
                )
                try:
                    temas_aplicaveis = classificar_temas_para_trecho(trecho, temas_global)
                    linhas_local = []
                    for tema in temas_global:
                        linhas_local.append(
                            {
                                "tag_trecho": trecho.tag,
                                "letra": trecho.letra,
                                "topico_id": tema_para_id.get(tema),
                                "topicos_temas": tema,
                                "classificado_positivo": 1 if tema in temas_aplicaveis else 0,
                            }
                        )
                    selecionados.extend(linhas_local)
                    logger.log(f"    Temas marcados como positivos: {sorted(list(temas_aplicaveis))}")
                except Exception as exc:
                    logger.log(f"    !! Falha no registro {trecho.tag}: {exc}")

        if not selecionados:
            raise RuntimeError("Nenhum tema selecionado.")

        df_local = pd.DataFrame(
            selecionados, columns=["tag_trecho", "letra", "topico_id", "topicos_temas", "classificado_positivo"]
        )
        out_path = trechos_csv.with_name(f"{trechos_csv.stem}_temas_classificados.csv")
        df_local.to_csv(out_path, index=False)
        logger.log(f"Arquivo salvo: {out_path.name}")
    finally:
        logger.log(f"\n--- Script Concluido ---")
        logger.log(f"Tempo total: {(time.time() - inicio)/60:.1f} minutos")
        logger.log(f"Log salvo em: {log_path}")
        logger.close()

    return df_local


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classifica cada registro (ex: rodar_llmusic_parteii.csv) usando apenas temas fornecidos."
    )
    parser.add_argument("trechos_csv", help="CSV com colunas tag_trecho/tag_musica e letra (ex: rodar_llmusic_parteii.csv).")
    parser.add_argument(
        "temas_csv",
        help="CSV de temas base (saida normalizada do script 05 ou arquivo simples como Topicos_tema.csv).",
    )
    parser.add_argument("--log", help="Caminho opcional para o log (padrao: <trechos>_processar_temas.log).")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    processar(Path(args.trechos_csv), Path(args.temas_csv), Path(args.log) if args.log else None)


if __name__ == "__main__":
    main()