# ================================================================================
# TESTE DE EXTRAÇÃO DE ANO - VERSÃO MELHORADA
# Analisa o JSON-LD e outros metadados para extrair ano
# ================================================================================

import requests
from bs4 import BeautifulSoup
import re
import json

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
    """Extrai o ano da música usando várias estratégias."""
    try:
        print("🔍 Procurando ano na página...")
        
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
                                print(f"   ✅ Ano encontrado em JSON-LD ({campo}): {ano_match.group()}")
                                return int(ano_match.group())
                    
                    # Se for MusicRecording, procurar em album
                    if data.get('@type') == 'MusicRecording' and 'inAlbum' in data:
                        album = data['inAlbum']
                        if isinstance(album, dict) and 'datePublished' in album:
                            ano_match = re.search(r'\b(19|20)\d{2}\b', str(album['datePublished']))
                            if ano_match:
                                print(f"   ✅ Ano encontrado em álbum: {ano_match.group()}")
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
                    print(f"   ✅ Ano encontrado em meta {attr}='{valor}': {ano_match.group()}")
                    return int(ano_match.group())
        
        # 3. Procurar em elementos específicos com microdata
        elementos_microdata = soup.find_all(attrs={'itemprop': re.compile(r'date|year', re.I)})
        for elem in elementos_microdata:
            texto = elem.get_text() or elem.get('content', '') or elem.get('datetime', '')
            ano_match = re.search(r'\b(19|20)\d{2}\b', texto)
            if ano_match:
                print(f"   ✅ Ano encontrado em microdata: {ano_match.group()}")
                return int(ano_match.group())
        
        # 4. Procurar em classes específicas do site
        seletores_especificos = [
            '.song-year',
            '.release-year', 
            '.album-year',
            '.song-info .year',
            '.song-header .year',
            '.cnt-head_subtitle',
            '.song-date'
        ]
        
        for seletor in seletores_especificos:
            elemento = soup.select_one(seletor)
            if elemento:
                texto = elemento.get_text()
                ano_match = re.search(r'\b(19|20)\d{2}\b', texto)
                if ano_match:
                    print(f"   ✅ Ano encontrado em {seletor}: {ano_match.group()}")
                    return int(ano_match.group())
        
        print("   ❌ Ano não encontrado em nenhuma fonte estruturada")
        return None
        
    except Exception as e:
        print(f"❌ Erro ao extrair ano: {str(e)}")
        return None

def analisar_json_ld(soup):
    """Analisa todos os dados JSON-LD da página."""
    print("📋 Analisando dados estruturados JSON-LD:")
    scripts_json = soup.find_all('script', type='application/ld+json')
    
    for i, script in enumerate(scripts_json):
        try:
            data = json.loads(script.string)
            print(f"\n   Script {i+1}:")
            print(f"   Tipo: {data.get('@type', 'Não especificado')}")
            
            # Mostrar campos relevantes
            campos_relevantes = ['name', 'datePublished', 'releaseDate', 'dateCreated', 'uploadDate', 'inAlbum']
            for campo in campos_relevantes:
                if campo in data:
                    print(f"   {campo}: {str(data[campo])[:100]}...")
                    
        except json.JSONDecodeError:
            print(f"   Script {i+1}: Erro ao decodificar JSON")

def testar_multiplas_musicas():
    """Testa a extração de ano em várias músicas."""
    
    urls_teste = [
        "https://www.letras.mus.br/henrique-e-juliano/ai-que-saudade-de-voce/",
        "https://www.letras.mus.br/marilia-mendonca/infiel/",
        "https://www.letras.mus.br/gusttavo-lima/balada/",
        "https://www.letras.mus.br/almir-sater/tocando-em-frente/"
    ]
    
    print("🎵 Testando extração de ano em múltiplas músicas")
    print("=" * 70)
    
    for url in urls_teste:
        print(f"\n🔗 URL: {url}")
        
        soup = fazer_request(url)
        if not soup:
            print("❌ Não foi possível acessar a página")
            continue
        
        # Extrair informações básicas
        titulo_elem = soup.find('h1', class_='head_title')
        titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Título não encontrado"
        
        artista_elem = soup.find('h2', class_='head_subtitle')  
        artista = artista_elem.get_text(strip=True) if artista_elem else "Artista não encontrado"
        
        print(f"🎤 {artista} - {titulo}")
        
        # Tentar extrair ano
        ano = extrair_ano_melhorado(soup)
        if ano:
            print(f"📅 Ano: {ano}")
        else:
            print("❌ Ano não encontrado")
            # Analisar JSON-LD para debug
            analisar_json_ld(soup)

if __name__ == "__main__":
    testar_multiplas_musicas()