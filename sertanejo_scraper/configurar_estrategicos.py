#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuração equilibrada - 10 artistas estratégicos
"""

# Lista estratégica de 10 artistas para diversidade máxima
artistas_estrategicos = [
    # 2 do Sertanejo Moderno (mais populares)
    "Henrique & Juliano",
    "Jorge & Mateus",
    
    # 2 dos Clássicos/Icônicos  
    "Zezé Di Camargo & Luciano",
    "Leandro & Leonardo",
    
    # 2 do Feminino
    "Marília Mendonça",
    "Paula Fernandes",
    
    # 2 do Raiz/Tradicional
    "Milionário e José Rico", 
    "Almir Sater",
    
    # 2 da Nova Geração
    "Diego e Victor Hugo",
    "Gustavo Mioto"
]

print("🎯 CONFIGURAÇÃO ESTRATÉGICA - 10 ARTISTAS")
print("=" * 60)

print("📋 ARTISTAS SELECIONADOS:")
categorias_selecionadas = {
    "🔥 Sertanejo Moderno": ["Henrique & Juliano", "Jorge & Mateus"],
    "👑 Clássicos": ["Zezé Di Camargo & Luciano", "Leandro & Leonardo"], 
    "⭐ Feminino": ["Marília Mendonça", "Paula Fernandes"],
    "🎸 Raiz": ["Milionário e José Rico", "Almir Sater"],
    "🚀 Nova Geração": ["Diego e Victor Hugo", "Gustavo Mioto"]
}

for categoria, lista in categorias_selecionadas.items():
    print(f"\n{categoria}:")
    for artista in lista:
        print(f"   • {artista}")

print(f"\n📊 PROJEÇÃO DA COLETA:")
musicas_por_artista = 12
total_artistas = len(artistas_estrategicos)
total_musicas_novas = total_artistas * musicas_por_artista
musicas_atuais = 24  # Já temos

print(f"   📀 Artistas novos: {total_artistas}")
print(f"   🎵 Músicas por artista: {musicas_por_artista}")  
print(f"   📈 Músicas novas: {total_musicas_novas}")
print(f"   📊 Total final: {musicas_atuais} + {total_musicas_novas} = {musicas_atuais + total_musicas_novas} músicas")
print(f"   ⏱️ Tempo estimado: ~25-30 minutos")

print(f"\n💡 VANTAGENS DESTA SELEÇÃO:")
print(f"   ✅ Diversidade geracional (tradicional → moderno)")
print(f"   ✅ Representação feminina (20%)")
print(f"   ✅ Mix de estilos (raiz, moderno, clássico)")
print(f"   ✅ Artistas populares = maior disponibilidade de músicas")
print(f"   ✅ Base sólida para análise comparativa")

print(f"\n🚀 PRÓXIMO PASSO:")
print(f"   Implementar esta lista no scraper e executar coleta")

print("\n" + "=" * 60)