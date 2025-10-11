# ================================================================================
# ANÁLISE DE MÚSICAS MODERNAS (2023+)
# Analisa a base atual para identificar padrões e estratégias de expansão
# ================================================================================

import pandas as pd
from datetime import datetime

def analisar_base_moderna():
    """Analisa as músicas de 2023+ na base atual."""
    
    print("🎯 ANÁLISE DE MÚSICAS MODERNAS (2023+)")
    print("=" * 60)
    
    # Carregar dados
    df = pd.read_csv('letras_sertanejo_com_anos_20250930_195644.csv')
    
    # Filtrar músicas com ano
    df_com_ano = df[df['ano'].notna()].copy()
    
    # Filtrar músicas 2023+
    df_modernas = df_com_ano[df_com_ano['ano'] >= 2023].copy()
    
    print(f"📊 ESTATÍSTICAS GERAIS:")
    print(f"   Total de músicas: {len(df)}")
    print(f"   Músicas com ano: {len(df_com_ano)}")
    print(f"   Músicas 2023+: {len(df_modernas)}")
    print(f"   Porcentagem moderna: {(len(df_modernas)/len(df_com_ano)*100):.1f}%")
    
    # Distribuição por ano
    print(f"\n📅 DISTRIBUIÇÃO POR ANO (2023+):")
    distribuicao_anos = df_modernas['ano'].value_counts().sort_index()
    for ano, count in distribuicao_anos.items():
        print(f"   {int(ano)}: {count} músicas")
    
    # Top artistas modernos
    print(f"\n🎤 TOP ARTISTAS COM MÚSICAS 2023+:")
    artistas_modernos = df_modernas['artista'].value_counts()
    for artista, count in artistas_modernos.head(10).items():
        print(f"   {artista}: {count} músicas")
    
    # Análise de palavras
    total_palavras_modernas = df_modernas['contagem_palavras'].sum()
    media_palavras = df_modernas['contagem_palavras'].mean()
    
    print(f"\n📝 ANÁLISE DE CONTEÚDO:")
    print(f"   Total de palavras: {total_palavras_modernas:,}")
    print(f"   Média por música: {media_palavras:.0f} palavras")
    
    # Músicas mais longas
    print(f"\n📏 TOP 5 MÚSICAS MAIS LONGAS (2023+):")
    top_longas = df_modernas.nlargest(5, 'contagem_palavras')
    for _, row in top_longas.iterrows():
        print(f"   {row['artista']} - {row['titulo']} ({int(row['contagem_palavras'])} palavras, {int(row['ano'])})")
    
    # Estratégia de expansão
    print(f"\n💡 ESTRATÉGIA DE EXPANSÃO:")
    
    # Calcular déficit
    meta = 1000
    deficit = meta - len(df_modernas)
    
    print(f"   Meta: {meta} músicas")
    print(f"   Atual: {len(df_modernas)} músicas")
    print(f"   Déficit: {deficit} músicas")
    
    # Estimativas
    if len(artistas_modernos) > 0:
        media_por_artista = len(df_modernas) / len(artistas_modernos)
        artistas_necessarios = int(deficit / media_por_artista) + 10
        
        print(f"   Média atual: {media_por_artista:.1f} músicas/artista")
        print(f"   Novos artistas estimados: ~{artistas_necessarios}")
    
    # Salvar análise das músicas modernas
    arquivo_modernas = f"musicas_modernas_2023+_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df_modernas.to_csv(arquivo_modernas, index=False, encoding='utf-8')
    print(f"\n💾 Músicas 2023+ salvas em: {arquivo_modernas}")
    
    return df_modernas, artistas_modernos

def identificar_artistas_estrategicos():
    """Identifica artistas que devemos focar para expansão."""
    
    print(f"\n🎯 IDENTIFICAÇÃO DE ARTISTAS ESTRATÉGICOS")
    print("-" * 60)
    
    # Lista de artistas sertanejos modernos populares
    artistas_estrategicos = [
        # Duplas consolidadas com hits recentes
        "Henrique & Juliano", "Jorge & Mateus", "Matheus & Kauan",
        "Hugo & Guilherme", "Guilherme & Benuto", "Marcos & Belutti",
        
        # Solos modernos
        "Gusttavo Lima", "Luan Santana", "Gustavo Mioto", "Murilo Huff",
        "Felipe Araújo", "Eduardo Costa", "Zé Felipe", "Luan Pereira",
        
        # Feminino
        "Marília Mendonça", "Maiara & Maraisa", "Simone Mendes",
        "Ana Castela", "Lauana Prado", "Paula Fernandes",
        
        # Novos talentos e emergentes
        "Clayton e Romário", "Diego e Victor Hugo", "João Gustavo e Murilo",
        "Ryan e Ruan", "Fred e Gustavo", "Brenno & Matheus",
        "Pedro Henrique & Fernando", "Cristiano Araújo", "Thiago Freitas",
        
        # Colaboradores frequentes
        "Zé Neto & Cristiano", "Israel & Rodolffo", "Antony & Gabriel",
        "Rafa & Pipo Marques", "George Henrique & Rodrigo", "João Bosco & Vinícius",
        
        # Sertanejo universitário
        "Wesley Safadão", "Gabriel Diniz", "Xand Avião", "Jonas Esticado"
    ]
    
    print(f"📋 Lista estratégica base: {len(artistas_estrategicos)} artistas")
    
    # Artistas que ainda não exploramos ou precisamos expandir
    artistas_novos = [
        "Anitta", "Ludmilla", "IZA", "Luísa Sonza",  # Pop/Sertanejo crossover
        "Mari Fernandez", "Tarcísio do Acordeon", "João Gomes",  # Forró/Sertanejo
        "Zé Vaqueiro", "Eric Land", "Pisadinha de Luxo",
        "MC Ryan SP", "MC Hariel", "MC Daniel",  # Sertanejo/Funk fusion
        "Dennis DJ", "Kevin o Chris", "MC Kevinho"
    ]
    
    print(f"🆕 Artistas novos/crossover: {len(artistas_novos)} artistas")
    
    # Combinar listas
    lista_expandida = artistas_estrategicos + artistas_novos
    
    print(f"🎯 TOTAL DE ARTISTAS PARA EXPANSÃO: {len(lista_expandida)}")
    print(f"📈 Estimativa conservadora: {len(lista_expandida) * 8} músicas")
    print(f"📈 Estimativa otimista: {len(lista_expandida) * 15} músicas")
    
    return lista_expandida

if __name__ == "__main__":
    print("🚀 Iniciando análise de base moderna...")
    
    # Analisar base atual
    df_modernas, artistas_atuais = analisar_base_moderna()
    
    # Identificar estratégia de expansão
    lista_expandida = identificar_artistas_estrategicos()
    
    print(f"\n" + "=" * 60)
    print(f"✅ ANÁLISE CONCLUÍDA")
    print(f"   Base atual: {len(df_modernas)} músicas 2023+")
    print(f"   Artistas estratégicos: {len(lista_expandida)}")
    print(f"   Próximo passo: Implementar scraper otimizado")