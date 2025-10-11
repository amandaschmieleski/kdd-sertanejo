# ================================================================================
# SCRAPER CORRIGIDO COM SELETORES ATUALIZADOS
# Baseado na análise da estrutura real das páginas
# ================================================================================

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
import json
from datetime import datetime
from urllib.parse import urljoin, quote
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
        return None

def extrair_ano_melhorado(soup):
    """Extrai o ano da música usando JSON-LD."""
    try:
        scripts_json = soup.find_all('script', type='application/ld+json')
        for script in scripts_json:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    for campo in ['datePublished', 'releaseDate', 'dateCreated', 'uploadDate']:
                        if campo in data:
                            ano_match = re.search(r'\b(19|20)\d{2}\b', str(data[campo]))
                            if ano_match:
                                return int(ano_match.group())
                    
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

def limpar_letra(letra_bruta):
    """Limpa e formata o texto da letra."""
    if not letra_bruta:
        return ""
    
    # Separar palavras grudadas usando regex
    texto_limpo = re.sub(r'([a-záéíóúçãõâêôà])([A-ZÁÉÍÓÚÇÃÕÂÊÔÀ])', r'\1 \2', letra_bruta)
    
    # Limpar espaços extras e quebras de linha
    linhas = [linha.strip() for linha in texto_limpo.split('\n') if linha.strip()]
    
    return '\n'.join(linhas)

def extrair_letra_completa_corrigida(url_musica, titulo_original, artista_original, ranking_pos):
    """Extrai letra completa usando seletores atualizados."""
    
    print(f"[{ranking_pos:3}] 🎵 {artista_original} - {titulo_original}")
    
    soup = fazer_request(url_musica)
    if not soup:
        print(f"      ❌ Erro ao acessar URL")
        return None
    
    try:
        # Novos seletores baseados na análise
        # Título: h1 dentro de textStyle-primary
        titulo_elem = soup.find('h1', class_='textStyle-primary')
        if not titulo_elem:
            # Fallback para outros seletores
            titulo_elem = soup.find('h1')
        
        if not titulo_elem:
            print(f"      ❌ Título não encontrado")
            return None
        
        titulo = titulo_elem.get_text(strip=True)
        
        # Artista: link para artista (geralmente próximo ao título)
        artista_elem = titulo_elem.find_next('a')
        if artista_elem and '/henrique-e-juliano/' in artista_elem.get('href', ''):
            artista = artista_elem.get_text(strip=True)
        else:
            # Fallback para artista original
            artista = artista_original
        
        # Letra: procurar diferentes classes
        seletores_letra = [
            '.lyric-original',
            '[class*="lyric"]',
            'div.lyric',
            '.letra'
        ]
        
        letra_elem = None
        for seletor in seletores_letra:
            letra_elem = soup.select_one(seletor)
            if letra_elem and len(letra_elem.get_text().strip()) > 100:
                break
        
        if not letra_elem:
            print(f"      ❌ Letra não encontrada")
            return None
        
        letra_bruta = letra_elem.get_text()
        letra_limpa = limpar_letra(letra_bruta)
        
        if len(letra_limpa.split()) < 10:
            print(f"      ⚠️ Letra muito curta")
            return None
        
        # Extrair ano
        ano = extrair_ano_melhorado(soup)
        
        dados_musica = {
            'ranking_posicao': ranking_pos,
            'titulo': titulo,
            'artista': artista,
            'titulo_original': titulo_original,
            'artista_original': artista_original,
            'letra': letra_limpa,
            'url': url_musica,
            'ano': ano,
            'coletado_em': datetime.now().isoformat(),
            'contagem_palavras': len(letra_limpa.split()),
            'contagem_linhas': len(letra_limpa.split('\n')),
            'fonte': 'ranking_mais_acessadas_corrigido'
        }
        
        ano_str = f", ano: {ano}" if ano else ""
        print(f"      ✅ Sucesso! ({dados_musica['contagem_palavras']} palavras{ano_str})")
        return dados_musica
        
    except Exception as e:
        print(f"      ❌ Erro: {str(e)}")
        return None

def normalizar_nome_url(texto):
    """Normaliza nome para URL do Letras.mus.br."""
    # Remover partes entre parênteses
    texto = re.sub(r'\s*\([^)]*\)\s*', '', texto)
    # Remover acentos
    texto = unidecode.unidecode(texto) if texto else ""
    # Converter para minúsculas
    texto = texto.lower()
    # Casos especiais
    texto = texto.replace('&', 'e')
    # Remover caracteres especiais
    texto = re.sub(r'[^a-z0-9\s]', '', texto)
    # Trocar espaços por hífens
    texto = re.sub(r'\s+', '-', texto)
    # Limpar hífens
    texto = re.sub(r'-+', '-', texto).strip('-')
    return texto

def construir_url_musica(titulo, artista):
    """Constrói URL da música."""
    artista_url = normalizar_nome_url(artista)
    titulo_url = normalizar_nome_url(titulo)
    return f"https://www.letras.mus.br/{artista_url}/{titulo_url}/"

def coletar_hits_corrigido():
    """Coleta hits usando seletores corrigidos."""
    
    print(f"🚀 COLETA DE HITS - VERSÃO CORRIGIDA")
    print("=" * 70)
    
    # Lista teste pequena primeiro
    musicas_teste = [
        (1, "Amor Dos Outros", "Henrique & Juliano"),
        (2, "Evidências", "Chitãozinho & Xororó"),
        (3, "Infiel", "Marília Mendonça"),
        (4, "Seja Ex", "Henrique & Juliano"),
        (5, "OLHO MARROM", "Luan Santana"),
        (6, "Balada", "Gusttavo Lima"),
        (7, "Boate Azul", "Bruno & Marrone"),
        (8, "Tocando Em Frente", "Almir Sater"),
        (9, "Cuida Bem Dela", "Henrique & Juliano"),
        (10, "Retrovisor", "Gusttavo Lima"),
    ]
    
    print(f"🎵 Testando com {len(musicas_teste)} músicas...")
    
    musicas_coletadas = []
    sucessos = 0
    falhas = 0
    
    for posicao, titulo, artista in musicas_teste:
        url = construir_url_musica(titulo, artista)
        
        dados = extrair_letra_completa_corrigida(url, titulo, artista, posicao)
        
        if dados:
            musicas_coletadas.append(dados)
            sucessos += 1
        else:
            falhas += 1
        
        # Delay
        time.sleep(random.uniform(2, 4))
    
    print(f"\n" + "=" * 70)
    print(f"📊 RESULTADO DO TESTE:")
    print(f"   ✅ Sucessos: {sucessos}")
    print(f"   ❌ Falhas: {falhas}")
    print(f"   📈 Taxa de sucesso: {(sucessos/(sucessos+falhas)*100):.1f}%")
    
    if musicas_coletadas:
        # Salvar dados
        df = pd.DataFrame(musicas_coletadas)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        arquivo = f"teste_hits_corrigido_{timestamp}.csv"
        df.to_csv(arquivo, index=False, encoding='utf-8')
        
        print(f"💾 Dados salvos em: {arquivo}")
        
        # Análises
        total_palavras = df['contagem_palavras'].sum()
        musicas_com_ano = df[df['ano'].notna()]
        
        print(f"\n📊 ANÁLISE:")
        print(f"   Total de palavras: {total_palavras:,}")
        print(f"   Média por música: {df['contagem_palavras'].mean():.0f} palavras")
        print(f"   Músicas com ano: {len(musicas_com_ano)}")
        
        if len(musicas_com_ano) > 0:
            anos = musicas_com_ano['ano'].value_counts().sort_index()
            print(f"   Anos encontrados: {list(anos.index)}")
    
    return musicas_coletadas

if __name__ == "__main__":
    print("🚀 Testando scraper corrigido...")
    
    musicas = coletar_hits_corrigido()
    
    print(f"\n✅ TESTE CONCLUÍDO!")
    print(f"   📊 Total coletado: {len(musicas)} músicas")
    
    if len(musicas) >= 5:
        print(f"   🎯 Seletores funcionando! Pronto para lista completa.")
    else:
        print(f"   ⚠️ Ainda precisamos ajustar os seletores.")