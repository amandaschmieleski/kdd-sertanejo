# ================================================================================
# PROCESSAMENTO INTELIGENTE DE ANOS - VERSÃO ROBUSTA
# Processa em pequenos lotes e salva progresso incremental
# ================================================================================

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import re
import json
from datetime import datetime
import os

def fazer_request(url):
    """Faz uma requisição HTTP e retorna o soup."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception:
        return None

def extrair_ano_melhorado(soup):
    """Extrai o ano da música usando JSON-LD."""
    try:
        scripts_json = soup.find_all('script', type='application/ld+json')
        for script in scripts_json:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    # Procurar campos de data
                    for campo in ['datePublished', 'releaseDate', 'dateCreated', 'uploadDate']:
                        if campo in data:
                            ano_match = re.search(r'\b(19|20)\d{2}\b', str(data[campo]))
                            if ano_match:
                                return int(ano_match.group())
                    
                    # Procurar em álbum
                    if data.get('@type') == 'MusicRecording' and 'inAlbum' in data:
                        album = data['inAlbum']
                        if isinstance(album, dict) and 'datePublished' in album:
                            ano_match = re.search(r'\b(19|20)\d{2}\b', str(album['datePublished']))
                            if ano_match:
                                return int(ano_match.group())
            except:
                continue
        return None
    except:
        return None

def processar_em_lotes():
    """Processa o arquivo em lotes pequenos, salvando progresso."""
    
    arquivo_original = "letras_sertanejo_massivo_20250930_192052.csv"
    
    print("🚀 PROCESSAMENTO INTELIGENTE DE ANOS")
    print("=" * 60)
    
    # Carregar dados
    df = pd.read_csv(arquivo_original, encoding='utf-8')
    total_musicas = len(df)
    
    print(f"📊 Total de músicas: {total_musicas}")
    
    # Verificar se já existe progresso
    arquivo_progresso = "progresso_anos.csv"
    inicio = 0
    
    if os.path.exists(arquivo_progresso):
        df_progresso = pd.read_csv(arquivo_progresso, encoding='utf-8')
        # Copiar anos já processados
        for i, row in df_progresso.iterrows():
            if pd.notna(row['ano']) and row['ano'] != '':
                df.at[i, 'ano'] = row['ano']
        
        # Encontrar próximo índice a processar
        inicio = len(df_progresso)
        print(f"📈 Retomando do índice {inicio}")
    
    # Configurações de lote
    tamanho_lote = 50  # Lotes menores para salvar progresso mais frequente
    delay_min, delay_max = 1.5, 3.0  # Delay mais rápido
    
    sucessos = 0
    falhas = 0
    
    print(f"⏳ Processando de {inicio} até {total_musicas}")
    print(f"📦 Tamanho do lote: {tamanho_lote} músicas")
    
    for i in range(inicio, total_musicas):
        row = df.iloc[i]
        
        # Pular se já tem ano
        if pd.notna(row['ano']) and row['ano'] != '':
            continue
            
        url = row['url']
        titulo = row['titulo'][:50] + "..." if len(row['titulo']) > 50 else row['titulo']
        artista = row['artista']
        
        print(f"[{i+1}/{total_musicas}] 🎵 {artista} - {titulo}")
        
        # Fazer requisição
        soup = fazer_request(url)
        if soup:
            ano = extrair_ano_melhorado(soup)
            if ano:
                df.at[i, 'ano'] = ano
                sucessos += 1
                print(f"   ✅ {ano}")
            else:
                falhas += 1
                print(f"   ❌ Sem ano")
        else:
            falhas += 1
            print(f"   ❌ Erro")
        
        # Delay
        time.sleep(random.uniform(delay_min, delay_max))
        
        # Salvar progresso a cada lote
        if (i + 1) % tamanho_lote == 0:
            df.to_csv(arquivo_progresso, index=False, encoding='utf-8')
            porcentagem = ((i + 1) / total_musicas) * 100
            taxa_sucesso = (sucessos / (sucessos + falhas)) * 100 if (sucessos + falhas) > 0 else 0
            
            print(f"\n💾 Progresso salvo! {porcentagem:.1f}% concluído")
            print(f"📊 Sucessos: {sucessos}, Falhas: {falhas} (Taxa: {taxa_sucesso:.1f}%)")
            print(f"⏱️  ETA: ~{((total_musicas - i - 1) * 2.2) / 60:.1f} minutos\n")
    
    # Salvar resultado final
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    arquivo_final = f"letras_sertanejo_com_anos_{timestamp}.csv"
    
    df.to_csv(arquivo_final, index=False, encoding='utf-8')
    
    # Estatísticas finais
    total_com_ano = df['ano'].notna().sum()
    porcentagem_final = (total_com_ano / total_musicas) * 100
    
    print("\n" + "=" * 60)
    print("🎯 PROCESSAMENTO CONCLUÍDO!")
    print(f"✅ Anos adicionados: {sucessos}")
    print(f"❌ Falhas: {falhas}")
    print(f"📅 Total com ano: {total_com_ano}/{total_musicas} ({porcentagem_final:.1f}%)")
    print(f"💾 Arquivo final: {arquivo_final}")
    
    # Distribuição de anos
    if total_com_ano > 0:
        print(f"\n📊 DISTRIBUIÇÃO DE ANOS:")
        distribuicao = df['ano'].value_counts().sort_index()
        for ano, count in distribuicao.head(10).items():
            if pd.notna(ano):
                print(f"   {int(ano)}: {count} músicas")
        if len(distribuicao) > 10:
            print(f"   ... e mais {len(distribuicao) - 10} anos")
    
    # Cleanup
    if os.path.exists(arquivo_progresso):
        os.remove(arquivo_progresso)
        print(f"🧹 Arquivo de progresso removido")

if __name__ == "__main__":
    try:
        processar_em_lotes()
    except KeyboardInterrupt:
        print("\n⚠️  Processamento interrompido pelo usuário")
        print("💾 Progresso foi salvo em progresso_anos.csv")
        print("🔄 Execute novamente para continuar de onde parou")