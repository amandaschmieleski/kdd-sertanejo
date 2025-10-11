#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste final com coleta completa para validar as correções
"""

import sys
sys.path.append('.')

from scraper_sertanejo import fazer_scraping_artista
import json

print("🧪 TESTE FINAL - COLETA COMPLETA")
print("=" * 60)

# Testar com um artista e poucas músicas
artista_teste = "Chitãozinho & Xororó"
max_musicas = 2

print(f"🎯 Coletando {max_musicas} músicas de: {artista_teste}")

letras = fazer_scraping_artista(artista_teste, max_musicas)

if letras:
    print(f"\n✅ COLETA CONCLUÍDA: {len(letras)} músicas")
    
    for i, musica in enumerate(letras, 1):
        print(f"\n📀 MÚSICA {i}:")
        print(f"   🎵 Título: {musica['titulo']}")
        print(f"   🎤 Artista: {musica['artista']}")
        print(f"   📊 Palavras: {musica['contagem_palavras']}")
        print(f"   🔗 URL: {musica['url']}")
        
        # Mostrar início da letra
        letra_preview = musica['letra'][:150]
        print(f"   📝 Início: {letra_preview}...")
        
        # Verificar qualidade
        if " É " in musica['letra'] and " E " in musica['letra']:
            print(f"   ✅ Espaçamento correto detectado")
        else:
            print(f"   ⚠️  Verificar espaçamento")
    
    # Salvar resultado de teste
    with open('teste_resultado.json', 'w', encoding='utf-8') as f:
        json.dump(letras, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Resultado salvo em: teste_resultado.json")
    
else:
    print(f"\n❌ FALHA na coleta")

print("\n" + "=" * 60)