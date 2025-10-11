# ================================================================================
# PROJETO FUNK AI - CÓDIGO SEQUENCIAL COMPLETO
# Análise de Tópicos em Letras de Funk usando MariTalk
# Data: 25/09/2025
# ================================================================================

# ================================================================================
# 1. INSTALAÇÃO E IMPORTAÇÃO DE BIBLIOTECAS
# ================================================================================

# Instalação das bibliotecas necessárias (descomente se necessário)
# !pip install maritalk pandas numpy openpyxl

import pandas as pd
import numpy as np
import maritalk
import random
import os
import logging
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ================================================================================
# 2. CONFIGURAÇÃO DE LOGGING
# ================================================================================

# Configurar sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('funk_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ================================================================================
# 3. CONFIGURAÇÃO INICIAL E PARÂMETROS
# ================================================================================

def configurar_parametros():
    """Define os parâmetros principais do projeto"""
    
    parametros = {
        # Parâmetros de análise
        'num_iter': 10,          # Número de iterações para robustez
        'num_groups': 20,        # Número de grupos por iteração
        'num_topicos': 5,        # Número de tópicos a identificar
        
        # Configurações do modelo
        'temperature': 0.5,      # Controle de aleatoriedade
        'top_p': 0.95,          # Controle de diversidade
        'max_tokens': 200,       # Máximo de tokens na resposta
        
        # Caminhos de arquivos
        'repo_url': 'https://github.com/yepez26/SBBD2024_FUNK',
        'arquivo_dados': 'funk_lyrics.xlsx',
        'path_save': './resultados',
        
        # Configurações de API
        'maritalk_key': "",      # INSERIR CHAVE AQUI
    }
    
    # Criar dicionário auxiliar para montagem da base final
    parametros['aux_dic'] = {
        number: ['topics:'] for number in range(0, parametros['num_topicos'])
    }
    
    # Criar diretório de resultados se não existir
    os.makedirs(parametros['path_save'], exist_ok=True)
    
    logger.info("Parâmetros configurados com sucesso")
    return parametros

# ================================================================================
# 4. FUNÇÕES DE CARREGAMENTO DE DADOS
# ================================================================================

def clonar_repositorio_dados(repo_url):
    """Clona o repositório com os dados das músicas"""
    try:
        import subprocess
        
        # Verificar se o diretório já existe
        if os.path.exists('SBBD2024_FUNK'):
            logger.info("Repositório já existe, pulando clonagem")
            return True
            
        # Clonar repositório
        result = subprocess.run(['git', 'clone', repo_url], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("Repositório clonado com sucesso")
            return True
        else:
            logger.error(f"Erro ao clonar repositório: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Erro na clonagem: {str(e)}")
        return False

def carregar_dados(arquivo_dados):
    """Carrega e processa os dados das letras de funk"""
    try:
        # Mudar para diretório do repositório
        if os.path.exists('SBBD2024_FUNK'):
            os.chdir('SBBD2024_FUNK')
        
        # Carregar arquivo Excel
        data = pd.read_excel(arquivo_dados)
        logger.info(f"Dados carregados: {len(data)} registros")
        
        # Verificar estrutura dos dados
        logger.info(f"Colunas disponíveis: {list(data.columns)}")
        
        # Criar coluna 'trecho' se não existir (assumindo que seja 'ESTROFE' ou 'text')
        if 'trecho' not in data.columns:
            if 'ESTROFE' in data.columns:
                data['trecho'] = data['ESTROFE']
                logger.info("Coluna 'trecho' criada a partir de 'ESTROFE'")
            elif 'text' in data.columns:
                data['trecho'] = data['text']
                logger.info("Coluna 'trecho' criada a partir de 'text'")
            else:
                raise ValueError("Não foi possível identificar a coluna de trechos")
        
        # Limpar dados nulos
        data = data.dropna(subset=['trecho'])
        logger.info(f"Dados após limpeza: {len(data)} registros")
        
        return data
        
    except Exception as e:
        logger.error(f"Erro no carregamento de dados: {str(e)}")
        return None

# ================================================================================
# 5. CONFIGURAÇÃO DO MODELO MARITALK
# ================================================================================

def configurar_modelo_maritalk(maritalk_key):
    """Configura e testa o modelo MariTalk"""
    try:
        if not maritalk_key:
            raise ValueError("Chave da API MariTalk não fornecida")
        
        # Inicializar modelo
        model = maritalk.MariTalk(key=maritalk_key)
        logger.info("Modelo MariTalk configurado com sucesso")
        
        # Teste básico
        test_response = model.generate(
            "Teste de conexão. Responda apenas 'OK'.",
            do_sample=True,
            temperature=0.1,
            max_tokens=10
        )
        
        if test_response:
            logger.info("Teste de conexão com MariTalk: SUCESSO")
            return model
        else:
            raise Exception("Falha no teste de conexão")
            
    except Exception as e:
        logger.error(f"Erro na configuração do MariTalk: {str(e)}")
        return None

def criar_template_prompt(num_topicos):
    """Cria o template para o prompt do modelo"""
    template = f"dados os seguintes trechos de música, sugira {num_topicos} tópicos que descrevam os assuntos abordados: "
    return template

# ================================================================================
# 6. FUNÇÕES DE PROCESSAMENTO PRINCIPAL
# ================================================================================

def dividir_dados_em_grupos(data, num_groups, seed=None):
    """Divide os dados aleatoriamente em grupos"""
    try:
        if seed is not None:
            random.seed(seed)
        
        tamanho = len(data)
        list_sample = [random.randrange(0, num_groups) for _ in range(tamanho)]
        
        data_copy = data.copy()
        data_copy['sample'] = list_sample
        
        logger.info(f"Dados divididos em {num_groups} grupos")
        return data_copy
        
    except Exception as e:
        logger.error(f"Erro na divisão em grupos: {str(e)}")
        return None

def processar_grupo(data_grupo, model, template_base, parametros):
    """Processa um grupo específico de trechos"""
    try:
        # Extrair trechos do grupo
        lista_trechos = data_grupo['trecho'].tolist()
        
        if not lista_trechos:
            logger.warning("Grupo vazio encontrado")
            return None
        
        # Criar string com trechos
        string_trechos = [
            f'trecho {i}: {trecho}' 
            for i, trecho in enumerate(lista_trechos)
        ]
        string_trechos = '; '.join(string_trechos) + ' '
        
        # Montar prompt completo
        template_completo = template_base + string_trechos
        
        # Chamar modelo MariTalk
        answer = model.generate(
            template_completo,
            do_sample=True,
            temperature=parametros['temperature'],
            top_p=parametros['top_p'],
            max_tokens=parametros.get('max_tokens', 200)
        )
        
        if not answer:
            logger.warning("Resposta vazia do modelo")
            return None
        
        # Processar resposta
        list_answer = answer.split('\n')
        list_answer = list_answer[:parametros['num_topicos']]
        
        # Completar com tópicos padrão se necessário
        while len(list_answer) < parametros['num_topicos']:
            list_answer.append('sem_topico')
        
        # Criar DataFrame resultado
        df_resultado = pd.DataFrame()
        df_resultado['trechos'] = lista_trechos
        
        # Adicionar colunas de tópicos
        for col in parametros['aux_dic'].keys():
            df_resultado[col] = str(parametros['aux_dic'][col])
        
        for i in range(parametros['num_topicos']):
            df_resultado[i] = df_resultado[i] + str(list_answer[i])
        
        return df_resultado
        
    except Exception as e:
        logger.error(f"Erro no processamento do grupo: {str(e)}")
        return None

def executar_iteracao_completa(data, model, parametros, iteracao):
    """Executa uma iteração completa de análise"""
    try:
        logger.info(f"Iniciando iteração {iteracao + 1}/{parametros['num_iter']}")
        
        # Dividir dados em grupos
        seed = iteracao * 10
        data_grupos = dividir_dados_em_grupos(data, parametros['num_groups'], seed)
        
        if data_grupos is None:
            return None
        
        # Criar template base
        template_base = criar_template_prompt(parametros['num_topicos'])
        
        # DataFrame para resultado da iteração
        df_iteracao = pd.DataFrame()
        
        # Processar cada grupo
        grupos_processados = 0
        for grupo in range(parametros['num_groups']):
            # Filtrar dados do grupo
            data_grupo = data_grupos[data_grupos['sample'] == grupo]
            
            if len(data_grupo) == 0:
                logger.info(f"Grupo {grupo} vazio, pulando")
                continue
            
            # Processar grupo
            df_grupo = processar_grupo(data_grupo, model, template_base, parametros)
            
            if df_grupo is not None:
                df_iteracao = pd.concat([df_iteracao, df_grupo], ignore_index=True)
                grupos_processados += 1
                logger.info(f"Grupo {grupo} processado ({len(data_grupo)} trechos)")
        
        # Salvar resultado da iteração
        arquivo_saida = os.path.join(parametros['path_save'], f'base_topics_{iteracao}.xlsx')
        df_iteracao.to_excel(arquivo_saida, index=False)
        
        logger.info(f"Iteração {iteracao + 1} concluída: {grupos_processados} grupos processados")
        return df_iteracao
        
    except Exception as e:
        logger.error(f"Erro na iteração {iteracao}: {str(e)}")
        return None

# ================================================================================
# 7. FUNÇÃO PRINCIPAL DE EXECUÇÃO
# ================================================================================

def executar_analise_completa():
    """Executa todo o processo de análise de tópicos"""
    try:
        logger.info("=== INICIANDO ANÁLISE DE TÓPICOS EM LETRAS DE FUNK ===")
        inicio = datetime.now()
        
        # 1. Configurar parâmetros
        parametros = configurar_parametros()
        
        # 2. Verificar chave da API
        if not parametros['maritalk_key']:
            logger.error("ERRO: Chave da API MariTalk não configurada!")
            logger.info("Configure a chave na variável 'maritalk_key' nos parâmetros")
            return False
        
        # 3. Clonar repositório de dados
        if not clonar_repositorio_dados(parametros['repo_url']):
            return False
        
        # 4. Carregar dados
        data = carregar_dados(parametros['arquivo_dados'])
        if data is None:
            return False
        
        # 5. Configurar modelo
        model = configurar_modelo_maritalk(parametros['maritalk_key'])
        if model is None:
            return False
        
        # 6. Executar iterações
        lista_resultados = []
        
        for iteracao in range(parametros['num_iter']):
            resultado = executar_iteracao_completa(data, model, parametros, iteracao)
            
            if resultado is not None:
                lista_resultados.append(resultado)
            else:
                logger.warning(f"Iteração {iteracao + 1} falhou")
        
        # 7. Consolidar resultados
        if lista_resultados:
            df_consolidado = pd.concat(lista_resultados, ignore_index=True)
            arquivo_final = os.path.join(parametros['path_save'], 'analise_consolidada.xlsx')
            df_consolidado.to_excel(arquivo_final, index=False)
            
            logger.info(f"Análise consolidada salva em: {arquivo_final}")
            logger.info(f"Total de registros processados: {len(df_consolidado)}")
        
        # 8. Relatório final
        fim = datetime.now()
        tempo_total = fim - inicio
        
        logger.info("=== ANÁLISE CONCLUÍDA ===")
        logger.info(f"Tempo total: {tempo_total}")
        logger.info(f"Iterações realizadas: {len(lista_resultados)}/{parametros['num_iter']}")
        logger.info(f"Resultados salvos em: {parametros['path_save']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro na execução principal: {str(e)}")
        return False

# ================================================================================
# 8. FUNÇÕES AUXILIARES E UTILITÁRIOS
# ================================================================================

def gerar_relatorio_resultados(path_resultados='./resultados'):
    """Gera relatório estatístico dos resultados"""
    try:
        logger.info("Gerando relatório de resultados...")
        
        # Listar arquivos de resultado
        arquivos = [f for f in os.listdir(path_resultados) if f.endswith('.xlsx')]
        
        if not arquivos:
            logger.warning("Nenhum arquivo de resultado encontrado")
            return
        
        relatorio = {
            'total_arquivos': len(arquivos),
            'arquivos_iteracao': [f for f in arquivos if 'base_topics_' in f],
            'arquivo_consolidado': [f for f in arquivos if 'consolidada' in f]
        }
        
        # Estatísticas básicas
        if 'analise_consolidada.xlsx' in arquivos:
            df_consolidado = pd.read_excel(os.path.join(path_resultados, 'analise_consolidada.xlsx'))
            relatorio['total_registros'] = len(df_consolidado)
            relatorio['colunas_topicos'] = [col for col in df_consolidado.columns if isinstance(col, int)]
        
        logger.info(f"Relatório: {relatorio}")
        
        # Salvar relatório
        relatorio_path = os.path.join(path_resultados, 'relatorio_execucao.txt')
        with open(relatorio_path, 'w', encoding='utf-8') as f:
            f.write("=== RELATÓRIO DE EXECUÇÃO - FUNK AI ===\n\n")
            f.write(f"Data/Hora: {datetime.now()}\n")
            f.write(f"Total de arquivos gerados: {relatorio['total_arquivos']}\n")
            f.write(f"Arquivos de iteração: {len(relatorio['arquivos_iteracao'])}\n")
            f.write(f"Arquivo consolidado: {'Sim' if relatorio['arquivo_consolidado'] else 'Não'}\n")
            
            if 'total_registros' in relatorio:
                f.write(f"Total de registros processados: {relatorio['total_registros']}\n")
        
        logger.info(f"Relatório salvo em: {relatorio_path}")
        
    except Exception as e:
        logger.error(f"Erro na geração do relatório: {str(e)}")

def limpar_arquivos_temporarios():
    """Remove arquivos temporários e de cache"""
    try:
        import shutil
        
        # Remover repositório clonado
        if os.path.exists('SBBD2024_FUNK'):
            shutil.rmtree('SBBD2024_FUNK')
            logger.info("Repositório temporário removido")
        
        # Limpar cache Python
        cache_dirs = ['__pycache__', '.pytest_cache']
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
        
        logger.info("Limpeza de arquivos temporários concluída")
        
    except Exception as e:
        logger.error(f"Erro na limpeza: {str(e)}")

# ================================================================================
# 9. CONFIGURAÇÕES DE EXECUÇÃO
# ================================================================================

def configurar_ambiente_google_colab():
    """Configurações específicas para Google Colab"""
    try:
        # Verificar se está rodando no Colab
        import google.colab
        
        # Montar Google Drive
        from google.colab import drive
        drive.mount('/content/drive')
        
        # Mudar para diretório do projeto
        os.chdir('/content/drive/MyDrive/funk_ai')
        
        logger.info("Ambiente Google Colab configurado")
        return True
        
    except ImportError:
        logger.info("Não está rodando no Google Colab")
        return False
    except Exception as e:
        logger.error(f"Erro na configuração do Colab: {str(e)}")
        return False

# ================================================================================
# 10. EXECUÇÃO PRINCIPAL
# ================================================================================

if __name__ == "__main__":
    """Ponto de entrada principal do programa"""
    
    print("=" * 80)
    print("PROJETO FUNK AI - ANÁLISE DE TÓPICOS EM LETRAS DE FUNK")
    print("=" * 80)
    
    # Configurar ambiente se necessário
    configurar_ambiente_google_colab()
    
    # Executar análise principal
    sucesso = executar_analise_completa()
    
    if sucesso:
        # Gerar relatório final
        gerar_relatorio_resultados()
        
        print("\n" + "=" * 80)
        print("EXECUÇÃO CONCLUÍDA COM SUCESSO!")
        print("Verifique os resultados na pasta './resultados'")
        print("=" * 80)
        
        # Opcionalmente limpar arquivos temporários
        # limpar_arquivos_temporarios()
        
    else:
        print("\n" + "=" * 80)
        print("EXECUÇÃO FALHOU!")
        print("Verifique os logs para mais detalhes")
        print("=" * 80)

# ================================================================================
# INSTRUÇÕES DE USO:
# ================================================================================
"""
INSTRUÇÕES PARA EXECUÇÃO:

1. CONFIGURAÇÃO INICIAL:
   - Instale as dependências: pip install maritalk pandas numpy openpyxl
   - Configure sua chave da API MariTalk na variável 'maritalk_key'

2. EXECUÇÃO:
   - Execute este arquivo: python codigo_sequencial.py
   - Os resultados serão salvos na pasta './resultados'

3. PERSONALIZAÇÃO:
   - Modifique os parâmetros na função 'configurar_parametros()'
   - Ajuste o número de iterações, grupos e tópicos conforme necessário

4. MONITORAMENTO:
   - Acompanhe o progresso através dos logs no console
   - Um arquivo de log será criado: 'funk_analysis.log'

5. RESULTADOS:
   - Arquivos individuais por iteração: 'base_topics_X.xlsx'
   - Arquivo consolidado: 'analise_consolidada.xlsx'
   - Relatório de execução: 'relatorio_execucao.txt'

OBSERVAÇÕES:
- O código está preparado para Google Colab e ambiente local
- Certifique-se de ter uma conexão estável com a internet
- A execução pode demorar dependendo do volume de dados
"""