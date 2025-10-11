# Análise de Tópicos em Letras de Funk

Este projeto realiza a análise de tópicos em letras de música funk utilizando processamento de linguagem natural através do modelo MariTalk.

## Estrutura do Projeto

```
funk_ai/
    ├── identificacao_topicos.ipynb    # Notebook principal de análise
    ├── scapper.ipynb                  # Notebook de configuração do repositório
    ├── excerpts_analysis.xlsx         # Arquivo de análise dos trechos
    └── funk_lyrics_estrofes_1000.xlsx # Base de dados com letras de funk
```

## Detalhamento dos Notebooks

### identificacao_topicos.ipynb

Este é o notebook principal onde acontece a análise dos tópicos. Aqui está o passo a passo do que o código faz:

1. **Configuração Inicial**
   - Instalação do pacote `maritalk`
   - Importação das bibliotecas necessárias (pandas, numpy, maritalk)

2. **Carregamento dos Dados**
   - Clona o repositório SBBD2024_FUNK
   - Carrega o arquivo 'funk_lyrics.xlsx' usando pandas

3. **Definição de Parâmetros**
   - `num_iter = 10`: Número de vezes que a análise será repetida
   - `num_groups = 20`: Número de grupos diferentes em cada iteração
   - `num_topicos = 5`: Número de tópicos a serem identificados
   - Cria um dicionário auxiliar para armazenar os tópicos

4. **Configuração do Modelo**
   - Inicializa o modelo MariTalk
   - Define o template para a pergunta que será feita ao modelo

5. **Processo de Análise**
   Para cada iteração (num_iter):
   - Gera uma semente aleatória baseada na iteração
   - Divide os trechos em grupos aleatórios
   - Para cada grupo (num_groups):
     - Filtra as músicas do grupo
     - Cria uma string com os trechos
     - Gera tópicos usando o MariTalk
     - Processa e armazena as respostas

### scapper.ipynb

Este notebook é focado na configuração do ambiente e controle de versão:

1. **Configuração do Google Drive**
   - Monta o Google Drive
   - Configura as credenciais do Git

2. **Configuração do Repositório**
   - Inicializa um repositório Git
   - Configura usuário e email
   - Adiciona o repositório remoto
   - Configura a branch principal

## Arquivos de Dados

1. **funk_lyrics_estrofes_1000.xlsx**
   - Contém a base de dados principal
   - Armazena 1000 estrofes de músicas funk

2. **excerpts_analysis.xlsx**
   - Arquivo para análise dos trechos
   - Contém os resultados das análises

## Fluxo de Execução

1. Os dados são carregados do arquivo Excel
2. Os trechos são divididos aleatoriamente em grupos
3. Cada grupo é processado pelo modelo MariTalk
4. O modelo identifica 5 tópicos principais para cada grupo
5. O processo é repetido 10 vezes para maior robustez
6. Os resultados são armazenados em DataFrames

## Requisitos

- Python
- Bibliotecas:
  - maritalk
  - pandas
  - numpy
- Conta no Google Colab (recomendado para execução)
- Chave API do MariTalk

## Observações

- O projeto foi desenvolvido para ser executado no Google Colab
- É necessário uma chave API válida do MariTalk para execução
- Os resultados podem variar devido à natureza aleatória da divisão dos grupos