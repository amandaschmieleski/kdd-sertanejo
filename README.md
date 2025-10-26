# Scraper de Letras de Sertanejo

Este projeto é um scraper especializado para coleta de letras de música sertaneja do site Letras.mus.br. Foi desenvolvido como parte de um trabalho prático de Mestrado em KDD (Knowledge Discovery in Databases).

## 🎯 Objetivo

Coletar letras de músicas sertanejas populares com informações completas como título, artista, ano de lançamento e contagem de palavras para análise posterior.

## 📁 Estrutura do Projeto

```
projeto_funk/
├── sertanejo_scraper/
│   ├── scraper_sertanejo.py           # Script principal de coleta
│   └── teste_hits_corrigido_*.csv     # Exemplo de dados coletados
├── requirements.txt                    # Dependências do projeto
├── trabalhoPratico2025.pdf            # Documento do trabalho
└── README.md                          # Esta documentação
```

## 🚀 Como Usar

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

### Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/vinigm/analise-letras-sertanejo.git
cd analise-letras-sertanejo
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute o scraper:**
```bash
cd sertanejo_scraper
python scraper_sertanejo.py
```

## 🔧 Funcionalidades

- ✅ **Coleta automatizada** de letras do Letras.mus.br
- ✅ **Extração inteligente** de ano de lançamento usando JSON-LD
- ✅ **Limpeza automática** de texto das letras
- ✅ **Rate limiting** para respeitar o site
- ✅ **Detecção de erros** e tratamento de exceções
- ✅ **Exportação para CSV** com encoding UTF-8
- ✅ **Análise automática** dos dados coletados

## 📊 Dados Coletados

Cada música coletada inclui:
- **Posição no ranking** de popularidade
- **Título** da música
- **Artista** (normalizado e original)
- **Letra completa** limpa e formatada
- **URL** da fonte
- **Ano** de lançamento (quando disponível)
- **Timestamp** da coleta
- **Contagem de palavras** e linhas
- **Fonte** da coleta

### Exemplo de Saída
```csv
ranking_posicao,titulo,artista,letra,ano,contagem_palavras,contagem_linhas
1,"Amor Dos Outros","Henrique & Juliano","[letra completa...]",2019,156,32
```

## ⚙️ Como Funciona o Scraper

1. **Lista de Teste**: Utiliza uma lista curada de hits sertanejos populares
2. **Construção de URLs**: Normaliza nomes de artistas e títulos para criar URLs válidas
3. **Extração Inteligente**: 
   - Busca títulos usando seletores CSS específicos
   - Identifica artistas através de links contextuais
   - Extrai letras usando múltiplos seletores como fallback
   - Localiza anos através de dados estruturados JSON-LD
4. **Limpeza de Dados**: Remove caracteres especiais e formata o texto
5. **Validação**: Verifica se a letra tem tamanho mínimo aceitável
6. **Rate Limiting**: Delay de 2-4 segundos entre requisições

## 📈 Estatísticas de Exemplo

Baseado no último teste realizado:
- **Taxa de sucesso**: ~80-90%
- **Músicas com ano identificado**: ~60-70%
- **Média de palavras por música**: ~150-200 palavras
- **Range de anos**: 1990-2025

## 🛠️ Tecnologias Utilizadas

- **Python 3.7+**
- **requests** - Para requisições HTTP
- **BeautifulSoup4** - Para parsing HTML
- **pandas** - Para manipulação de dados
- **unidecode** - Para normalização de texto

## ⚠️ Considerações Legais

Este projeto é para fins educacionais e de pesquisa. Respeite os termos de uso do site Letras.mus.br e use com moderação para não sobrecarregar os servidores.

## 📝 Trabalho Acadêmico

Desenvolvido como parte do trabalho prático de **Mestrado em KDD** (Knowledge Discovery in Databases), focando na coleta e análise de dados textuais da música popular brasileira.

---

⭐ **Se este projeto foi útil para sua pesquisa, considere dar uma estrela!**