# ================================================================================
# REPROCESSAR ARQUIVO MASSIVO PARA ADICIONAR ANOS
# Atualiza o arquivo CSV massivo existente com informações de ano
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
        print(f"❌ Erro ao acessar {url}: {str(e)}")
        return None

def extrair_ano_melhorado(soup):
    """Extrai o ano da música usando estratégias melhoradas."""
    try:
        # 1. Procurar em JSON-LD (Schema.org) - estratégia mais confiável
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
        
        # 2. Procurar em meta tags
        meta_tags = [
            ('property', 'music:release_date'),
            ('property', 'article:published_time'),
            ('name', 'publish_date'),
            ('name', 'release_date'),
            ('itemprop', 'datePublished'),
            ('itemprop', 'releaseDate')
        ]
        
        for attr, valor in meta_tags:
            meta = soup.find('meta', {attr: valor})
            if meta and meta.get('content'):
                ano_match = re.search(r'\b(19|20)\d{2}\b', meta.get('content'))
                if ano_match:
                    return int(ano_match.group())
        
        # 3. Procurar em elementos com microdata
        elementos_microdata = soup.find_all(attrs={'itemprop': re.compile(r'date|year', re.I)})
        for elem in elementos_microdata:
            texto = elem.get_text() or elem.get('content', '') or elem.get('datetime', '')
            ano_match = re.search(r'\b(19|20)\d{2}\b', texto)
            if ano_match:
                return int(ano_match.group())
        
        return None
        
    except Exception:
        return None

def reprocessar_arquivo_massivo():
    """Reprocessa o arquivo massivo para adicionar anos."""
    
    arquivo_original = "letras_sertanejo_massivo_20250930_192052.csv"
    
    print("🔄 REPROCESSAMENTO PARA ADICIONAR ANOS")
    print("=" * 70)
    print(f"📁 Arquivo original: {arquivo_original}")
    
    # Carregar dados existentes
    try:
        df = pd.read_csv(arquivo_original, encoding='utf-8')
        print(f"📊 Carregadas {len(df)} músicas")
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo: {str(e)}")
        return
    
    # Verificar estrutura
    print(f"📋 Colunas: {list(df.columns)}")
    
    # Contar músicas sem ano
    sem_ano = df['ano'].isna().sum()
    com_ano = len(df) - sem_ano
    
    print(f"📅 Músicas com ano: {com_ano}")
    print(f"❓ Músicas sem ano: {sem_ano}")
    
    if sem_ano == 0:
        print("✅ Todas as músicas já têm ano!")
        return
    
    print(f"\n⏳ Processando {sem_ano} músicas sem ano...")
    print("⚠️  ATENÇÃO: Este processo pode demorar bastante!")
    print("⏱️  Estimativa: ~3 segundos por música")
    print(f"⏱️  Tempo estimado total: ~{(sem_ano * 3) // 60} minutos")
    
    resposta = input("\n❓ Continuar? (s/n): ").lower().strip()
    if resposta != 's':
        print("❌ Operação cancelada")
        return
    
    print("\n🚀 Iniciando reprocessamento...")
    
    # Processar músicas sem ano
    sucessos = 0
    falhas = 0
    
    for i, row in df.iterrows():
        if pd.isna(row['ano']) or row['ano'] == '':
            # Tentar extrair ano
            url = row['url']
            titulo = row['titulo']
            artista = row['artista']
            
            print(f"[{i+1}/{len(df)}] 🎵 {artista} - {titulo}")
            
            # Fazer requisição
            soup = fazer_request(url)
            if soup:
                ano = extrair_ano_melhorado(soup)
                if ano:
                    df.at[i, 'ano'] = ano
                    sucessos += 1
                    print(f"   ✅ Ano encontrado: {ano}")
                else:
                    falhas += 1
                    print(f"   ❌ Ano não encontrado")
            else:
                falhas += 1
                print(f"   ❌ Erro ao acessar página")
            
            # Delay para não sobrecarregar o servidor
            time.sleep(random.uniform(2, 4))
            
            # Mostrar progresso a cada 10 músicas
            if (i + 1) % 10 == 0:
                porcentagem = ((i + 1) / len(df)) * 100
                print(f"\n📊 Progresso: {porcentagem:.1f}% - Sucessos: {sucessos}, Falhas: {falhas}")
    
    # Resultados finais
    print("\n" + "=" * 70)
    print("📊 RESULTADOS DO REPROCESSAMENTO:")
    print(f"   ✅ Anos adicionados: {sucessos}")
    print(f"   ❌ Falhas: {falhas}")
    
    # Estatísticas finais
    total_com_ano = df['ano'].notna().sum()
    porcentagem_final = (total_com_ano / len(df)) * 100
    print(f"   📅 Total de músicas com ano: {total_com_ano}/{len(df)} ({porcentagem_final:.1f}%)")
    
    # Salvar arquivo atualizado
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    arquivo_atualizado = f"letras_sertanejo_com_anos_{timestamp}.csv"
    
    try:
        df.to_csv(arquivo_atualizado, index=False, encoding='utf-8')
        print(f"💾 Arquivo salvo: {arquivo_atualizado}")
        
        # Também salvar em JSON
        arquivo_json = arquivo_atualizado.replace('.csv', '.json')
        df.to_json(arquivo_json, orient='records', indent=2, force_ascii=False)
        print(f"💾 Arquivo JSON salvo: {arquivo_json}")
        
    except Exception as e:
        print(f"❌ Erro ao salvar: {str(e)}")
    
    # Distribuição de anos
    if total_com_ano > 0:
        print("\n📊 DISTRIBUIÇÃO DE ANOS:")
        distribuicao = df['ano'].value_counts().sort_index()
        for ano, count in distribuicao.items():
            if pd.notna(ano):
                print(f"   {int(ano)}: {count} músicas")

if __name__ == "__main__":
    reprocessar_arquivo_massivo()