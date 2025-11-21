import os
import pandas as pd
import requests # Usaremos 'requests' para chamar a API local do Ollama
import json
import time
import random
from pathlib import Path
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
# A biblioteca do Google NÃO é mais necessária aqui

MODEL_NAME = os.environ.get("LLMUSIC_MODEL", "llama3:8b")
N_ITERACOES = int(os.environ.get("LLMUSIC_ITERACOES", 10))
TRECHOS_POR_LOTE = int(os.environ.get("LLMUSIC_TRECHOS_LOTE", 5))
TEMAS_POR_LOTE = int(os.environ.get("LLMUSIC_TEMAS_POR_LOTE", 3))
EMBEDDING_DEVICE = os.environ.get("LLMUSIC_EMBEDDING_DEVICE", "cuda")

print("--- Iniciando o pipeline LLMusic (Versão Local com Ollama) ---")
print(
    f"Configuração: modelo={MODEL_NAME}, iteracoes={N_ITERACOES}, "
    f"lote={TRECHOS_POR_LOTE}, temas_por_lote={TEMAS_POR_LOTE}, "
    f"device_embedding={EMBEDDING_DEVICE}"
)

# --- 1. Carregar os Dados ---
data_path = Path(__file__).resolve().parent.parent / "pre_processamento" / "musicas_por_trechos_limpo_20251116_112423.csv"
print(f"Lendo dados de: {data_path}")
try:
    df = pd.read_csv(data_path)
    trechos = df['letra'].dropna().astype(str).tolist()
    print(f"Carregados {len(trechos)} trechos únicos.")
except FileNotFoundError:
    print(f"Erro: Arquivo não encontrado em '{data_path}'.")
    exit()

# --- 2. Etapa 1: Geração de Temas (com LLM Local) ---
print("\n--- ETAPA 1: Gerando temas com o LLM (Ollama) ---")
print("Isso vai usar o processamento do seu computador...")

lista_de_temas_gerados = []
url_ollama = "http://localhost:11434/api/generate" # API local do Ollama

for i in range(N_ITERACOES):
    print(f"\nIniciando Iteração {i + 1}/{N_ITERACOES}...")
    random.shuffle(trechos)
    lotes = [trechos[j:j + TRECHOS_POR_LOTE] for j in range(0, len(trechos), TRECHOS_POR_LOTE)]
    print(f"Processando {len(lotes)} lotes...")

    for count, lote in enumerate(lotes):
        trechos_formatados = "\n".join([f"{idx+1}. {trecho}" for idx, trecho in enumerate(lote)])
        
        prompt = (
            f"dado os seguintes trechos de música, "
            f"sugira {TEMAS_POR_LOTE} tópicos que descrevem os assuntos abordados:\n\n"
            f"{trechos_formatados}\n\n"
            f"REGRAS:\n"
            f"- Responda APENAS com os tópicos, um por linha.\n"
            f"- Não inclua números na sua resposta.\n"
            f"- Gere temas curtos e conceituais (ex: 'Sofrimento por amor', 'Festa e bebida')."
        )
        
        # Estrutura de dados que o Ollama espera
        data = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7
            }
        }
        
        try:
            # Envia a requisição para a sua máquina local
            response = requests.post(url_ollama, json=data)
            if response.status_code != 200:
                print(f"  Erro HTTP {response.status_code} no lote {count + 1}: {response.text[:200]}")
                continue

            response_json = response.json()
            if "error" in response_json:
                print(f"  Lote {count + 1} retornou erro do Ollama: {response_json['error']}")
                continue

            raw_response = response_json.get('response', '')
            if not raw_response or not raw_response.strip():
                print(f"  Lote {count + 1} não retornou tópicos. Verifique o modelo no Ollama.")
                continue

            temas = [tema.strip() for tema in raw_response.strip().split('\n') if tema.strip()]
            if not temas:
                print(f"  Lote {count + 1} retornou somente linhas vazias.")
                continue

            lista_de_temas_gerados.extend(temas)
            print(f"    Temas do lote {count + 1}: {temas}")
            
            if (count + 1) % 50 == 0:
                print(f"  ...lote {count + 1}/{len(lotes)} processado.")

        except requests.exceptions.ConnectionError:
            print("ERRO DE CONEXÃO: O Ollama não está rodando. Inicie o Ollama e tente novamente.")
            exit()
        except Exception as e:
            print(f"  Erro inesperado no lote {count + 1}: {e}. Pulando.")
            time.sleep(1)

print(f"\n--- Geração de Temas Concluída ---")
print(f"Total de temas gerados: {len(lista_de_temas_gerados)}")

pd.DataFrame(lista_de_temas_gerados, columns=["tema"]).to_csv("temas_gerados_llmusic_local.csv", index=False)

# --- 3. Etapa 2: Agrupamento de Temas (BERTopic) ---
print("\n--- ETAPA 2: Agrupando temas com BERTopic ---")

print("Carregando modelo de embedding...")
embedding_model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2",
    device=EMBEDDING_DEVICE
)

print("Instanciando o modelo BERTopic...")
topic_model_llmusic = BERTopic(
    embedding_model=embedding_model,
    language="multilingual",
    verbose=True
)

print("Iniciando o treinamento do modelo nos temas gerados...")
topics, probabilities = topic_model_llmusic.fit_transform(lista_de_temas_gerados)

# --- 4. Visualizar os Resultados ---
print("\n--- TÓPICOS ENCONTRADOS (Pipeline LLMusic - Local) ---")
topic_info_llmusic = topic_model_llmusic.get_topic_info()
print(topic_info_llmusic)

topic_info_llmusic.to_csv("resultados_llmusic_pipeline_local.csv", index=False)

print("\n--- Script Concluído ---")
