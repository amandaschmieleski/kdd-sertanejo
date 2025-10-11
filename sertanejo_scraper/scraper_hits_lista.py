# ================================================================================
# SCRAPER DE HITS MAIS ACESSADOS - LISTA ESPECÍFICA
# Coleta músicas baseada na lista de mais acessados fornecida pelo usuário
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

def remover_acentos(texto):
    """Remove acentos do texto."""
    try:
        return unidecode.unidecode(texto)
    except:
        return texto

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

def validar_qualidade_letra(letra, titulo=""):
    """Valida se a letra tem qualidade adequada."""
    if not letra or len(letra.strip()) < 50:
        return False
    
    contagem_palavras = len(letra.split())
    if contagem_palavras < 10:
        return False
    
    return True

def construir_url_musica(titulo, artista):
    """Constrói a URL da música no Letras.mus.br."""
    
    # Limpar e normalizar nomes
    titulo_limpo = titulo.strip()
    artista_limpo = artista.strip()
    
    # Remover partes entre parênteses do título
    titulo_limpo = re.sub(r'\s*\([^)]*\)\s*', '', titulo_limpo)
    
    # Substituir caracteres especiais
    def normalizar_url(texto):
        # Remover acentos
        texto = remover_acentos(texto)
        # Converter para minúsculas
        texto = texto.lower()
        # Remover caracteres especiais, manter apenas letras, números e espaços
        texto = re.sub(r'[^a-z0-9\s&]', '', texto)
        # Substituir & por e
        texto = texto.replace('&', 'e')
        # Trocar espaços por hífens
        texto = re.sub(r'\s+', '-', texto)
        # Remover hífens no início/fim
        texto = texto.strip('-')
        return texto
    
    artista_url = normalizar_url(artista_limpo)
    titulo_url = normalizar_url(titulo_limpo)
    
    # Construir URL
    url = f"https://www.letras.mus.br/{artista_url}/{titulo_url}/"
    
    return url

def buscar_musica_alternativa(titulo, artista):
    """Tenta encontrar a música usando busca."""
    
    try:
        # Tentar busca no Google do site
        query = f"site:letras.mus.br {titulo} {artista}"
        query_encoded = quote(query)
        
        # Como não podemos fazer busca no Google diretamente,
        # vamos tentar algumas variações da URL
        
        variações = []
        
        # Variação 1: título e artista completos
        variações.append(construir_url_musica(titulo, artista))
        
        # Variação 2: remover acentos e caracteres especiais do título
        titulo_simples = re.sub(r'[^\w\s]', '', titulo)
        variações.append(construir_url_musica(titulo_simples, artista))
        
        # Variação 3: apenas primeiras palavras do título
        titulo_curto = ' '.join(titulo.split()[:3])
        variações.append(construir_url_musica(titulo_curto, artista))
        
        # Testar cada variação
        for url in variações:
            soup = fazer_request(url)
            if soup:
                # Verificar se encontrou a página correta
                title_elem = soup.find('h1', class_='head_title')
                if title_elem:
                    return url
        
        return None
        
    except Exception:
        return None

def extrair_letra_completa(url_musica, titulo_original, artista_original, ranking_pos):
    """Extrai letra completa de uma música."""
    
    print(f"[{ranking_pos:3}] 🎵 {artista_original} - {titulo_original}")
    
    soup = fazer_request(url_musica)
    if not soup:
        print(f"      ❌ Erro ao acessar URL")
        return None
    
    try:
        # Verificar se a página existe (não é erro 404)
        title_elem = soup.find('h1', class_='head_title')
        if not title_elem:
            print(f"      ❌ Página não encontrada")
            return None
        
        titulo = title_elem.get_text(strip=True)
        
        # Extrair artista
        artista_elem = soup.find('h2', class_='head_subtitle')
        artista = artista_elem.get_text(strip=True) if artista_elem else artista_original
        
        # Extrair letra
        letra_elem = soup.select_one('.lyric-original')
        if not letra_elem:
            print(f"      ❌ Letra não encontrada")
            return None
        
        letra_bruta = letra_elem.get_text()
        letra_limpa = limpar_letra(letra_bruta)
        
        if not validar_qualidade_letra(letra_limpa, titulo):
            print(f"      ⚠️ Letra de baixa qualidade")
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
            'fonte': 'ranking_mais_acessadas_usuario'
        }
        
        ano_str = f", ano: {ano}" if ano else ""
        print(f"      ✅ Sucesso! ({dados_musica['contagem_palavras']} palavras{ano_str})")
        return dados_musica
        
    except Exception as e:
        print(f"      ❌ Erro: {str(e)}")
        return None

def processar_lista_hits():
    """Processa a lista de hits fornecida pelo usuário."""
    
    # Lista de hits mais acessados (formato: título, artista, título, artista...)
    lista_raw = '''Amor Dos Outros
Henrique & Juliano
Evidências
Chitãozinho & Xororó
Body Splash (part. Luan Pereira)
Felipe Araújo
Caso Indefinido
Cristiano Araújo
OLHO MARROM
Luan Santana
Tocando Em Frente
Almir Sater
Tubarões
Diego e Victor Hugo
Decida
Milionário e José Rico
Se Eu Te Perdoar (part. Zé Felipe)
Clayton e Romário
Princesa (part. Ana Castela)
Gustavo Mioto
Seja Ex
Henrique & Juliano
Retrovisor
Gusttavo Lima
Erro Gostoso
Simone Mendes
Sublime renúncia
Leandro & Leonardo
Cuida Bem Dela
Henrique & Juliano
Saudade Proibida
Simone Mendes
Todo Mundo Menos Eu (part. Ana Castela)
Hugo & Guilherme
Escondendo o Ouro
Zé Neto e Cristiano
Proibido Terminar
Gusttavo Lima
Realidade Ou Fantasia
Henrique & Juliano
Dois Tristes
Simone Mendes
Vai Cair Água (part. Zé Neto e Cristiano)
Diego e Arnaldo
Logo Logo
Henrique & Juliano
Evento Cancelado
Henrique & Juliano
Ela É Demais
Rick & Renner
Amo Noite e Dia
Jorge & Mateus
Boate Azul
Bruno & Marrone
Apaga Apaga Apaga
Danilo e Davi
Infiel
Marília Mendonça'''.strip()
    
    # Processar lista
    linhas = [linha.strip() for linha in lista_raw.split('\n') if linha.strip()]
    
    musicas = []
    for i in range(0, len(linhas), 2):
        if i + 1 < len(linhas):
            titulo = linhas[i]
            artista = linhas[i + 1]
            posicao = (i // 2) + 1
            
            musicas.append({
                'posicao': posicao,
                'titulo': titulo,
                'artista': artista
            })
    
    print(f"🎯 LISTA DE HITS MAIS ACESSADOS PROCESSADA")
    print("=" * 60)
    print(f"📊 Total de músicas na lista: {len(musicas)}")
    print(f"📋 Primeiras 5 músicas:")
    for i, musica in enumerate(musicas[:5]):
        print(f"   {musica['posicao']:2}. {musica['artista']} - {musica['titulo']}")
    
    return musicas

def coletar_hits_lista(limite=50):
    """Coleta os hits da lista fornecida."""
    
    print(f"🚀 COLETA DE HITS MAIS ACESSADOS")
    print("=" * 70)
    
    # Processar lista
    musicas_lista = processar_lista_hits()
    
    # Limitar se necessário
    if limite and limite < len(musicas_lista):
        musicas_lista = musicas_lista[:limite]
        print(f"⚠️ Limitando coleta a {limite} músicas")
    
    print(f"\n🎵 Iniciando coleta de {len(musicas_lista)} músicas...")
    
    musicas_coletadas = []
    sucessos = 0
    falhas = 0
    
    for musica in musicas_lista:
        posicao = musica['posicao']
        titulo = musica['titulo']
        artista = musica['artista']
        
        # Construir URL
        url_principal = construir_url_musica(titulo, artista)
        
        # Tentar extrair
        dados = extrair_letra_completa(url_principal, titulo, artista, posicao)
        
        if dados:
            musicas_coletadas.append(dados)
            sucessos += 1
        else:
            # Tentar URLs alternativas
            print(f"      🔄 Tentando URLs alternativas...")
            url_alternativa = buscar_musica_alternativa(titulo, artista)
            if url_alternativa and url_alternativa != url_principal:
                dados = extrair_letra_completa(url_alternativa, titulo, artista, posicao)
                if dados:
                    musicas_coletadas.append(dados)
                    sucessos += 1
                else:
                    falhas += 1
            else:
                falhas += 1
        
        # Delay entre requisições
        time.sleep(random.uniform(1.5, 3.0))
        
        # Progresso a cada 10 músicas
        if (sucessos + falhas) % 10 == 0:
            progresso = ((sucessos + falhas) / len(musicas_lista)) * 100
            print(f"\n📊 Progresso: {progresso:.1f}% - Sucessos: {sucessos}, Falhas: {falhas}")
    
    print(f"\n" + "=" * 70)
    print(f"📊 RESULTADO DA COLETA:")
    print(f"   ✅ Sucessos: {sucessos}")
    print(f"   ❌ Falhas: {falhas}")
    print(f"   📈 Taxa de sucesso: {(sucessos/(sucessos+falhas)*100):.1f}%")
    
    if musicas_coletadas:
        # Salvar dados
        df = pd.DataFrame(musicas_coletadas)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        arquivo = f"hits_mais_acessados_sertanejo_{timestamp}.csv"
        df.to_csv(arquivo, index=False, encoding='utf-8')
        
        print(f"💾 Dados salvos em: {arquivo}")
        
        # Análises
        total_palavras = df['contagem_palavras'].sum()
        musicas_com_ano = df[df['ano'].notna()]
        musicas_2023_plus = df[df['ano'] >= 2023] if len(musicas_com_ano) > 0 else pd.DataFrame()
        
        print(f"\n📊 ANÁLISE DA COLETA:")
        print(f"   Total de palavras: {total_palavras:,}")
        print(f"   Média por música: {df['contagem_palavras'].mean():.0f} palavras")
        print(f"   Músicas com ano: {len(musicas_com_ano)}")
        print(f"   Músicas 2023+: {len(musicas_2023_plus)}")
        
        # Top artistas
        if len(df) > 0:
            top_artistas = df['artista'].value_counts().head()
            print(f"\n🎤 TOP ARTISTAS NO RANKING:")
            for artista, count in top_artistas.items():
                print(f"   {artista}: {count} músicas")
        
        # Músicas mais longas
        print(f"\n📏 TOP 5 MÚSICAS MAIS LONGAS:")
        top_longas = df.nlargest(5, 'contagem_palavras')
        for _, row in top_longas.iterrows():
            ano_str = f" ({int(row['ano'])})" if pd.notna(row['ano']) else ""
            print(f"   #{row['ranking_posicao']:2} {row['artista']} - {row['titulo']}: {row['contagem_palavras']} palavras{ano_str}")
    
    return musicas_coletadas

if __name__ == "__main__":
    print("🚀 Iniciando coleta de hits mais acessados do sertanejo...")
    
    # Coletar primeiras 100 músicas como teste
    musicas = coletar_hits_lista(limite=100)
    
    print(f"\n✅ COLETA CONCLUÍDA!")
    print(f"   📊 Total coletado: {len(musicas)} músicas")
    
    if len(musicas) > 0:
        print(f"   🎯 Próximo passo: Expandir para lista completa se resultados forem bons")