import requests
from bs4 import BeautifulSoup
import time

# Teste simples para verificar se conseguimos acessar o site
def testar_acesso():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print("🧪 TESTE DE ACESSO AO LETRAS.MUS.BR")
    print("=" * 50)
    
    # Testar página inicial
    try:
        print("1. Testando acesso à página inicial...")
        response = requests.get("https://www.letras.mus.br", headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Tamanho da resposta: {len(response.text)} caracteres")
        
        if "letras" in response.text.lower():
            print("   ✅ Site acessível!")
        else:
            print("   ⚠️ Resposta inesperada")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Testar busca por um artista famoso
    time.sleep(2)
    
    try:
        print("\n2. Testando busca por 'sertanejo'...")
        search_url = "https://www.letras.mus.br/busca.php?words=sertanejo"
        response = requests.get(search_url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        artist_links = [link for link in links if link.get('href', '').startswith('/') and len(link.get_text().strip()) > 3]
        
        print(f"   Links de artistas encontrados: {len(artist_links)}")
        
        if artist_links:
            print("   Primeiros 5 artistas encontrados:")
            for i, link in enumerate(artist_links[:5]):
                print(f"     - {link.get_text().strip()} -> {link.get('href')}")
        
    except Exception as e:
        print(f"   ❌ Erro na busca: {e}")
    
    # Testar URL direta de um artista conhecido
    time.sleep(2)
    
    try:
        print("\n3. Testando URL direta para 'chitaozinho-e-xororo'...")
        artist_url = "https://www.letras.mus.br/chitaozinho-e-xororo/"
        response = requests.get(artist_url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('h1')
            if title:
                print(f"   Título da página: {title.get_text().strip()}")
            
            # Procurar por lista de músicas
            songs = soup.find_all('a', href=True)
            song_links = [s for s in songs if '/chitaozinho-e-xororo/' in s.get('href', '') and s.get('href') != '/chitaozinho-e-xororo/']
            print(f"   Músicas encontradas: {len(song_links)}")
            
            if song_links:
                print("   Primeiras 3 músicas:")
                for song in song_links[:3]:
                    print(f"     - {song.get_text().strip()}")
        
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print("\n" + "=" * 50)
    print("Teste concluído!")

if __name__ == "__main__":
    testar_acesso()