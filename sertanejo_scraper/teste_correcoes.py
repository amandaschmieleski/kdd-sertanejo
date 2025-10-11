#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste das correções no scraper sertanejo
1. Teste do espaçamento entre palavras nas letras
2. Teste da correção do nome do artista
"""

import sys
sys.path.append('.')

from scraper_sertanejo import extrair_letra_musica

# URL de teste
url_teste = "https://www.letras.mus.br/chitaozinho-e-xororo/768469/"  # Evidências

print("🧪 TESTANDO CORREÇÕES DO SCRAPER")
print("=" * 60)

print(f"\n🔗 Testando URL: {url_teste}")
print(f"🎯 Música esperada: Evidências - Chitãozinho & Xororó")

# Testar com nome do artista fornecido
resultado = extrair_letra_musica(url_teste, "Chitãozinho & Xororó")

if resultado:
    print(f"\n✅ SUCESSO!")
    print(f"🎵 Título: {resultado['titulo']}")
    print(f"🎤 Artista: {resultado['artista']}")
    print(f"📊 Palavras: {resultado['contagem_palavras']}")
    print(f"📄 Linhas: {resultado['contagem_linhas']}")
    
    print(f"\n📝 INÍCIO DA LETRA (primeiros 200 caracteres):")
    letra_inicio = resultado['letra'][:200]
    print(f"'{letra_inicio}...'")
    
    # Verificar se não há palavras concatenadas
    print(f"\n🔍 VERIFICAÇÃO DE PALAVRAS CONCATENADAS:")
    
    # Procurar por padrões típicos de concatenação
    concatenacoes_encontradas = []
    
    # Padrões que indicam concatenação: maiúscula no meio da palavra
    import re
    palavras = resultado['letra'].split()
    
    for palavra in palavras[:20]:  # Verificar primeiras 20 palavras
        # Procurar por padrões como "amarÉ", "vocêÉ", etc.
        if re.search(r'[a-z][ÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÃ]', palavra):
            concatenacoes_encontradas.append(palavra)
    
    if concatenacoes_encontradas:
        print(f"   ⚠️  Possíveis concatenações encontradas:")
        for concat in concatenacoes_encontradas[:5]:
            print(f"      - '{concat}'")
    else:
        print(f"   ✅ Nenhuma concatenação óbvia detectada!")
    
    # Verificar problemas comuns específicos
    problemas_conhecidos = [
        ("amarÉ", "amar É"),
        ("vocêÉ", "você É"), 
        ("coraçãoE", "coração E"),
        ("mimSe", "mim Se")
    ]
    
    letra_lower = resultado['letra'].lower()
    print(f"\n🎯 VERIFICAÇÃO DE PROBLEMAS ESPECÍFICOS:")
    
    for problema, correcao in problemas_conhecidos:
        if problema.lower() in letra_lower:
            print(f"   ❌ Encontrado: '{problema}' (deveria ser '{correcao}')")
        else:
            print(f"   ✅ OK: '{problema}' não encontrado")
    
    print(f"\n📋 ESTATÍSTICAS:")
    print(f"   • Tamanho total: {len(resultado['letra'])} caracteres")
    print(f"   • Número de palavras: {len(resultado['letra'].split())}")
    print(f"   • Média caracteres/palavra: {len(resultado['letra']) / len(resultado['letra'].split()):.1f}")
    
else:
    print(f"\n❌ FALHA: Não foi possível extrair a letra")

print("\n" + "=" * 60)
print("Teste concluído!")