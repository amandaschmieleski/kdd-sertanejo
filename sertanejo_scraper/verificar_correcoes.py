import pandas as pd

# Verificar qualidade dos dados corrigidos
df = pd.read_csv("letras_sertanejo_20250930_182159.csv")

print("🔍 VERIFICAÇÃO DOS DADOS CORRIGIDOS")
print("=" * 60)

print(f"📊 ESTRUTURA:")
print(f"   Músicas: {len(df)}")
print(f"   Artistas únicos: {df['artista'].nunique()}")

print(f"\n🎤 ARTISTAS:")
for artista in df['artista'].unique():
    count = (df['artista'] == artista).sum()
    print(f"   ✅ {artista}: {count} músicas")

print(f"\n📝 AMOSTRA DE LETRAS (primeiros 100 chars):")
for i, row in df.head(3).iterrows():
    letra_sample = row['letra'][:100].replace('\n', ' ')
    print(f"   {i+1}. {row['titulo']}: '{letra_sample}...'")

# Verificar se há palavras concatenadas
print(f"\n🔍 VERIFICAÇÃO DE CONCATENAÇÕES:")
problemas = []
for i, row in df.iterrows():
    letra = row['letra']
    # Procurar padrões comuns de concatenação
    import re
    concatenadas = re.findall(r'[a-z][ÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÃÇA-Z]', letra)
    if concatenadas:
        problemas.append((row['titulo'], concatenadas[:3]))  # Primeiras 3

if problemas:
    print(f"   ⚠️  Possíveis problemas encontrados:")
    for titulo, concatenadas in problemas[:3]:
        print(f"      - {titulo}: {concatenadas}")
else:
    print(f"   ✅ Nenhuma concatenação detectada!")

print(f"\n📈 ESTATÍSTICAS:")
print(f"   Palavras total: {df['contagem_palavras'].sum()}")
print(f"   Média palavras: {df['contagem_palavras'].mean():.1f}")
print(f"   Min-Max: {df['contagem_palavras'].min()}-{df['contagem_palavras'].max()}")

print("\n" + "=" * 60)
print("✅ Verificação concluída!")