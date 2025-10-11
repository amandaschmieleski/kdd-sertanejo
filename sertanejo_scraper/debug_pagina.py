# ================================================================================
# DEBUG - ANÁLISE DE PÁGINA
# Salva conteúdo HTML para entender estrutura
# ================================================================================

import requests
from bs4 import BeautifulSoup

def analisar_pagina():
    """Analisa uma página específica para entender a estrutura."""
    
    url = "https://www.letras.mus.br/henrique-e-juliano/amor-dos-outros/"
    
    print(f"🔍 Analisando: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print(f"✅ Status: {response.status_code}")
        print(f"📏 Tamanho: {len(response.content)} bytes")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Salvar HTML
        with open('debug_pagina.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print(f"💾 HTML salvo em: debug_pagina.html")
        
        # Procurar title da página
        title_tag = soup.find('title')
        if title_tag:
            print(f"📋 Title: {title_tag.get_text()}")
        
        # Procurar h1
        h1_tags = soup.find_all('h1')
        print(f"📋 H1 tags encontradas: {len(h1_tags)}")
        for i, h1 in enumerate(h1_tags[:3]):
            print(f"   H1 {i+1}: {h1.get_text()[:100]}...")
        
        # Procurar elementos com classes relacionadas a música
        classes_musica = [
            'head_title', 'head-title', 'song-title', 'title',
            'head_subtitle', 'head-subtitle', 'artist', 'artist-name',
            'lyric-original', 'lyric', 'letra'
        ]
        
        for classe in classes_musica:
            elementos = soup.find_all(attrs={'class': classe})
            if elementos:
                print(f"📋 Classe '{classe}': {len(elementos)} elementos")
                for elem in elementos[:2]:
                    texto = elem.get_text(strip=True)
                    if texto:
                        print(f"   → {texto[:50]}...")
        
        # Verificar se é uma página de erro ou redirecionamento
        if "404" in response.text or "not found" in response.text.lower():
            print("⚠️ Possível página 404")
        
        if "redirect" in response.text.lower():
            print("⚠️ Possível redirecionamento")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    analisar_pagina()