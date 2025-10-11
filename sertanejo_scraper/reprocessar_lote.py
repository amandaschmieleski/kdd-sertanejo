# ================================================================================
# REPROCESSAR ARQUIVO MASSIVO PARA ADICIONAR ANOS - VERSÃO LOTE
# Atualiza o arquivo CSV massivo com anos, processando em pequenos lotes
# ================================================================================

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import re
import json
from datetime import datetime

def fazer_request(url):
    """Faz uma requisição HTTP e retorna o soup."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        return None

def extrair_ano_melhorado(soup):
    """Extrai o ano da música usando estratégias melhoradas."""
    try:
        # 1. Procurar em JSON-LD (Schema.org)
        scripts_json = soup.find_all('script', type='application/ld+json')
        for script in scripts_json:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    # Procurar datePublished, releaseDate, etc.
                    for campo in ['datePublished', 'releaseDate', 'dateCreated', 'uploadDate']:
                        if campo in data:
                            ano_match = re.search(r'\b(19|20)\d{2}\b', str(data[campo]))
                            if ano_match:
                                return int(ano_match.group())
                    
                    # Se for MusicRecording, procurar em album
                    if data.get('@type') == 'MusicRecording' and 'inAlbum' in data:
                        album = data['inAlbum']
                        if isinstance(album, dict) and 'datePublished' in album:
                            ano_match = re.search(r'\b(19|20)\d{2}\b', str(album['datePublished']))
                            if ano_match:
                                return int(ano_match.group())
                                
            except (json.JSONDecodeError, KeyError):
                continue
        
        return None
        
    except Exception:
        return None

def reprocessar_lote():
    """Reprocessa um pequeno lote de músicas para testar."""
    
    arquivo_original = "letras_sertanejo_massivo_20250930_192052.csv"
    
    print("🔄 REPROCESSAMENTO DE LOTE PARA TESTAR ANOS")
    print("=" * 60)
    
    # Carregar dados
    df = pd.read_csv(arquivo_original, encoding='utf-8')
    print(f"📊 Total de músicas: {len(df)}")
    
    # Processar apenas as primeiras 20 músicas como teste
    lote_size = 20
    print(f"🎯 Processando apenas {lote_size} músicas como teste...")
    
    sucessos = 0
    falhas = 0
    
    for i in range(min(lote_size, len(df))):
        row = df.iloc[i]
        url = row['url']
        titulo = row['titulo']
        artista = row['artista']
        
        print(f"[{i+1}/{lote_size}] 🎵 {artista} - {titulo}")
        
        # Fazer requisição
        soup = fazer_request(url)
        if soup:
            ano = extrair_ano_melhorado(soup)
            if ano:
                df.at[i, 'ano'] = ano
                sucessos += 1
                print(f"   ✅ Ano: {ano}")
            else:
                falhas += 1
                print(f"   ❌ Ano não encontrado")
        else:
            falhas += 1
            print(f"   ❌ Erro na requisição")
        
        # Delay
        time.sleep(random.uniform(2, 3))
    
    # Resultados
    print("\n" + "=" * 60)
    print("📊 RESULTADOS DO TESTE:")
    print(f"   ✅ Anos encontrados: {sucessos}")
    print(f"   ❌ Falhas: {falhas}")
    print(f"   📈 Taxa de sucesso: {(sucessos/lote_size*100):.1f}%")
    
    # Salvar lote teste
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    arquivo_teste = f"teste_lote_anos_{timestamp}.csv"
    
    df_teste = df.head(lote_size).copy()
    df_teste.to_csv(arquivo_teste, index=False, encoding='utf-8')
    print(f"💾 Lote teste salvo: {arquivo_teste}")
    
    # Mostrar distribuição de anos do teste
    if sucessos > 0:
        anos_encontrados = df_teste['ano'].dropna().astype(int).value_counts().sort_index()
        print(f"\n📅 Anos encontrados no teste:")
        for ano, count in anos_encontrados.items():
            print(f"   {ano}: {count} músicas")
    
    # Estimativa para arquivo completo
    if sucessos > 0:
        taxa_sucesso = sucessos / lote_size
        total_estimado = int(len(df) * taxa_sucesso)
        tempo_estimado = (len(df) * 2.5) / 60  # ~2.5 segundos por música
        
        print(f"\n🔮 ESTIMATIVAS PARA ARQUIVO COMPLETO:")
        print(f"   📊 Anos esperados: ~{total_estimado} de {len(df)} músicas")
        print(f"   ⏱️  Tempo estimado: ~{tempo_estimado:.0f} minutos")
        print(f"   💡 Recomendação: {'VALE A PENA' if taxa_sucesso > 0.5 else 'AVALIAR'}")

if __name__ == "__main__":
    reprocessar_lote()