# ================================================================================
# LISTA EXPANDIDA DE ARTISTAS SERTANEJOS MODERNOS
# Lista abrangente com 60+ artistas focados em lançamentos 2023+
# ================================================================================

def criar_lista_artistas_expandida():
    """Cria lista abrangente de artistas sertanejos para coleta moderna."""
    
    print("🎯 CRIANDO LISTA EXPANDIDA DE ARTISTAS SERTANEJOS")
    print("=" * 70)
    
    # Categoria 1: Duplas consolidadas (sempre lançando)
    duplas_consolidadas = [
        "Henrique & Juliano", "Jorge & Mateus", "Matheus & Kauan",
        "Zé Neto & Cristiano", "Hugo & Guilherme", "Guilherme & Benuto",
        "Marcos & Belutti", "Israel & Rodolffo", "João Bosco & Vinícius",
        "Clayton e Romário", "Pedro Henrique & Fernando", "George Henrique & Rodrigo",
        "Antony & Gabriel", "Ryan e Ruan", "Fred e Gustavo", "Brenno & Matheus"
    ]
    
    # Categoria 2: Solos masculinos populares
    solos_masculinos = [
        "Gusttavo Lima", "Luan Santana", "Gustavo Mioto", "Murilo Huff",
        "Felipe Araújo", "Eduardo Costa", "Zé Felipe", "Luan Pereira",
        "Wesley Safadão", "Gabriel Diniz", "Jonas Esticado", "Thiago Freitas",
        "João Gomes", "Tarcísio do Acordeon", "Zé Vaqueiro", "Eric Land"
    ]
    
    # Categoria 3: Artistas femininas e duplas femininas
    femininas = [
        "Marília Mendonça", "Maiara & Maraisa", "Simone Mendes", "Ana Castela",
        "Lauana Prado", "Paula Fernandes", "Mari Fernandez", "Naiara Azevedo",
        "Roberta Miranda", "Elba Ramalho", "Fabiana Cantilo", "Gabi Martins",
        "Yasmin Santos", "Racyne e Rafael", "Duda Beat", "Luísa Sonza"
    ]
    
    # Categoria 4: Novos talentos e emergentes (2022-2025)
    novos_talentos = [
        "João Gustavo e Murilo", "Rafa & Pipo Marques", "Diego e Victor Hugo",
        "Brenno & Matheus", "Fiduma & Jeca", "Conrado & Aleksandro",
        "Léo & Raphael", "Ícaro e Gilmar", "Lucas & Higor", "Bruno & Denner",
        "Zé Ricardo & Thiago", "Kleo Dibah", "Rayane & Rafaela", "Israel Novaes"
    ]
    
    # Categoria 5: Crossover e fusão (Sertanejo + outros gêneros)
    crossover = [
        "Anitta", "Ludmilla", "IZA", "MC Hariel", "MC Daniel", "MC Ryan SP",
        "Kevin o Chris", "Dennis DJ", "Pabllo Vittar", "Gloria Groove",
        "Vitão", "Ferrugem", "Thiaguinho", "Péricles"
    ]
    
    # Categoria 6: Veteranos ainda ativos
    veteranos_ativos = [
        "Leonardo", "Daniel", "Sérgio Reis", "Chitãozinho e Xororó",
        "Bruno e Marrone", "Zezé Di Camargo & Luciano", "Leandro & Leonardo",
        "Victor & Leo", "Edson & Hudson", "Rick & Renner"
    ]
    
    # Combinar todas as categorias
    todos_artistas = (duplas_consolidadas + solos_masculinos + femininas + 
                     novos_talentos + crossover + veteranos_ativos)
    
    # Remover duplicatas mantendo ordem
    artistas_unicos = []
    for artista in todos_artistas:
        if artista not in artistas_unicos:
            artistas_unicos.append(artista)
    
    print(f"📊 ESTATÍSTICAS POR CATEGORIA:")
    print(f"   🎭 Duplas consolidadas: {len(duplas_consolidadas)}")
    print(f"   🎤 Solos masculinos: {len(solos_masculinos)}")
    print(f"   👩‍🎤 Femininas: {len(femininas)}")
    print(f"   🌟 Novos talentos: {len(novos_talentos)}")
    print(f"   🔀 Crossover: {len(crossover)}")
    print(f"   🏆 Veteranos ativos: {len(veteranos_ativos)}")
    print(f"   📈 TOTAL ÚNICO: {len(artistas_unicos)} artistas")
    
    return artistas_unicos

def estimar_coleta_moderna(artistas):
    """Estima quantas músicas 2023+ conseguiremos coletar."""
    
    print(f"\n💡 ESTIMATIVAS DE COLETA MODERNA")
    print("-" * 50)
    
    # Estimativas baseadas em perfis diferentes
    estimativas = {
        "Novos talentos (20 artistas)": {"artistas": 20, "musicas_por_artista": 15, "taxa_2023": 0.8},
        "Duplas consolidadas (20 artistas)": {"artistas": 20, "musicas_por_artista": 12, "taxa_2023": 0.6},
        "Solos populares (15 artistas)": {"artistas": 15, "musicas_por_artista": 18, "taxa_2023": 0.7},
        "Femininas (15 artistas)": {"artistas": 15, "musicas_por_artista": 14, "taxa_2023": 0.75},
        "Crossover (10 artistas)": {"artistas": 10, "musicas_por_artista": 10, "taxa_2023": 0.9}
    }
    
    total_musicas_2023 = 0
    
    for categoria, dados in estimativas.items():
        musicas_categoria = dados["artistas"] * dados["musicas_por_artista"]
        musicas_2023_categoria = int(musicas_categoria * dados["taxa_2023"])
        total_musicas_2023 += musicas_2023_categoria
        
        print(f"   {categoria}:")
        print(f"      Total músicas: {musicas_categoria}")
        print(f"      Músicas 2023+: {musicas_2023_categoria}")
    
    print(f"\n🎯 ESTIMATIVA TOTAL:")
    print(f"   Total de artistas: {len(artistas)}")
    print(f"   Músicas 2023+ estimadas: {total_musicas_2023}")
    print(f"   Meta de 1000: {'✅ VIÁVEL' if total_musicas_2023 >= 1000 else '⚠️ AJUSTAR'}")
    
    return total_musicas_2023

def salvar_lista_artistas(artistas):
    """Salva a lista de artistas em arquivo para uso no scraper."""
    
    from datetime import datetime
    
    # Salvar em formato Python
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    arquivo_py = f"lista_artistas_modernos_{timestamp}.py"
    
    with open(arquivo_py, 'w', encoding='utf-8') as f:
        f.write("# Lista de artistas para coleta de músicas modernas (2023+)\n")
        f.write("# Gerada automaticamente\n\n")
        f.write("ARTISTAS_MODERNOS = [\n")
        for artista in artistas:
            f.write(f'    "{artista}",\n')
        f.write("]\n\n")
        f.write(f"# Total: {len(artistas)} artistas\n")
    
    print(f"💾 Lista salva em: {arquivo_py}")
    
    # Também salvar em CSV simples
    import pandas as pd
    df_artistas = pd.DataFrame({'artista': artistas})
    arquivo_csv = arquivo_py.replace('.py', '.csv')
    df_artistas.to_csv(arquivo_csv, index=False, encoding='utf-8')
    print(f"💾 CSV salvo em: {arquivo_csv}")
    
    return arquivo_py

if __name__ == "__main__":
    print("🚀 Criando lista expandida de artistas sertanejos modernos...")
    
    # Criar lista expandida
    artistas = criar_lista_artistas_expandida()
    
    # Estimar coleta
    estimativa = estimar_coleta_moderna(artistas)
    
    # Salvar lista
    arquivo = salvar_lista_artistas(artistas)
    
    print(f"\n" + "=" * 70)
    print(f"✅ LISTA EXPANDIDA CRIADA")
    print(f"   📊 Total de artistas: {len(artistas)}")
    print(f"   🎯 Estimativa 2023+: {estimativa} músicas")
    print(f"   📁 Arquivo: {arquivo}")
    print(f"   🚀 Próximo: Criar scraper otimizado para músicas recentes")