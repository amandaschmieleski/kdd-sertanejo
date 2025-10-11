# ================================================================================
# SCRAPER SEQUENCIAL DE LETRAS DE SERTANEJO
# Web scraping do site Letras.mus.br para coleta de letras de música sertaneja
# Data: 30/09/2025
# ================================================================================

# Bibliotecas necessárias (instalar com: pip install requests beautifulsoup4 pandas unidecode)
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
import json
from datetime import datetime
from urllib.parse import urljoin, quote

# Tentar importar unidecode, se não estiver disponível usar alternativa
try:
    import unidecode
    HAS_UNIDECODE = True
except ImportError:
    HAS_UNIDECODE = False
    print("⚠️  Biblioteca 'unidecode' não encontrada. Instale com: pip install unidecode")
    print("   Continuando sem remoção de acentos...")

def remover_acentos(texto):
    """Remove acentos do texto, com ou sem unidecode."""
    if HAS_UNIDECODE:
        return unidecode.unidecode(texto)
    else:
        # Alternativa simples sem unidecode
        replacements = {
            'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a', 'ä': 'a',
            'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
            'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
            'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o', 'ö': 'o',
            'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
            'ç': 'c', 'ñ': 'n',
            'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A', 'Ä': 'A',
            'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
            'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
            'Ó': 'O', 'Ò': 'O', 'Õ': 'O', 'Ô': 'O', 'Ö': 'O',
            'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ü': 'U',
            'Ç': 'C', 'Ñ': 'N'
        }
        for accented, normal in replacements.items():
            texto = texto.replace(accented, normal)
        return texto

# ================================================================================
# CONFIGURAÇÕES GLOBAIS
# ================================================================================

# Configurações do scraper
BASE_URL = "https://www.letras.mus.br"
DELAY_MIN = 1.0  # Delay mínimo entre requests (segundos)
DELAY_MAX = 3.0  # Delay máximo entre requests (segundos)
TIMEOUT = 30     # Timeout para requests (segundos)

# Headers para parecer mais humano
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Lista de artistas populares de sertanejo
ARTISTAS_POPULARES = [
    "Zezé Di Camargo e Luciano",
    "Chitãozinho e Xororó",
    "Bruno e Marrone",
    "Victor e Leo",
    "Jorge e Mateus",
    "Henrique e Juliano",
    "Marília Mendonça",
    "Gusttavo Lima",
    "Luan Santana",
    "Wesley Safadão",
    "Matheus e Kauan",
    "Simone e Simaria",
    "Maiara e Maraisa",
    "Zé Neto e Cristiano",
    "Israel e Rodolffo",
    "César Menotti e Fabiano",
    "João Bosco e Vinícius",
    "Marcos e Belutti",
    "Thaeme e Thiago",
    "Fernando e Sorocaba"
]

print("=" * 80)
print("SCRAPER SEQUENCIAL DE LETRAS DE SERTANEJO")
print("=" * 80)
print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print()

# ================================================================================
# FUNÇÕES AUXILIARES
# ================================================================================

def aplicar_delay():
    """Aplica delay aleatório entre requests."""
    delay = random.uniform(DELAY_MIN, DELAY_MAX)
    time.sleep(delay)

def fazer_request(url):
    """
    Faz request HTTP com tratamento de erros.
    Retorna BeautifulSoup object ou None se erro.
    """
    try:
        aplicar_delay()
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        
        # Verificar se não é página de erro
        if "página não encontrada" in response.text.lower():
            print(f"⚠️  Página não encontrada: {url}")
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar {url}: {str(e)}")
        return None

def normalizar_nome_artista(nome_artista):
    """Normaliza o nome do artista para URL."""
    # Remover acentos
    nome_normalizado = remover_acentos(nome_artista.lower())
    # Substituir espaços e caracteres especiais
    nome_normalizado = nome_normalizado.replace(' ', '-').replace('&', 'e')
    # Remover caracteres não alfanuméricos (exceto hífen)
    nome_normalizado = re.sub(r'[^a-z0-9\-]', '', nome_normalizado)
    return nome_normalizado

def limpar_letra(texto_bruto):
    """Limpa e formata o texto da letra."""
    if not texto_bruto:
        return ""
    
    # Remover quebras de linha excessivas
    linhas = [linha.strip() for linha in texto_bruto.split('\n')]
    linhas = [linha for linha in linhas if linha]  # Remover linhas vazias
    
    # Juntar linhas com espaços para evitar palavras concatenadas
    texto_limpo = ' '.join(linhas)
    
    # Corrigir concatenações comuns onde quebras de linha juntaram palavras
    import re
    
    # Padrão: palavra(minúscula)MAIÚSCULA -> palavra MAIÚSCULA  
    texto_limpo = re.sub(r'([a-záéíóúâêîôûàèìòùãç])([ÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÃÇA-Z])', r'\1 \2', texto_limpo)
    
    # Padrão: pontuação+MAIÚSCULA -> pontuação MAIÚSCULA
    texto_limpo = re.sub(r'([!?.,;:])([A-ZÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÃÇ])', r'\1 \2', texto_limpo)
    
    # Remover caracteres especiais desnecessários
    texto_limpo = texto_limpo.replace('\r', '')
    texto_limpo = texto_limpo.replace('\t', ' ')
    
    # Remover espaços duplos
    while '  ' in texto_limpo:
        texto_limpo = texto_limpo.replace('  ', ' ')
    
    return texto_limpo.strip()

def extrair_ano(soup):
    """Extrai o ano da música se disponível."""
    try:
        import json
        
        # 1. Procurar em JSON-LD (Schema.org) - estratégia mais confiável
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
                                return int(ano_match.group())
                    
                    # Se for MusicRecording, procurar em album
                    if data.get('@type') == 'MusicRecording' and 'inAlbum' in data:
                        album = data['inAlbum']
                        if isinstance(album, dict) and 'datePublished' in album:
                            ano_match = re.search(r'\b(19|20)\d{2}\b', str(album['datePublished']))
                            if ano_match:
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
                    return int(ano_match.group())
        
        # 3. Procurar em elementos com microdata
        elementos_microdata = soup.find_all(attrs={'itemprop': re.compile(r'date|year', re.I)})
        for elem in elementos_microdata:
            texto = elem.get_text() or elem.get('content', '') or elem.get('datetime', '')
            ano_match = re.search(r'\b(19|20)\d{2}\b', texto)
            if ano_match:
                return int(ano_match.group())
        
        # 4. Estratégia original como fallback
        elementos_ano = [
            soup.find('span', class_='year'),
            soup.find('time'),
            soup.find('div', class_='song-info')
        ]
        
        for elemento in elementos_ano:
            if elemento:
                texto = elemento.get_text()
                match_ano = re.search(r'\b(19|20)\d{2}\b', texto)
                if match_ano:
                    return int(match_ano.group())
        
        return None
        
    except Exception:
        return None

def validar_qualidade_letra(dados_musica):
    """
    Valida a qualidade de uma letra.
    Retorna True se a letra tem qualidade adequada.
    """
    letra = dados_musica.get('letra', '')
    titulo = dados_musica.get('titulo', '')
    
    # DEBUG: mostrar info da letra
    print(f"   📝 Validando: {len(letra)} caracteres, {len(letra.split())} palavras")
    
    # Verificar comprimento mínimo
    contagem_palavras = len(letra.split())
    if contagem_palavras < 10:
        print(f"   ❌ Muito curta: {contagem_palavras} palavras")
        return False
    
    # Verificar se não é muito longa (possível erro)
    if contagem_palavras > 2000:
        print(f"   ❌ Muito longa: {contagem_palavras} palavras")
        return False
    
    # Verificar indicadores de conteúdo inválido
    indicadores_invalidos = [
        'página não encontrada',
        'erro 404',
        'acesso negado',
        'letra não disponível'
    ]
    
    letra_lower = letra.lower()
    titulo_lower = titulo.lower()
    
    for indicador in indicadores_invalidos:
        if indicador in letra_lower or indicador in titulo_lower:
            print(f"   ❌ Conteúdo inválido: {indicador}")
            return False
    
    print(f"   ✅ Qualidade OK: {contagem_palavras} palavras")
    return True

# ================================================================================
# FUNÇÃO PRINCIPAL DE BUSCA DE ARTISTA
# ================================================================================

def buscar_artista(nome_artista):
    """
    Busca o URL do artista no site.
    Retorna URL do artista ou None se não encontrado.
    """
    print(f"🔍 Buscando artista: {nome_artista}")
    
    # Tentar URL direta primeiro
    nome_normalizado = normalizar_nome_artista(nome_artista)
    url_direta = f"{BASE_URL}/{nome_normalizado}/"
    
    soup = fazer_request(url_direta)
    
    # Verificar se é página válida de artista
    if soup and (soup.find('h1', class_='head_title') or 
                soup.find('div', class_='artist-info') or 
                soup.find('ul', class_='songList') or
                soup.find('h1') and 'discografia' in soup.get_text().lower()):
        print(f"✅ Artista encontrado: {url_direta}")
        return url_direta
    
    # Se URL direta não funcionou, tentar busca
    print(f"🔍 Tentando busca por: {nome_artista}")
    url_busca = f"{BASE_URL}/busca.php?words={quote(nome_artista)}"
    soup = fazer_request(url_busca)
    
    if not soup:
        return None
    
    # Procurar link do artista nos resultados
    links_artista = soup.find_all('a', href=True)
    for link in links_artista:
        href = link.get('href', '')
        texto = link.get_text(strip=True)
        
        if (href.startswith('/') and 
            nome_artista.lower() in texto.lower() and
            'discografia' in href):
            
            url_artista = urljoin(BASE_URL, href.replace('/discografia', ''))
            print(f"✅ Artista encontrado via busca: {url_artista}")
            return url_artista
    
    print(f"❌ Artista não encontrado: {nome_artista}")
    return None

# ================================================================================
# FUNÇÃO PARA OBTER LISTA DE MÚSICAS
# ================================================================================

def obter_musicas_artista(url_artista, limite=None):
    """
    Obtém lista de músicas do artista.
    Retorna lista de dicionários com informações das músicas.
    """
    print(f"📋 Obtendo lista de músicas de: {url_artista}")
    
    soup = fazer_request(url_artista)
    if not soup:
        return []
    
    musicas = []
    
    # Procurar diferentes estruturas de lista de músicas
    containers_musicas = [
        soup.find_all('li', class_='songList-table-row'),
        soup.find_all('a', class_='song-name'),
        soup.find_all('div', class_='cnt-list-songs'),
    ]
    
    for lista_container in containers_musicas:
        if lista_container:
            for item in lista_container:
                # Extrair link da música
                link = item.find('a', href=True)
                if not link:
                    if item.name == 'a':
                        link = item
                    else:
                        continue
                
                titulo_musica = link.get_text(strip=True)
                url_musica = urljoin(BASE_URL, link['href'])
                
                if titulo_musica and url_musica:
                    musicas.append({
                        'titulo': titulo_musica,
                        'url': url_musica,
                        'url_artista': url_artista
                    })
                    
                    if limite and len(musicas) >= limite:
                        break
            break
    
    print(f"📋 Encontradas {len(musicas)} músicas")
    return musicas[:limite] if limite else musicas

# ================================================================================
# FUNÇÃO PARA EXTRAIR LETRA DE UMA MÚSICA
# ================================================================================

def extrair_letra_musica(url_musica, nome_artista_real=None):
    """
    Extrai a letra de uma música.
    Retorna dicionário com dados da música ou None.
    """
    soup = fazer_request(url_musica)
    if not soup:
        return None
    
    try:
        # Extrair título
        elemento_titulo = soup.find('h1', class_='head_title')
        if not elemento_titulo:
            elemento_titulo = soup.find('h1')
        
        titulo = elemento_titulo.get_text(strip=True) if elemento_titulo else "Título não encontrado"
        
        # Usar nome do artista fornecido ou tentar extrair da página
        if nome_artista_real:
            artista = nome_artista_real
        else:
            # Extrair artista da página (fallback)
            elemento_artista = soup.find('h2', class_='head_subtitle')
            if not elemento_artista:
                elemento_artista = soup.find('h2')
            artista = elemento_artista.get_text(strip=True) if elemento_artista else "Artista não encontrado"
        
        # Extrair letra - tentar diferentes seletores
        seletores_letra = [
            '.lyric-original',      # Principal do Letras.mus.br
            'div[class*="lyric"]',
            'div[class*="letra"]',
            'div.cnt-lyric',
            'pre.lyric'
        ]
        
        elemento_letra = None
        for seletor in seletores_letra:
            elemento_letra = soup.select_one(seletor)
            if elemento_letra and len(elemento_letra.get_text().strip()) > 50:
                break
        
        if not elemento_letra:
            print(f"⚠️  Letra não encontrada em: {url_musica}")
            return None
        
        # Limpar e extrair texto da letra
        texto_letra = limpar_letra(elemento_letra.get_text())
        
        if not texto_letra.strip():
            print(f"⚠️  Letra vazia em: {url_musica}")
            return None
        
        # Extrair ano se disponível
        ano = extrair_ano(soup)
        
        # Montar dados da música
        dados_musica = {
            'titulo': titulo,
            'artista': artista,
            'letra': texto_letra,
            'url': url_musica,
            'ano': ano,
            'coletado_em': datetime.now().isoformat(),
            'contagem_palavras': len(texto_letra.split()),
            'contagem_linhas': len(texto_letra.split('\n'))
        }
        
        # Validar qualidade
        if validar_qualidade_letra(dados_musica):
            print(f"✅ Letra extraída: {artista} - {titulo} ({dados_musica['contagem_palavras']} palavras)")
            return dados_musica
        else:
            print(f"⚠️  Letra de baixa qualidade rejeitada: {titulo}")
            return None
        
    except Exception as e:
        print(f"❌ Erro ao extrair letra de {url_musica}: {str(e)}")
        return None

# ================================================================================
# FUNÇÃO PRINCIPAL DE SCRAPING
# ================================================================================

def fazer_scraping_artista(nome_artista, max_musicas=None):
    """
    Faz scraping completo de um artista.
    Retorna lista de dicionários com letras das músicas.
    """
    print(f"\n🎵 Iniciando scraping de: {nome_artista}")
    print("-" * 60)
    
    # 1. Buscar artista
    url_artista = buscar_artista(nome_artista)
    if not url_artista:
        print(f"❌ Artista não encontrado: {nome_artista}")
        return []
    
    # 2. Obter lista de músicas
    musicas = obter_musicas_artista(url_artista, limite=max_musicas)
    if not musicas:
        print(f"❌ Nenhuma música encontrada para: {nome_artista}")
        return []
    
    print(f"🎼 Iniciando download de {len(musicas)} músicas...")
    
    # 3. Baixar letras
    letras_coletadas = []
    contador_sucesso = 0
    contador_falha = 0
    
    for i, musica in enumerate(musicas, 1):
        print(f"[{i}/{len(musicas)}] Processando: {musica['titulo']}")
        
        letra = extrair_letra_musica(musica['url'], nome_artista)
        if letra:
            letras_coletadas.append(letra)
            contador_sucesso += 1
        else:
            contador_falha += 1
        
        # Rate limiting mais agressivo para muitas músicas
        if len(musicas) > 20:
            time.sleep(random.uniform(2.0, 4.0))
    
    print(f"\n📊 Scraping de {nome_artista} concluído:")
    print(f"   ✅ Sucessos: {contador_sucesso}")
    print(f"   ❌ Falhas: {contador_falha}")
    if (contador_sucesso + contador_falha) > 0:
        taxa_sucesso = (contador_sucesso/(contador_sucesso+contador_falha)*100)
        print(f"   📈 Taxa de sucesso: {taxa_sucesso:.1f}%")
    
    # Mostrar preview das músicas coletadas
    if letras_coletadas:
        print(f"\n🎵 MÚSICAS COLETADAS DE {nome_artista.upper()}:")
        print("-" * 70)
        for i, musica in enumerate(letras_coletadas, 1):
            titulo_truncado = musica['titulo'][:40] + "..." if len(musica['titulo']) > 40 else musica['titulo']
            print(f"   {i:2d}. {titulo_truncado:<43} ({musica['contagem_palavras']:3d} palavras)")
        print("-" * 70)
    
    return letras_coletadas

# ================================================================================
# FUNÇÃO PARA SALVAR DADOS
# ================================================================================

def salvar_dados(dados_letras, nome_arquivo_base):
    """Salva os dados coletados em diferentes formatos."""
    if not dados_letras:
        print("⚠️  Nenhum dado para salvar")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Salvar em JSON
    arquivo_json = f"{nome_arquivo_base}_{timestamp}.json"
    with open(arquivo_json, 'w', encoding='utf-8') as f:
        json.dump(dados_letras, f, ensure_ascii=False, indent=2)
    print(f"💾 Dados salvos em JSON: {arquivo_json}")
    
    # Salvar em CSV
    try:
        df = pd.DataFrame(dados_letras)
        arquivo_csv = f"{nome_arquivo_base}_{timestamp}.csv"
        df.to_csv(arquivo_csv, index=False, encoding='utf-8')
        print(f"💾 Dados salvos em CSV: {arquivo_csv}")
    except Exception as e:
        print(f"⚠️  Erro ao salvar CSV: {str(e)}")

def gerar_relatorio(dados_letras):
    """Gera relatório estatístico dos dados coletados."""
    if not dados_letras:
        print("⚠️  Nenhum dado para relatório")
        return
    
    print("\n" + "=" * 80)
    print("📊 RELATÓRIO ESTATÍSTICO - LETRAS DE SERTANEJO")
    print("=" * 80)
    
    # Criar DataFrame para análise
    df = pd.DataFrame(dados_letras)
    
    total_musicas = len(dados_letras)
    total_palavras = sum(musica['contagem_palavras'] for musica in dados_letras)
    media_palavras = total_palavras / total_musicas if total_musicas > 0 else 0
    
    # Estatísticas gerais
    print(f"\n📈 ESTATÍSTICAS GERAIS:")
    print(f"   Total de músicas coletadas: {total_musicas}")
    print(f"   Total de palavras: {total_palavras:,}")
    print(f"   Média de palavras por música: {media_palavras:.1f}")
    print(f"   Artistas únicos: {df['artista'].nunique()}")
    
    # Tabela resumo por artista
    print(f"\n🎤 RESUMO POR ARTISTA:")
    resumo_artista = df.groupby('artista').agg({
        'titulo': 'count',
        'contagem_palavras': ['sum', 'mean'],
        'contagem_linhas': 'mean',
        'ano': lambda x: f"{x.min()}-{x.max()}" if x.notna().any() else "N/A"
    }).round(1)
    
    # Simplificar nomes das colunas
    resumo_artista.columns = ['Músicas', 'Total Palavras', 'Média Palavras', 'Média Linhas', 'Período']
    
    # Exibir tabela formatada
    print(resumo_artista.to_string())
    
    # Top 10 músicas com mais palavras
    print(f"\n🏆 TOP 10 MÚSICAS COM MAIS PALAVRAS:")
    top_musicas = df.nlargest(10, 'contagem_palavras')[['artista', 'titulo', 'contagem_palavras']]
    top_musicas.columns = ['Artista', 'Música', 'Palavras']
    print(top_musicas.to_string(index=False))
    
    # Distribuição de anos (se disponível)
    anos_com_dados = df[df['ano'].notna()]
    if len(anos_com_dados) > 0:
        print(f"\n📅 DISTRIBUIÇÃO POR DÉCADA:")
        anos_com_dados['decada'] = (anos_com_dados['ano'] // 10) * 10
        dist_decada = anos_com_dados['decada'].value_counts().sort_index()
        
        for decada, count in dist_decada.items():
            print(f"   {int(decada)}s: {count} músicas")
    
    # Estatísticas de qualidade
    print(f"\n🔍 ESTATÍSTICAS DE QUALIDADE:")
    print(f"   Menor número de palavras: {df['contagem_palavras'].min()}")
    print(f"   Maior número de palavras: {df['contagem_palavras'].max()}")
    print(f"   Desvio padrão de palavras: {df['contagem_palavras'].std():.1f}")
    
    quartis = df['contagem_palavras'].quantile([0.25, 0.5, 0.75])
    print(f"   Q1 (25%): {quartis[0.25]:.0f} palavras")
    print(f"   Mediana: {quartis[0.5]:.0f} palavras") 
    print(f"   Q3 (75%): {quartis[0.75]:.0f} palavras")
    
    print("\n" + "=" * 80)

# ================================================================================
# EXECUÇÃO PRINCIPAL
# ================================================================================

def main():
    """Função principal do programa."""
    
    # Configurações do usuário - COLETA MASSIVA PARA MODELO ML
    ARTISTAS_PARA_COLETAR = [
        # ============ JÁ COLETADOS (manter) ============
        "Chitãozinho e Xororó",
        "Bruno e Marrone", 
        "Henrique & Juliano",
        "Jorge & Mateus",
        "Zezé Di Camargo & Luciano",
        "Leandro & Leonardo",
        "Marília Mendonça",
        "Paula Fernandes",
        "Milionário e José Rico",
        "Almir Sater",
        "Diego e Victor Hugo",
        "Gustavo Mioto",
        
        # ============ EXPANSÃO MASSIVA ============
        # Sertanejo Moderno Top
        "Luan Santana",
        "Gusttavo Lima", 
        "Zé Neto e Cristiano",
        "Matheus & Kauan",
        
        # Feminino
        "Simone Mendes",
        "Ana Castela",
        "Lauana Prado",
        "Maiara & Maraisa",
        
        # Clássicos/Icônicos
        "Rick & Renner",
        "Victor & Leo",
        "Daniel",
        "Leonardo",
        "Chrystian & Ralf",
        
        # Nova Geração
        "Felipe Araújo",
        "Murilo Huff",
        "Zé Felipe",
        "Luan Pereira",
        
        # Raiz/Tradicional
        "Tião Carreiro e Pardinho",
        "Trio Parada Dura",
        "João Mineiro e Marciano",
        "Gino e Geno",
        "Sérgio Reis",
        "Tonico e Tinoco",
        "Teodoro e Sampaio",
        
        # Populares Diversos
        "Eduardo Costa",
        "Hugo & Guilherme",
        "Clayton e Romário",
        "Guilherme & Benuto",
        "Matogrosso & Mathias",
        "Ícaro e Gilmar",
        "Gian e Giovani",
        "Rionegro & Solimões",
        "João Paulo e Daniel",
        "Marcos & Belutti",
        "Lourenço e Lourival",
        "Edson & Hudson",
        "Chico Rey e Paraná",
        "Guilherme & Santiago"
    ]
    
    MAX_MUSICAS_POR_ARTISTA = 10  # Reduzindo para 10 para cobrir mais artistas
    NOME_ARQUIVO_BASE = "letras_sertanejo_massivo"
    
    print("🚀 Configurações:")
    print(f"   Artistas: {', '.join(ARTISTAS_PARA_COLETAR)}")
    print(f"   Máx. músicas por artista: {MAX_MUSICAS_POR_ARTISTA or 'Todas'}")
    print(f"   Delay entre requests: {DELAY_MIN}-{DELAY_MAX}s")
    print()
    
    # Coletar dados de todos os artistas
    todas_as_letras = []
    
    for artista in ARTISTAS_PARA_COLETAR:
        letras_artista = fazer_scraping_artista(artista, MAX_MUSICAS_POR_ARTISTA)
        todas_as_letras.extend(letras_artista)
        
        # Pequena pausa entre artistas
        if len(ARTISTAS_PARA_COLETAR) > 1:
            print("⏳ Pausa entre artistas...")
            time.sleep(5)
    
    # Salvar dados coletados
    print("\n" + "=" * 60)
    print("💾 SALVANDO DADOS")
    print("=" * 60)
    
    salvar_dados(todas_as_letras, NOME_ARQUIVO_BASE)
    
    # Gerar relatório
    gerar_relatorio(todas_as_letras)
    
    print("\n" + "=" * 60)
    print("✅ SCRAPING CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    print(f"Finalizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# ================================================================================
# PONTO DE ENTRADA
# ================================================================================

if __name__ == "__main__":
    main()

# ================================================================================
# INSTRUÇÕES DE USO:
# ================================================================================
"""
COMO USAR ESTE SCRAPER:

1. INSTALAÇÃO:
   pip install requests beautifulsoup4 pandas

2. CONFIGURAÇÃO:
   - Edite a lista ARTISTAS_PARA_COLETAR na função main()
   - Ajuste MAX_MUSICAS_POR_ARTISTA conforme necessário
   - Modifique DELAY_MIN/DELAY_MAX se necessário

3. EXECUÇÃO:
   python scraper_sertanejo.py

4. RESULTADOS:
   - Arquivos JSON e CSV serão criados automaticamente
   - Relatório estatístico será exibido no final
   - Logs de progresso mostram o andamento

EXEMPLO DE CONFIGURAÇÃO:

ARTISTAS_PARA_COLETAR = [
    "Zezé Di Camargo e Luciano",
    "Chitãozinho e Xororó",
    "Henrique e Juliano"
]

MAX_MUSICAS_POR_ARTISTA = 50  # ou None para todas

OBSERVAÇÕES:
- O script respeita rate limiting (1-3s entre requests)
- Músicas de baixa qualidade são automaticamente filtradas
- Dados são salvos em JSON e CSV com timestamp
- O código é totalmente sequencial, sem classes
"""