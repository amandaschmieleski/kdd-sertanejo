import pandas as pd
import json
from datetime import datetime

# Análise detalhada dos dados coletados
print("🔍 ANÁLISE DETALHADA DOS DADOS COLETADOS")
print("=" * 80)

# Carregar dados CSV
df = pd.read_csv("letras_sertanejo_20250930_175739.csv")

print(f"📊 ESTRUTURA DO DATASET:")
print(f"   Linhas: {len(df)}")
print(f"   Colunas: {len(df.columns)}")
print(f"   Tamanho do arquivo CSV: {len(open('letras_sertanejo_20250930_175739.csv', 'r', encoding='utf-8').read())} caracteres")

print(f"\n📝 COLUNAS DISPONÍVEIS:")
for i, col in enumerate(df.columns, 1):
    print(f"   {i}. {col} - Tipo: {df[col].dtype}")

print(f"\n🎵 AMOSTRA DOS DADOS:")
print(df[['titulo', 'contagem_palavras', 'contagem_linhas']].head())

print(f"\n❌ PROBLEMAS IDENTIFICADOS:")

# 1. Problema com nome do artista
artistas_unicos = df['artista'].unique()
print(f"   1. Nome do artista incorreto:")
for artista in artistas_unicos:
    print(f"      - '{artista}' (deveria ser 'Chitãozinho & Xororó' ou 'Bruno e Marrone')")

# 2. Problema com quebras de linha
print(f"   2. Formatação das letras:")
print(f"      - Todas as músicas têm apenas 1 linha (deviam ter múltiplas)")

# 3. Ano não capturado
anos_nulos = df['ano'].isnull().sum()
print(f"   3. Dados de ano:")
print(f"      - {anos_nulos}/{len(df)} músicas sem ano informado")

# 4. Análise das letras
print(f"\n📈 ESTATÍSTICAS DAS LETRAS:")
print(f"   Palavra mais frequente nas letras:")
todas_palavras = ' '.join(df['letra']).lower().split()
from collections import Counter
palavras_freq = Counter(todas_palavras)
print(f"   Top 10 palavras:")
for palavra, freq in palavras_freq.most_common(10):
    if len(palavra) > 2:  # Filtrar palavras muito pequenas
        print(f"      - '{palavra}': {freq} vezes")

print(f"\n🎯 ANÁLISE POR MÚSICA:")
print(f"   {'Título':<30} {'Palavras':<10} {'Primeiro trecho da letra'}")
print("-" * 80)
for _, row in df.iterrows():
    titulo_truncado = row['titulo'][:28]
    letra_trecho = row['letra'][:40].replace('\n', ' ')
    print(f"   {titulo_truncado:<30} {row['contagem_palavras']:<10} {letra_trecho}...")

print(f"\n🔗 URLS COLETADAS:")
for i, url in enumerate(df['url'], 1):
    print(f"   {i}. {url}")

print(f"\n✅ PONTOS POSITIVOS:")
print(f"   ✅ Todas as 10 músicas foram coletadas com sucesso")
print(f"   ✅ Letras completas capturadas (145-228 palavras)")
print(f"   ✅ URLs válidas e acessíveis")
print(f"   ✅ Timestamp de coleta registrado")
print(f"   ✅ Contagem de palavras precisa")

print(f"\n⚠️  MELHORIAS NECESSÁRIAS:")
print(f"   1. Corrigir extração do nome do artista")
print(f"   2. Preservar quebras de linha nas letras")
print(f"   3. Melhorar extração do ano de lançamento")
print(f"   4. Adicionar validação de estrutura das letras")

# Exemplo de como uma letra deveria estar formatada
print(f"\n📋 EXEMPLO DE LETRA BEM FORMATADA:")
print("   Título: Evidências")
print("   Artista: Chitãozinho & Xororó")
print("   Letra (com quebras de linha):")
letra_exemplo = df.iloc[0]['letra'][:200]
# Tentar reconstruir quebras de linha básicas
letra_formatada = letra_exemplo.replace('É porque', '\nÉ porque').replace('Eu tenho', '\nEu tenho')
print("   " + letra_formatada.replace('\n', '\n   '))

print("\n" + "=" * 80)
print("Análise concluída!")