# Scraper Sequencial de Letras de Sertanejo

Sistema de web scraping em código sequencial puro (sem classes) para coleta de letras de música sertaneja do site Letras.mus.br.

## 🎯 Características

- **Código sequencial simples** - sem classes, apenas funções
- **Web scraping robusto** com rate limiting e tratamento de erros
- **Validação automática** de qualidade das letras
- **Exportação** em JSON e CSV
- **Relatórios estatísticos** automáticos

## 📁 Arquivo Principal

```
scraper_sertanejo.py - Script sequencial completo (450+ linhas)
```

## 🛠️ Instalação Rápida

```bash
pip install requests beautifulsoup4 pandas unidecode
```

## 💻 Uso Simples

1. **Edite as configurações** no final do arquivo `scraper_sertanejo.py`:

```python
# EDITE AQUI - suas configurações
ARTISTAS_PARA_COLETAR = [
    "Victor e Leo",
    "Bruno e Marrone", 
    "Jorge e Mateus"
]

MAX_MUSICAS_POR_ARTISTA = 10  # None = todas
```

2. **Execute o script**:

```bash
python scraper_sertanejo.py
```

3. **Acompanhe o progresso** no terminal e os arquivos serão salvos automaticamente.

## 📊 Saída Automática

O script gera automaticamente:

- **`letras_sertanejo_YYYYMMDD_HHMMSS.json`** - Dados em formato JSON
- **`letras_sertanejo_YYYYMMDD_HHMMSS.csv`** - Dados em formato CSV
- **Relatório estatístico** no terminal

## � Estrutura dos Dados

Cada música coletada tem:

```json
{
    "titulo": "Nome da Música",
    "artista": "Nome do Artista", 
    "letra": "Texto completo da letra",
    "url": "URL da música no site",
    "ano": 2023,
    "contagem_palavras": 150,
    "contagem_linhas": 32,
    "coletado_em": "2025-09-30T10:30:00"
}
```

## ⚙️ Funcionalidades Incluídas

### � Busca Inteligente
- Normalização automática de nomes de artistas
- Busca direta por URL + busca por termo
- Tratamento de caracteres especiais e acentos

### 🛡️ Proteções
- Rate limiting configurável (1-3 segundos entre requests)
- Headers de navegador real
- Timeout de 30 segundos
- Detecção de páginas de erro

### ✅ Validação de Qualidade
- Filtro de letras muito curtas (< 20 palavras)
- Filtro de letras muito longas (> 2000 palavras)
- Detecção de conteúdo inválido
- Verificação de estrutura mínima

### 📈 Relatórios
- Estatísticas por artista
- Contagem total de palavras
- Distribuição temporal (se anos disponíveis)
- Taxa de sucesso do scraping

## 🎵 Artistas Populares Incluídos

Lista pré-configurada com 20+ artistas:
- Zezé Di Camargo e Luciano
- Chitãozinho e Xororó  
- Bruno e Marrone
- Victor e Leo
- Jorge e Mateus
- Henrique e Juliano
- Marília Mendonça
- Gusttavo Lima
- E muitos outros...

## ⚖️ Uso Responsável

### ✅ Recomendado para:
- Pesquisa acadêmica
- Análise de texto e linguística
- Estudos de música brasileira
- Projetos de ciência de dados

### ⚠️ Rate Limiting
- Delay automático de 1-3 segundos entre requests
- Pausa adicional de 5 segundos entre artistas
- Delay extra para listas grandes (>20 músicas)

### 🔒 Considerações Legais
- Respeita robots.txt e termos de uso
- Apenas para análise, não redistribuição
- Headers educados e identificação apropriada

## � Resolução de Problemas

**"Artista não encontrado"**
- Verifique a grafia exata do nome
- Teste com artistas da lista popular primeiro

**"Letra não encontrada"**  
- Algumas músicas podem não ter letra disponível
- O script automaticamente pula e continua

**"Imports não encontrados"**
- Execute: `pip install requests beautifulsoup4 pandas unidecode`
- Se `unidecode` falhar, o script usa alternativa interna

## � Performance Típica

- **~2-4 segundos** por música (com rate limiting)
- **~10-50 músicas** por artista típico
- **~100-200 letras/hora** em execução normal
- **Arquivos de saída** leves (JSON ~1MB para 100 músicas)

## 🔧 Personalização

### Ajustar Rate Limiting
```python
DELAY_MIN = 0.5  # Mais rápido (cuidado!)
DELAY_MAX = 5.0  # Mais conservador
```

### Filtros de Qualidade
```python
# Na função validar_qualidade_letra():
if contagem_palavras < 30:  # Mínimo mais alto
if contagem_palavras > 1000:  # Máximo mais baixo
```

### Timeout de Requests
```python
TIMEOUT = 60  # 60 segundos para conexões lentas
```

---

**🎵 Script sequencial completo para coleta educacional de letras de sertanejo 🎵**