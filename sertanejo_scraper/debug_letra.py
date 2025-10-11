import requests
from bs4 import BeautifulSoup
import time

# Debug de uma música específica
def debug_letra():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # URL de uma música conhecida
    url_musica = "https://www.letras.mus.br/chitaozinho-e-xororo/evidencias/"
    
    print("🔍 DEBUG DA EXTRAÇÃO DE LETRA")
    print("=" * 50)
    print(f"URL: {url_musica}")
    
    try:
        response = requests.get(url_musica, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Título
        titulo = soup.find('h1')
        print(f"Título: {titulo.get_text().strip() if titulo else 'Não encontrado'}")
        
        # Procurar por diferentes seletores de letra
        seletores = [
            'div[class*="lyric"]',
            'div[class*="letra"]', 
            'div.cnt-lyric',
            'pre.lyric',
            '.lyric-original',
            'div.lyric-cnt',
            'div.letter',
            'div.song-text'
        ]
        
        print("\nTestando seletores:")
        for seletor in seletores:
            elemento = soup.select_one(seletor)
            if elemento:
                texto = elemento.get_text()[:100]  # Primeiros 100 chars
                print(f"✅ {seletor}: {len(elemento.get_text())} chars - '{texto}...'")
            else:
                print(f"❌ {seletor}: não encontrado")
        
        # Ver todas as divs que podem conter letra
        print("\nDivs que podem conter letras:")
        divs = soup.find_all('div')
        for i, div in enumerate(divs):
            if div.get_text().strip() and len(div.get_text()) > 50:
                classes = div.get('class', [])
                text_preview = div.get_text()[:50].replace('\n', ' ')
                print(f"Div {i}: classes={classes} - '{text_preview}...'")
                if i > 10:  # Limitar saída
                    break
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    debug_letra()