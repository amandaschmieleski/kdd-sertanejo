#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste para descobrir quantas músicas realmente estão disponíveis
"""

import sys
sys.path.append('.')

from scraper_sertanejo import buscar_artista, obter_musicas_artista

print("🔍 INVESTIGANDO DISPONIBILIDADE DE MÚSICAS")
print("=" * 60)

artistas_teste = [
    "Chitãozinho e Xororó",
    "Bruno e Marrone"
]

for artista in artistas_teste:
    print(f"\n🎤 ARTISTA: {artista}")
    print("-" * 40)
    
    # Buscar URL do artista
    url_artista = buscar_artista(artista)
    if not url_artista:
        print(f"   ❌ Artista não encontrado")
        continue
    
    print(f"   🔗 URL encontrado: {url_artista}")
    
    # Obter TODAS as músicas (sem limite)
    musicas = obter_musicas_artista(url_artista, limite=None)
    
    if musicas:
        print(f"   📀 TOTAL DE MÚSICAS DISPONÍVEIS: {len(musicas)}")
        print(f"   📋 Primeiras 10 músicas:")
        
        for i, musica in enumerate(musicas[:10], 1):
            print(f"      {i:2d}. {musica['titulo']}")
        
        if len(musicas) > 10:
            print(f"      ... e mais {len(musicas) - 10} músicas")
    else:
        print(f"   ❌ Nenhuma música encontrada")

print(f"\n" + "=" * 60)
print("📊 CONCLUSÃO:")
print("   A limitação de 5 músicas é artificial - há muito mais disponível!")
print("   Podemos expandir para coletar mais músicas.")