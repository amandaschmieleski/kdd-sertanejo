#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuração expandida para coleta de mais dados
"""

print("🚀 CONFIGURAÇÕES PARA EXPANSÃO DA BASE DE DADOS")
print("=" * 60)

print("""
📊 SITUAÇÃO ATUAL:
   ✅ Chitãozinho e Xororó: 612 músicas disponíveis
   ✅ Bruno e Marrone: 608 músicas disponíveis  
   📝 Coletamos apenas: 5 + 5 = 10 músicas

🎯 OPÇÕES DE EXPANSÃO:
""")

opcoes = [
    {
        "nome": "Conservadora",
        "musicas_por_artista": 20,
        "total_musicas": 40,
        "tempo_estimado": "~5 minutos",
        "descrição": "Boa amostra representativa"
    },
    {
        "nome": "Moderada", 
        "musicas_por_artista": 50,
        "total_musicas": 100,
        "tempo_estimado": "~15 minutos", 
        "descrição": "Base sólida para análise"
    },
    {
        "nome": "Agressiva",
        "musicas_por_artista": 100,
        "total_musicas": 200,
        "tempo_estimado": "~30 minutos",
        "descrição": "Dataset robusto"
    },
    {
        "nome": "Máxima",
        "musicas_por_artista": None,
        "total_musicas": 1220,
        "tempo_estimado": "~3 horas",
        "descrição": "Coleta completa (pode ser limitada pelo site)"
    }
]

for i, opcao in enumerate(opcoes, 1):
    musicas = opcao["musicas_por_artista"] or "TODAS"
    print(f"   {i}. {opcao['nome']}:")
    print(f"      • {musicas} músicas/artista = {opcao['total_musicas']} total")
    print(f"      • Tempo: {opcao['tempo_estimado']}")
    print(f"      • {opcao['descrição']}")
    print()

print("💡 RECOMENDAÇÕES:")
print("   🟢 Para começar: Opção 1 ou 2 (20-50 músicas/artista)")
print("   🟡 Para análise séria: Opção 3 (100 músicas/artista)")  
print("   🔴 Para dataset completo: Opção 4 (todas - risco de bloqueio)")

print("\n🛡️  CONSIDERAÇÕES DE SEGURANÇA:")
print("   • Rate limiting: 1-3s entre requests")
print("   • User-Agent rotativo")
print("   • Possível bloqueio após muitas requests")

print("\n🎯 ALÉM DOS ARTISTAS ATUAIS:")
print("   Podemos adicionar mais duplas sertanejas:")
print("   • Zezé Di Camargo & Luciano")  
print("   • Victor & Leo")
print("   • João Bosco & Vinícius")
print("   • César Menotti & Fabiano")
print("   • E muitas outras...")

print("\n" + "=" * 60)
print("Qual estratégia você prefere?")