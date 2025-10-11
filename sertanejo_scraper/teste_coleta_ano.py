# ================================================================================
# TESTE RÁPIDO DE COLETA COM ANO
# Testa a função melhorada em um pequeno conjunto de músicas
# ================================================================================

import sys
import os

# Adicionar o diretório atual ao path para importar do scraper principal
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar funções do scraper principal
from scraper_sertanejo import fazer_scraping_artista, extrair_letra_musica, buscar_artista, obter_musicas_artista
import pandas as pd
from datetime import datetime

def testar_coleta_com_ano():
    """Testa a coleta de algumas músicas para verificar se o ano está sendo capturado."""
    
    print("🎵 Testando coleta com extração de ano melhorada")
    print("=" * 60)
    
    # Testar com um artista específico - pegar só 3 músicas
    nome_artista = "Henrique e Juliano"
    
    print(f"🎤 Testando com artista: {nome_artista}")
    print("⏳ Coletando algumas músicas...")
    
    # Fazer scraping com limite pequeno para teste
    musicas = fazer_scraping_artista(nome_artista, max_musicas=3)
    
    if not musicas:
        print("❌ Nenhuma música coletada")
        return
    
    print(f"\n✅ Coletadas {len(musicas)} músicas")
    print("\n📋 Resultados:")
    print("-" * 60)
    
    for i, musica in enumerate(musicas, 1):
        print(f"{i}. {musica['artista']} - {musica['titulo']}")
        print(f"   📅 Ano: {musica['ano'] if musica['ano'] else 'Não encontrado'}")
        print(f"   📝 Palavras: {musica['contagem_palavras']}")
        print(f"   🔗 URL: {musica['url']}")
        print()
    
    # Estatísticas
    musicas_com_ano = [m for m in musicas if m['ano']]
    porcentagem = (len(musicas_com_ano) / len(musicas)) * 100
    
    print(f"📊 Estatísticas do teste:")
    print(f"   Total de músicas: {len(musicas)}")
    print(f"   Músicas com ano: {len(musicas_com_ano)}")
    print(f"   Porcentagem de sucesso: {porcentagem:.1f}%")
    
    if musicas_com_ano:
        anos = [m['ano'] for m in musicas_com_ano]
        print(f"   Anos encontrados: {sorted(set(anos))}")
    
    # Salvar dados de teste em CSV para verificação
    df = pd.DataFrame(musicas)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    arquivo_teste = f"teste_ano_{timestamp}.csv"
    df.to_csv(arquivo_teste, index=False, encoding='utf-8')
    
    print(f"\n💾 Dados salvos em: {arquivo_teste}")
    
    return musicas

if __name__ == "__main__":
    testar_coleta_com_ano()