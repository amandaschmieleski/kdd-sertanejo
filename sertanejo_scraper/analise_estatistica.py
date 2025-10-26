# ================================================================================
# ANÁLISE ESTATÍSTICA PRÉVIA DOS DADOS COLETADOS
# Análise descritiva do dataset de sertanejo moderno (2023+)
# ================================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from datetime import datetime
import os

def carregar_dados_mais_recente():
    """Carrega o arquivo mais recente de dados."""
    base_path = "../base_de_dados/"
    
    # Forçar o arquivo _3.csv que é o mais recente com 142 músicas
    arquivo_target = "sertanejo_mais_acessadas_2023+_3.csv"
    caminho_completo = os.path.join(base_path, arquivo_target)
    
    print(f"📂 Carregando: {arquivo_target}")
    
    try:
        df = pd.read_csv(caminho_completo, encoding='utf-8')
        print(f"✅ Arquivo carregado com sucesso! {len(df)} registros encontrados.")
        return df, arquivo_target
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo: {e}")
        
        # Fallback - tentar encontrar qualquer arquivo
        print("🔍 Procurando outros arquivos disponíveis...")
        arquivos = []
        if os.path.exists(base_path):
            for arquivo in os.listdir(base_path):
                if arquivo.startswith("sertanejo_mais_acessadas_2023+") and arquivo.endswith(".csv") and not arquivo.startswith(".~lock"):
                    try:
                        df_test = pd.read_csv(os.path.join(base_path, arquivo), encoding='utf-8')
                        arquivos.append((len(df_test), arquivo))
                    except:
                        continue
        
        if arquivos:
            # Pegar o arquivo com mais registros
            arquivos.sort(reverse=True)
            arquivo_maior = arquivos[0][1]
            print(f"📂 Usando arquivo com mais dados: {arquivo_maior}")
            df = pd.read_csv(os.path.join(base_path, arquivo_maior), encoding='utf-8')
            return df, arquivo_maior
        
        return None, None

def analisar_artistas(df):
    """Análise de artistas únicos e mais frequentes."""
    print("\n" + "="*60)
    print("🎤 ANÁLISE DE ARTISTAS")
    print("="*60)
    
    # Artistas únicos
    artistas_unicos = df['artista'].nunique()
    total_musicas = len(df)
    
    print(f"📊 Total de artistas únicos: {artistas_unicos}")
    print(f"🎵 Total de músicas: {total_musicas}")
    print(f"📈 Média de músicas por artista: {total_musicas/artistas_unicos:.1f}")
    
    # Top 10 artistas mais frequentes
    top_artistas = df['artista'].value_counts().head(10)
    print(f"\n🏆 TOP 10 ARTISTAS MAIS FREQUENTES:")
    for i, (artista, count) in enumerate(top_artistas.items(), 1):
        porcentagem = (count/total_musicas)*100
        print(f"   {i:2d}. {artista:<30} - {count:2d} músicas ({porcentagem:.1f}%)")
    
    return artistas_unicos, top_artistas

def analisar_anos(df):
    """Análise da distribuição por anos."""
    print("\n" + "="*60)
    print("📅 ANÁLISE TEMPORAL")
    print("="*60)
    
    # Filtrar apenas músicas com ano conhecido
    df_com_ano = df[df['ano'].notna()]
    df_sem_ano = df[df['ano'].isna()]
    
    print(f"📊 Músicas com ano identificado: {len(df_com_ano)} ({len(df_com_ano)/len(df)*100:.1f}%)")
    print(f"❓ Músicas sem ano: {len(df_sem_ano)} ({len(df_sem_ano)/len(df)*100:.1f}%)")
    
    if len(df_com_ano) > 0:
        anos_count = df_com_ano['ano'].value_counts().sort_index()
        print(f"\n📈 DISTRIBUIÇÃO POR ANO:")
        for ano, count in anos_count.items():
            porcentagem = (count/len(df_com_ano))*100
            print(f"   {int(ano)}: {count:2d} músicas ({porcentagem:.1f}%)")
        
        print(f"\n📊 ESTATÍSTICAS TEMPORAIS:")
        print(f"   Ano mais antigo: {int(df_com_ano['ano'].min())}")
        print(f"   Ano mais recente: {int(df_com_ano['ano'].max())}")
        print(f"   Ano médio: {df_com_ano['ano'].mean():.1f}")
    
    return df_com_ano, df_sem_ano

def analisar_palavras(df):
    """Análise da contagem de palavras e características textuais."""
    print("\n" + "="*60)
    print("📝 ANÁLISE TEXTUAL")
    print("="*60)
    
    total_palavras = df['contagem_palavras'].sum()
    media_palavras = df['contagem_palavras'].mean()
    mediana_palavras = df['contagem_palavras'].median()
    
    print(f"📊 ESTATÍSTICAS DE PALAVRAS:")
    print(f"   Total de palavras no dataset: {total_palavras:,}")
    print(f"   Média de palavras por música: {media_palavras:.0f}")
    print(f"   Mediana de palavras: {mediana_palavras:.0f}")
    print(f"   Mínimo de palavras: {df['contagem_palavras'].min()}")
    print(f"   Máximo de palavras: {df['contagem_palavras'].max()}")
    
    # Distribuição em faixas
    print(f"\n📈 DISTRIBUIÇÃO POR FAIXAS DE PALAVRAS:")
    faixas = [
        (0, 100, "Curtas"),
        (101, 200, "Médias"),
        (201, 300, "Longas"),
        (301, float('inf'), "Muito Longas")
    ]
    
    for min_val, max_val, categoria in faixas:
        if max_val == float('inf'):
            count = len(df[df['contagem_palavras'] > min_val])
        else:
            count = len(df[(df['contagem_palavras'] >= min_val) & (df['contagem_palavras'] <= max_val)])
        porcentagem = (count/len(df))*100
        print(f"   {categoria:<12} ({min_val:3d}-{max_val if max_val != float('inf') else '∞':>3}): {count:2d} músicas ({porcentagem:.1f}%)")
    
    # Top 5 músicas mais longas
    print(f"\n🏆 TOP 5 MÚSICAS MAIS LONGAS:")
    top_longas = df.nlargest(5, 'contagem_palavras')[['artista', 'titulo', 'contagem_palavras']]
    for i, (_, row) in enumerate(top_longas.iterrows(), 1):
        print(f"   {i}. {row['artista']} - {row['titulo']} ({row['contagem_palavras']} palavras)")
    
    return total_palavras, media_palavras

def analisar_letras_conteudo(df):
    """Análise do conteúdo das letras - palavras mais frequentes."""
    print("\n" + "="*60)
    print("🔤 ANÁLISE DE CONTEÚDO")
    print("="*60)
    
    # Juntar todas as letras
    todas_letras = ' '.join(df['letra'].astype(str))
    
    # Limpar e dividir em palavras
    palavras = re.findall(r'\b[a-záéíóúçãõâêôà]+\b', todas_letras.lower())
    
    # Palavras mais comuns (filtrar palavras muito curtas)
    palavras_filtradas = [p for p in palavras if len(p) >= 3]
    palavras_comuns = Counter(palavras_filtradas).most_common(15)
    
    print(f"📊 PALAVRAS MAIS FREQUENTES (mín. 3 letras):")
    for i, (palavra, freq) in enumerate(palavras_comuns, 1):
        print(f"   {i:2d}. {palavra:<15} - {freq:,} vezes")
    
    print(f"\n📈 ESTATÍSTICAS VOCABULÁRIO:")
    print(f"   Total de palavras únicas: {len(set(palavras_filtradas)):,}")
    print(f"   Total de palavras: {len(palavras_filtradas):,}")
    print(f"   Riqueza vocabular: {len(set(palavras_filtradas))/len(palavras_filtradas)*100:.1f}%")
    
    return palavras_comuns

def gerar_relatorio_resumo(df, arquivo_nome):
    """Gera um relatório resumo completo."""
    print("\n" + "="*60)
    print("📋 RELATÓRIO RESUMO")
    print("="*60)
    
    print(f"📂 Arquivo analisado: {arquivo_nome}")
    print(f"📅 Data da análise: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🎵 Total de músicas: {len(df)}")
    print(f"🎤 Artistas únicos: {df['artista'].nunique()}")
    print(f"📝 Total de palavras: {df['contagem_palavras'].sum():,}")
    print(f"📊 Média palavras/música: {df['contagem_palavras'].mean():.0f}")
    
    # Período coberto
    df_com_ano = df[df['ano'].notna()]
    if len(df_com_ano) > 0:
        print(f"📅 Período: {int(df_com_ano['ano'].min())} - {int(df_com_ano['ano'].max())}")
        print(f"🏷️  Músicas com ano: {len(df_com_ano)} ({len(df_com_ano)/len(df)*100:.1f}%)")
    
    # Artista mais prolífico
    top_artista = df['artista'].value_counts().iloc[0]
    nome_artista = df['artista'].value_counts().index[0]
    print(f"👑 Artista mais presente: {nome_artista} ({top_artista} músicas)")

def main():
    """Função principal da análise."""
    print("🚀 ANÁLISE ESTATÍSTICA - SERTANEJO MODERNO 2023+")
    print("="*60)
    
    # Carregar dados
    resultado = carregar_dados_mais_recente()
    if resultado[0] is None:
        return
    
    df, arquivo_nome = resultado
    
    # Executar análises
    print(f"\n✅ Dados carregados com sucesso! {len(df)} registros encontrados.")
    
    # Análises específicas
    analisar_artistas(df)
    analisar_anos(df)
    analisar_palavras(df)
    analisar_letras_conteudo(df)
    gerar_relatorio_resumo(df, arquivo_nome)
    
    print(f"\n🎯 ANÁLISE CONCLUÍDA!")
    print(f"💡 Os dados mostram uma boa diversidade de artistas e músicas modernas do sertanejo.")
    print(f"📊 Dataset pronto para análises mais profundas!")

if __name__ == "__main__":
    main()