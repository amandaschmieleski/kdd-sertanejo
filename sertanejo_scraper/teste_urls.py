# ================================================================================
# TESTE DE URLs PARA AJUSTAR ALGORITMO
# Testa URLs conhecidas para entender o padrão correto
# ================================================================================

import requests
from bs4 import BeautifulSoup
import re
import unidecode

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
        print(f"❌ Erro: {str(e)}")
        return None

def testar_urls_conhecidas():
    """Testa URLs que sabemos que funcionam."""
    
    urls_conhecidas = [
        ("Evidências", "Chitãozinho & Xororó", "https://www.letras.mus.br/chitaozinho-e-xororo/768469/"),
        ("Infiel", "Marília Mendonça", "https://www.letras.mus.br/marilia-mendonca/infiel/"),
        ("Amor Dos Outros", "Henrique & Juliano", "https://www.letras.mus.br/henrique-e-juliano/amor-dos-outros/"),
        ("Seja Ex", "Henrique & Juliano", "https://www.letras.mus.br/henrique-e-juliano/seja-ex/"),
        ("Balada", "Gusttavo Lima", "https://www.letras.mus.br/gusttavo-lima/balada/"),
    ]
    
    print("🔍 TESTANDO URLs CONHECIDAS")
    print("=" * 50)
    
    for titulo, artista, url in urls_conhecidas:
        print(f"\n🎵 {artista} - {titulo}")
        print(f"🔗 URL: {url}")
        
        soup = fazer_request(url)
        if soup:
            title_elem = soup.find('h1', class_='head_title')
            artist_elem = soup.find('h2', class_='head_subtitle')
            
            if title_elem and artist_elem:
                titulo_real = title_elem.get_text(strip=True)
                artista_real = artist_elem.get_text(strip=True)
                print(f"   ✅ Encontrado: {artista_real} - {titulo_real}")
                
                # Analisar padrão da URL
                partes_url = url.replace('https://www.letras.mus.br/', '').replace('/', '').split('/')
                if len(partes_url) >= 2:
                    artista_url = partes_url[0]
                    musica_url = partes_url[1] if len(partes_url) > 1 else ""
                    print(f"   📋 Artista URL: {artista_url}")
                    print(f"   📋 Música URL: {musica_url}")
            else:
                print(f"   ❌ Elementos não encontrados")
        else:
            print(f"   ❌ Falha na requisição")

def construir_url_melhorada(titulo, artista):
    """Versão melhorada do construtor de URL."""
    
    def normalizar_nome(texto):
        # Remover partes entre parênteses
        texto = re.sub(r'\s*\([^)]*\)\s*', '', texto)
        # Remover acentos
        texto = unidecode.unidecode(texto) if texto else ""
        # Converter para minúsculas
        texto = texto.lower()
        # Tratar casos especiais
        texto = texto.replace('&', 'e')
        texto = texto.replace(' e ', '-e-')
        # Remover caracteres especiais, manter apenas letras, números, espaços e hífens
        texto = re.sub(r'[^a-z0-9\s\-]', '', texto)
        # Trocar espaços por hífens
        texto = re.sub(r'\s+', '-', texto)
        # Remover hífens duplos
        texto = re.sub(r'-+', '-', texto)
        # Remover hífens no início/fim
        texto = texto.strip('-')
        return texto
    
    artista_url = normalizar_nome(artista)
    titulo_url = normalizar_nome(titulo)
    
    url = f"https://www.letras.mus.br/{artista_url}/{titulo_url}/"
    
    return url

def testar_construtor_melhorado():
    """Testa o construtor melhorado com exemplos conhecidos."""
    
    testes = [
        ("Evidências", "Chitãozinho & Xororó"),
        ("Amor Dos Outros", "Henrique & Juliano"),
        ("Seja Ex", "Henrique & Juliano"),
        ("Infiel", "Marília Mendonça"),
        ("OLHO MARROM", "Luan Santana"),
        ("Body Splash (part. Luan Pereira)", "Felipe Araújo"),
    ]
    
    print("\n🛠️ TESTANDO CONSTRUTOR MELHORADO")
    print("=" * 50)
    
    sucessos = 0
    for titulo, artista in testes:
        url = construir_url_melhorada(titulo, artista)
        print(f"\n🎵 {artista} - {titulo}")
        print(f"🔗 URL gerada: {url}")
        
        soup = fazer_request(url)
        if soup:
            title_elem = soup.find('h1', class_='head_title')
            if title_elem:
                titulo_encontrado = title_elem.get_text(strip=True)
                print(f"   ✅ Encontrado: {titulo_encontrado}")
                sucessos += 1
            else:
                print(f"   ❌ Página existe mas sem título")
        else:
            print(f"   ❌ URL não encontrada")
    
    print(f"\n📊 Resultado: {sucessos}/{len(testes)} sucessos ({sucessos/len(testes)*100:.1f}%)")

if __name__ == "__main__":
    print("🚀 Testando estratégias de URLs...")
    
    # Testar URLs conhecidas
    testar_urls_conhecidas()
    
    # Testar construtor melhorado
    testar_construtor_melhorado()