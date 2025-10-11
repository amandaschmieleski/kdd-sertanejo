#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Verificação da lista de artistas configurada
"""

# Lista exata do scraper
artistas = [
    # ============ JÁ COLETADOS (manter) ============
    "Chitãozinho e Xororó",
    "Bruno e Marrone", 
    "Henrique & Juliano",
    "Jorge & Mateus",
    "Zezé Di Camargo & Luciano",
    "Leandro & Leonardo",
    "Marília Mendonça",
    "Paula Fernandes",
    "Milionário e José Rico",
    "Almir Sater",
    "Diego e Victor Hugo",
    "Gustavo Mioto",
    
    # ============ EXPANSÃO MASSIVA ============
    # Sertanejo Moderno Top
    "Luan Santana",
    "Gusttavo Lima", 
    "Zé Neto e Cristiano",
    "Matheus & Kauan",
    
    # Feminino
    "Simone Mendes",
    "Ana Castela",
    "Lauana Prado",
    "Maiara & Maraisa",
    
    # Clássicos/Icônicos
    "Rick & Renner",
    "Victor & Leo",
    "Daniel",
    "Leonardo",
    "Chrystian & Ralf",
    
    # Nova Geração
    "Felipe Araújo",
    "Murilo Huff",
    "Zé Felipe",
    "Luan Pereira",
    
    # Raiz/Tradicional
    "Tião Carreiro e Pardinho",
    "Trio Parada Dura",
    "João Mineiro e Marciano",
    "Gino e Geno",
    "Sérgio Reis",
    "Tonico e Tinoco",
    "Teodoro e Sampaio",
    
    # Populares Diversos
    "Eduardo Costa",
    "Hugo & Guilherme",
    "Clayton e Romário",
    "Guilherme & Benuto",
    "Matogrosso & Mathias",
    "Ícaro e Gilmar",
    "Gian e Giovani",
    "Rionegro & Solimões",
    "João Paulo e Daniel",
    "Marcos & Belutti",
    "Lourenço e Lourival",
    "Edson & Hudson",
    "Chico Rey e Paraná",
    "Guilherme & Santiago"
]

print("🎤 VERIFICAÇÃO DA LISTA DE ARTISTAS")
print("=" * 60)

print(f"📊 ESTATÍSTICAS:")
print(f"   Total de artistas: {len(artistas)}")
print(f"   Já coletados: 12")
print(f"   Novos para coletar: {len(artistas) - 12}")

print(f"\n🎯 PROJEÇÃO DE COLETA:")
musicas_por_artista = 10
total_musicas = len(artistas) * musicas_por_artista
musicas_atuais = 144  # Já temos 12 artistas × 12 músicas

print(f"   📀 {len(artistas)} artistas × {musicas_por_artista} músicas = {total_musicas} músicas")
print(f"   📈 Crescimento: {musicas_atuais} → {total_musicas} (+{total_musicas - musicas_atuais})")
print(f"   📊 Aumento: {((total_musicas - musicas_atuais) / musicas_atuais * 100):.0f}%")

print(f"\n🎵 LISTA COMPLETA DOS ARTISTAS:")
for i, artista in enumerate(artistas, 1):
    status = "✅" if i <= 12 else "🆕"
    print(f"   {i:2d}. {status} {artista}")

print(f"\n⏱️ ESTIMATIVAS:")
print(f"   Tempo por artista: ~2-3 minutos")
print(f"   Tempo total: ~{len(artistas) * 2.5 / 60:.1f} horas")
print(f"   Palavras estimadas: ~{total_musicas * 200:,}")

print("\n" + "=" * 60)
print("✅ Lista configurada e pronta para coleta massiva!")