# ================================================================================
# SCRAPER DE MÚSICAS MAIS ACESSADAS - SERTANEJO
# Coleta as músicas mais populares do sertanejo do Letras.mus.br
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

def analisar_pagina_mais_acessadas():
    """Analisa a estrutura da página de mais acessadas."""
    
    url = "https://www.letras.mus.br/mais-acessadas/sertanejo/"
    
    print("🔍 ANALISANDO PÁGINA DE MAIS ACESSADAS")
    print("=" * 60)
    print(f"🔗 URL: {url}")
    
    soup = fazer_request(url)
    if not soup:
        print("❌ Não foi possível acessar a página")
        return None
    
    print("✅ Página carregada com sucesso")
    
    # Procurar diferentes seletores para as músicas
    seletores_possiveis = [
        'a[href*="/letras/"]',  # Links para letras
        '.song-item',
        '.track-item', 
        '.song-link',
        'li a[href*="/"]',
        '.lista-musicas a',
        '.song-list a'
    ]
    
    print(f"\n🔍 Procurando músicas na página...")
    
    for seletor in seletores_possiveis:
        elementos = soup.select(seletor)
        if elementos:
            print(f"   ✅ Seletor '{seletor}': {len(elementos)} elementos encontrados")
            
            # Mostrar alguns exemplos
            for i, elem in enumerate(elementos[:5]):
                href = elem.get('href', '')
                texto = elem.get_text(strip=True)
                if href and len(texto) > 5:  # Filtrar links vazios
                    print(f"      {i+1}. {texto[:50]}... → {href[:50]}...")
        else:
            print(f"   ❌ Seletor '{seletor}': Nenhum elemento")
    
    # Verificar se há paginação
    print(f"\n🔍 Procurando paginação...")
    paginacao = soup.find_all('a', href=re.compile(r'page|pagina|\d+'))
    if paginacao:
        print(f"   ✅ Paginação encontrada: {len(paginacao)} links")
        for link in paginacao[:3]:
            print(f"      → {link.get('href', '')} ({link.get_text(strip=True)})")
    else:
        print(f"   ❌ Paginação não encontrada")
    
    # Salvar HTML para análise manual
    with open('pagina_mais_acessadas.html', 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    print(f"\n💾 HTML salvo em: pagina_mais_acessadas.html")
    
    return soup

def extrair_musicas_mais_acessadas(soup, limite=100):
    """Extrai lista de músicas da página de mais acessadas."""
    
    print(f"\n🎵 EXTRAINDO MÚSICAS MAIS ACESSADAS")
    print("-" * 50)
    
    musicas_encontradas = []
    
    # Tentar diferentes estratégias de extração
    estrategias = [
        # Estratégia 1: Links diretos para letras
        {
            'nome': 'Links diretos para letras',
            'seletor': 'a[href*="/letras/"]',
            'filtro': lambda href: '/letras/' in href and len(href.split('/')) >= 4
        },
        # Estratégia 2: Links de artistas que podem ter músicas
        {
            'nome': 'Links de artistas com músicas',
            'seletor': 'a[href]',
            'filtro': lambda href: '/' in href and not any(x in href for x in ['page', 'pagina', 'javascript', '#'])
        }
    ]
    
    for estrategia in estrategias:
        print(f"\n🔍 Tentando: {estrategia['nome']}")
        
        elementos = soup.select(estrategia['seletor'])
        musicas_estrategia = []
        
        for elem in elementos:
            href = elem.get('href', '')
            texto = elem.get_text(strip=True)
            
            # Aplicar filtro da estratégia
            if estrategia['filtro'](href) and len(texto) > 3:
                # Tentar extrair artista e música do texto ou URL
                url_completa = urljoin("https://www.letras.mus.br", href)
                
                musica_info = {
                    'texto_original': texto,
                    'url': url_completa,
                    'href': href
                }
                
                # Tentar extrair artista e música
                if ' - ' in texto:
                    partes = texto.split(' - ', 1)
                    musica_info['artista'] = partes[0].strip()
                    musica_info['titulo'] = partes[1].strip()
                else:
                    # Tentar extrair da URL
                    url_parts = href.strip('/').split('/')
                    if len(url_parts) >= 2:
                        musica_info['artista'] = url_parts[-2].replace('-', ' ').title()
                        musica_info['titulo'] = url_parts[-1].replace('-', ' ').title()
                    else:
                        musica_info['artista'] = 'Desconhecido'
                        musica_info['titulo'] = texto
                
                musicas_estrategia.append(musica_info)
                
                if len(musicas_estrategia) >= limite:
                    break
        
        print(f"   ✅ Encontradas: {len(musicas_estrategia)} músicas")
        
        # Mostrar exemplos
        for i, musica in enumerate(musicas_estrategia[:3]):
            print(f"      {i+1}. {musica['artista']} - {musica['titulo']}")
        
        if musicas_estrategia:
            musicas_encontradas = musicas_estrategia
            break
    
    print(f"\n📊 RESULTADO FINAL:")
    print(f"   Total encontrado: {len(musicas_encontradas)} músicas")
    
    return musicas_encontradas

def testar_scraper_mais_acessadas():
    """Testa o scraper na página de mais acessadas."""
    
    print("🚀 TESTANDO SCRAPER DE MAIS ACESSADAS")
    print("=" * 70)
    
    # Analisar página
    soup = analisar_pagina_mais_acessadas()
    if not soup:
        return
    
    # Extrair músicas
    musicas = extrair_musicas_mais_acessadas(soup, limite=50)
    
    if musicas:
        # Salvar em CSV
        df = pd.DataFrame(musicas)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        arquivo = f"musicas_mais_acessadas_{timestamp}.csv"
        df.to_csv(arquivo, index=False, encoding='utf-8')
        
        print(f"💾 Músicas salvas em: {arquivo}")
        
        # Estatísticas
        print(f"\n📊 ESTATÍSTICAS:")
        if 'artista' in df.columns:
            top_artistas = df['artista'].value_counts().head()
            print(f"   Top artistas:")
            for artista, count in top_artistas.items():
                print(f"      {artista}: {count} músicas")
    
    return musicas

if __name__ == "__main__":
    testar_scraper_mais_acessadas()