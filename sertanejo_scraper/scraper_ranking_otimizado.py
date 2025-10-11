# ================================================================================
# SCRAPER OTIMIZADO PARA MAIS ACESSADAS SERTANEJO
# Baseado na estrutura real da página mostrada na imagem
# ================================================================================

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
import json
from datetime import datetime
from urllib.parse import urljoin

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

def extrair_musicas_ranking():
    """Extrai as músicas do ranking de mais acessadas."""
    
    url = "https://www.letras.mus.br/mais-acessadas/sertanejo/"
    
    print("🎵 EXTRAINDO MÚSICAS DO RANKING SERTANEJO")
    print("=" * 60)
    print(f"🔗 URL: {url}")
    
    soup = fazer_request(url)
    if not soup:
        return []
    
    musicas_encontradas = []
    
    # A página tem uma estrutura específica que precisamos mapear
    # Vamos procurar por diferentes padrões comuns em rankings
    
    estrategias = [
        # Estratégia 1: Procurar por elementos de ranking com números
        {
            'nome': 'Elementos de ranking numerados',
            'seletor': '[class*="rank"], [class*="position"], [class*="number"]',
        },
        # Estratégia 2: Links com estrutura de música
        {
            'nome': 'Links para páginas de música',
            'seletor': 'a[href*="/"]',
        },
        # Estratégia 3: Elementos que contêm nomes de artistas conhecidos
        {
            'nome': 'Elementos com artistas',
            'seletor': '*',
        }
    ]
    
    print(f"\n🔍 Analisando estrutura da página...")
    
    # Vamos procurar por texto que contenha os artistas que vimos na imagem
    artistas_conhecidos = [
        "Henrique & Juliano", "Henrique e Juliano",
        "Chitãozinho & Xororó", "Chitaozinho e Xororo", 
        "Felipe Araújo", "Luan Pereira",
        "Diego e Victor Hugo", "Simone Mendes",
        "Clayton e Romário", "Gustavo Mioto",
        "Luan Santana", "Jorge & Mateus"
    ]
    
    # Procurar por elementos que contenham esses artistas
    for artista in artistas_conhecidos:
        # Procurar variações do nome
        variacao1 = artista.replace("&", "e")
        variacao2 = artista.replace("e", "&")
        
        for nome in [artista, variacao1, variacao2]:
            elementos = soup.find_all(text=re.compile(nome, re.IGNORECASE))
            if elementos:
                print(f"   ✅ Encontrado: {nome} ({len(elementos)} ocorrências)")
                
                # Para cada ocorrência, tentar extrair contexto
                for elem in elementos[:2]:  # Limitar para não spammar
                    parent = elem.parent
                    if parent:
                        # Procurar link relacionado
                        link = parent.find('a') or parent.find_parent('a')
                        if link and link.get('href'):
                            href = link.get('href')
                            if not any(skip in href for skip in ['javascript', '#', 'mailto']):
                                url_completa = urljoin(url, href)
                                
                                # Tentar extrair título da música
                                titulo_elem = parent
                                texto_completo = titulo_elem.get_text(strip=True)
                                
                                # Separar artista e música
                                if ' - ' in texto_completo:
                                    partes = texto_completo.split(' - ', 1)
                                    titulo = partes[0].strip()
                                    artista_extraido = partes[1].strip() if len(partes) > 1 else nome
                                elif any(a.lower() in texto_completo.lower() for a in [nome]):
                                    # O texto contém o artista, usar como base
                                    titulo = texto_completo.replace(nome, '').strip()
                                    artista_extraido = nome
                                else:
                                    titulo = texto_completo
                                    artista_extraido = nome
                                
                                musica_info = {
                                    'titulo': titulo,
                                    'artista': artista_extraido,
                                    'url': url_completa,
                                    'texto_original': texto_completo,
                                    'posicao': len(musicas_encontradas) + 1
                                }
                                
                                # Evitar duplicatas
                                if not any(m['url'] == url_completa for m in musicas_encontradas):
                                    musicas_encontradas.append(musica_info)
                                    print(f"      → {titulo} - {artista_extraido}")
    
    # Se não encontrou muitas músicas, tentar abordagem mais geral
    if len(musicas_encontradas) < 20:
        print(f"\n🔍 Tentando abordagem mais ampla...")
        
        # Procurar todos os links que podem ser músicas
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href')
            texto = link.get_text(strip=True)
            
            # Filtrar links que parecem ser de músicas
            if (href and len(texto) > 10 and 
                not any(skip in href for skip in ['javascript', '#', 'mailto', 'facebook', 'instagram', 'twitter']) and
                not any(skip in texto.lower() for skip in ['entrar', 'cadastro', 'sobre', 'contato', 'política'])):
                
                url_completa = urljoin(url, href)
                
                # Se o texto contém hífen, pode ser "Música - Artista"
                if ' - ' in texto:
                    partes = texto.split(' - ', 1)
                    titulo = partes[0].strip()
                    artista = partes[1].strip()
                else:
                    titulo = texto
                    artista = "A definir"
                
                musica_info = {
                    'titulo': titulo,
                    'artista': artista,
                    'url': url_completa,
                    'texto_original': texto,
                    'posicao': len(musicas_encontradas) + 1
                }
                
                # Evitar duplicatas e URLs muito curtas
                if (not any(m['url'] == url_completa for m in musicas_encontradas) and 
                    len(href.split('/')) >= 3):
                    musicas_encontradas.append(musica_info)
                    
                    if len(musicas_encontradas) >= 50:  # Limitar para teste
                        break
    
    print(f"\n📊 RESULTADO:")
    print(f"   Total encontrado: {len(musicas_encontradas)} músicas")
    
    return musicas_encontradas

def salvar_ranking_musicas(musicas):
    """Salva o ranking de músicas em arquivo."""
    
    if not musicas:
        print("❌ Nenhuma música para salvar")
        return None
    
    # Criar DataFrame
    df = pd.DataFrame(musicas)
    
    # Ordenar por posição
    df = df.sort_values('posicao').reset_index(drop=True)
    
    # Salvar
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    arquivo = f"ranking_sertanejo_mais_acessadas_{timestamp}.csv"
    df.to_csv(arquivo, index=False, encoding='utf-8')
    
    print(f"💾 Ranking salvo em: {arquivo}")
    
    # Mostrar top 10
    print(f"\n🏆 TOP 10 MÚSICAS MAIS ACESSADAS:")
    for i, row in df.head(10).iterrows():
        print(f"   {row['posicao']:2}. {row['artista']} - {row['titulo']}")
    
    # Estatísticas
    if len(df) > 0:
        top_artistas = df['artista'].value_counts().head()
        print(f"\n🎤 ARTISTAS COM MAIS MÚSICAS NO RANKING:")
        for artista, count in top_artistas.items():
            if artista != "A definir":
                print(f"   {artista}: {count} músicas")
    
    return arquivo

if __name__ == "__main__":
    print("🚀 Iniciando extração do ranking de mais acessadas...")
    
    # Extrair músicas
    musicas = extrair_musicas_ranking()
    
    # Salvar resultados
    if musicas:
        arquivo = salvar_ranking_musicas(musicas)
        print(f"\n✅ Extração concluída!")
        print(f"   📁 Arquivo: {arquivo}")
        print(f"   📊 Total: {len(musicas)} músicas")
    else:
        print("❌ Nenhuma música extraída")