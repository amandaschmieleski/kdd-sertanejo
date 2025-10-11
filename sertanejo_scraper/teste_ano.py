# ================================================================================
# TESTE DE EXTRAÇÃO DE ANO
# Testa se conseguimos extrair o ano das músicas do Letras.mus.br
# ================================================================================

import requests
from bs4 import BeautifulSoup
import re

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

def extrair_ano(soup):
    """Extrai o ano da música se disponível."""
    try:
        print("🔍 Procurando ano na página...")
        
        # Procurar ano em diferentes lugares
        elementos_ano = [
            soup.find('span', class_='year'),
            soup.find('time'),
            soup.find('div', class_='song-info'),
            soup.find('div', class_='song_header'),
            soup.find('div', class_='cnt-head_subtitle'),
            soup.find('p', class_='subtitle')
        ]
        
        for i, elemento in enumerate(elementos_ano):
            if elemento:
                texto = elemento.get_text()
                print(f"   Elemento {i+1}: {texto[:100]}...")
                # Procurar padrão de 4 dígitos (ano)
                match_ano = re.search(r'\b(19|20)\d{2}\b', texto)
                if match_ano:
                    print(f"   ✅ Ano encontrado: {match_ano.group()}")
                    return int(match_ano.group())
        
        # Procurar em qualquer lugar da página
        print("   Procurando em toda a página...")
        texto_completo = soup.get_text()
        anos = re.findall(r'\b(19|20)\d{2}\b', texto_completo)
        if anos:
            print(f"   Anos encontrados na página: {list(set(anos))}")
        
        return None
        
    except Exception as e:
        print(f"❌ Erro ao extrair ano: {str(e)}")
        return None

def testar_extracao_ano():
    """Testa a extração de ano em uma música específica."""
    
    # Testar com uma música conhecida
    url_teste = "https://www.letras.mus.br/henrique-e-juliano/ai-que-saudade-de-voce/"
    
    print(f"🎵 Testando extração de ano em: {url_teste}")
    print("=" * 70)
    
    soup = fazer_request(url_teste)
    if not soup:
        print("❌ Não foi possível acessar a página")
        return
    
    # Extrair informações básicas
    titulo_elem = soup.find('h1', class_='head_title')
    titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Título não encontrado"
    
    artista_elem = soup.find('h2', class_='head_subtitle')
    artista = artista_elem.get_text(strip=True) if artista_elem else "Artista não encontrado"
    
    print(f"🎤 Artista: {artista}")
    print(f"🎵 Música: {titulo}")
    print()
    
    # Tentar extrair ano
    ano = extrair_ano(soup)
    
    if ano:
        print(f"📅 Ano extraído: {ano}")
    else:
        print("❌ Ano não encontrado")
    
    print("\n" + "=" * 70)
    print("🔍 Vamos analisar o HTML da página para encontrar onde pode estar o ano...")
    
    # Procurar por elementos que podem conter data
    elementos_potenciais = [
        ('meta[property="music:release_date"]', 'content'),
        ('meta[name="publish_date"]', 'content'),
        ('script[type="application/ld+json"]', 'text'),
        ('.song-info', 'text'),
        ('.album-info', 'text'),
        ('.release-date', 'text'),
        ('[data-year]', 'data-year'),
    ]
    
    for seletor, atributo in elementos_potenciais:
        elementos = soup.select(seletor)
        if elementos:
            for elem in elementos:
                if atributo == 'text':
                    conteudo = elem.get_text()[:200]
                else:
                    conteudo = elem.get(atributo, '')
                if conteudo:
                    print(f"   {seletor}: {conteudo}")
                    # Procurar anos no conteúdo
                    anos = re.findall(r'\b(19|20)\d{2}\b', str(conteudo))
                    if anos:
                        print(f"      → Anos encontrados: {anos}")

if __name__ == "__main__":
    testar_extracao_ano()