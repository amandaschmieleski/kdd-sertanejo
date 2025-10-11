#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuração para coleta massiva - 50+ artistas sertanejos
"""

# Lista completa dos 51 artistas fornecidos pelo usuário
ARTISTAS_COMPLETOS = [
    # Já coletados (manter)
    "Chitãozinho & Xororó",
    "Bruno & Marrone", 
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
    
    # Novos artistas para expandir (39 restantes)
    "Luan Santana",
    "Gusttavo Lima", 
    "Zé Neto e Cristiano",
    "Matheus & Kauan",
    "Simone Mendes",
    "Cristiano Araújo",
    "Ana Castela",
    "Gustavo Mioto",
    "Rick & Renner",
    "Victor & Leo",
    "Felipe Araújo",
    "Eduardo Costa",
    "Lauana Prado",
    "Hugo & Guilherme",
    "Daniel",
    "Maiara & Maraisa",
    "Tião Carreiro e Pardinho",
    "Leonardo",
    "Clayton e Romário",
    "Guilherme & Benuto",
    "Chrystian & Ralf",
    "Trio Parada Dura",
    "Murilo Huff",
    "Matogrosso & Mathias",
    "Ícaro e Gilmar",
    "João Mineiro e Marciano",
    "Gian e Giovani",
    "Zé Felipe",
    "Gino e Geno",
    "Rionegro & Solimões",
    "João Paulo e Daniel",
    "Marcos & Belutti",
    "Sérgio Reis",
    "Tonico e Tinoco",
    "Lourenço e Lourival",
    "Teodoro e Sampaio",
    "Edson & Hudson",
    "Chico Rey e Paraná",
    "Guilherme & Santiago",
    "Luan Pereira"
]

print("🚀 CONFIGURAÇÃO PARA COLETA MASSIVA")
print("=" * 60)

print(f"📊 ESTATÍSTICAS:")
print(f"   Total de artistas disponíveis: {len(ARTISTAS_COMPLETOS)}")
print(f"   Já coletados: 12")
print(f"   Novos para coletar: {len(ARTISTAS_COMPLETOS) - 12}")

print(f"\n🎯 CENÁRIOS DE COLETA:")

cenarios = [
    {
        "nome": "🟡 Base Sólida",
        "artistas": 25,
        "musicas_cada": 10,
        "tempo": "~45 min",
        "total_musicas": 250,
        "desc": "Boa para modelos iniciais"
    },
    {
        "nome": "🟠 Robusto", 
        "artistas": 40,
        "musicas_cada": 12,
        "tempo": "~1.5 horas",
        "total_musicas": 480,
        "desc": "Ideal para modelo sério"
    },
    {
        "nome": "🔴 Completo",
        "artistas": len(ARTISTAS_COMPLETOS),
        "musicas_cada": 10,
        "tempo": "~2-3 horas",
        "total_musicas": len(ARTISTAS_COMPLETOS) * 10,
        "desc": "Dataset completo"
    }
]

for i, cenario in enumerate(cenarios, 1):
    print(f"\n   {i}. {cenario['nome']}: {cenario['artistas']} artistas")
    print(f"      • {cenario['musicas_cada']} músicas/artista = {cenario['total_musicas']} músicas")
    print(f"      • Tempo estimado: {cenario['tempo']}")
    print(f"      • {cenario['desc']}")

print(f"\n💡 RECOMENDAÇÃO PARA MODELO:")
print(f"   🎯 Para ML sério: Cenário 2 (40 artistas = 480 músicas)")
print(f"   🔥 Para dataset completo: Cenário 3 (51 artistas = 510+ músicas)")

print(f"\n⚠️  CONSIDERAÇÕES:")
print(f"   • Coleta em lotes para evitar bloqueio")
print(f"   • Rate limiting: 1-3s entre requests") 
print(f"   • Monitoramento de falhas")
print(f"   • Backup incremental")

print(f"\n🚀 ESTRATÉGIA RECOMENDADA:")
print(f"   1. Começar com 25 artistas (cenário 1)")
print(f"   2. Se bem-sucedido, expandir para 40-51")
print(f"   3. Fazer em sessões de 10-15 artistas")

print("\n" + "=" * 60)
print("Qual cenário você prefere? Vamos começar agressivo ou conservador?")