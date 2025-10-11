#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Análise e organização da lista expandida de artistas sertanejos
"""

print("🎤 ANÁLISE DA LISTA EXPANDIDA DE ARTISTAS SERTANEJO")
print("=" * 70)

# Lista fornecida pelo usuário
artistas_completos = [
    "Henrique & Juliano",
    "Luan Santana", 
    "Jorge & Mateus",
    "Zezé Di Camargo & Luciano",
    "Marília Mendonça",
    "Chitãozinho & Xororó",  # Já temos
    "Bruno & Marrone",       # Já temos
    "Gusttavo Lima",
    "Leandro & Leonardo",
    "Zé Neto e Cristiano",
    "Milionário e José Rico",
    "Matheus & Kauan",
    "Simone Mendes",
    "Cristiano Araújo",
    "Ana Castela",
    "Diego e Victor Hugo",
    "Gustavo Mioto",
    "Rick & Renner",
    "Victor & Leo",
    "Almir Sater",
    "Felipe Araújo",
    "Eduardo Costa",
    "Lauana Prado",
    "Hugo & Guilherme",
    "Daniel",
    "Maiara & Maraisa",
    "Tião Carreiro e Pardinho",
    "Leonardo",
    "Clayton e Romário",
    "Paula Fernandes",
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

# Categorização dos artistas
categorias = {
    "✅ Já Coletados": [
        "Chitãozinho & Xororó",
        "Bruno & Marrone"
    ],
    
    "🔥 Sertanejo Moderno (Top)": [
        "Henrique & Juliano",
        "Jorge & Mateus", 
        "Luan Santana",
        "Gusttavo Lima",
        "Zé Neto e Cristiano",
        "Matheus & Kauan"
    ],
    
    "👑 Clássicos/Icônicos": [
        "Zezé Di Camargo & Luciano",
        "Leandro & Leonardo",
        "Victor & Leo",
        "Daniel",
        "Leonardo"
    ],
    
    "⭐ Feminino": [
        "Marília Mendonça",
        "Simone Mendes", 
        "Ana Castela",
        "Lauana Prado",
        "Paula Fernandes",
        "Maiara & Maraisa"
    ],
    
    "🎸 Raiz/Tradicional": [
        "Milionário e José Rico",
        "Almir Sater",
        "Sérgio Reis",
        "Tião Carreiro e Pardinho",
        "Tonico e Tinoco",
        "João Mineiro e Marciano"
    ],
    
    "🚀 Nova Geração": [
        "Diego e Victor Hugo",
        "Gustavo Mioto",
        "Felipe Araújo",
        "Murilo Huff",
        "Zé Felipe",
        "Luan Pereira"
    ]
}

print(f"📊 ESTATÍSTICAS GERAIS:")
print(f"   Total de artistas na lista: {len(artistas_completos)}")
print(f"   Já coletados: {len(categorias['✅ Já Coletados'])}")
print(f"   Novos para coletar: {len(artistas_completos) - len(categorias['✅ Já Coletados'])}")

print(f"\n🎯 CATEGORIZAÇÃO:")
for categoria, lista in categorias.items():
    print(f"\n{categoria} ({len(lista)} artistas):")
    for artista in lista:
        print(f"   • {artista}")

# Estratégia de coleta
print(f"\n💡 ESTRATÉGIAS DE COLETA:")

estrategias = [
    {
        "nome": "🟢 Conservadora",
        "artistas": 5,
        "musicas_cada": 10,
        "total": 50,
        "tempo": "~10 min",
        "desc": "Top 5 mais populares"
    },
    {
        "nome": "🟡 Equilibrada", 
        "artistas": 10,
        "musicas_cada": 12,
        "total": 120,
        "tempo": "~25 min",
        "desc": "Mix de categorias"
    },
    {
        "nome": "🟠 Ampla",
        "artistas": 20,
        "musicas_cada": 10,
        "total": 200,
        "tempo": "~45 min", 
        "desc": "Boa representatividade"
    },
    {
        "nome": "🔴 Completa",
        "artistas": len(artistas_completos) - 2,  # Menos os já coletados
        "musicas_cada": 10,
        "total": (len(artistas_completos) - 2) * 10,
        "tempo": "~2-3 horas",
        "desc": "Todos os artistas"
    }
]

for i, est in enumerate(estrategias, 1):
    print(f"\n   {i}. {est['nome']}: {est['artistas']} artistas × {est['musicas_cada']} músicas = {est['total']} músicas")
    print(f"      ⏱️ {est['tempo']} | 💡 {est['desc']}")

print(f"\n🛡️  CONSIDERAÇÕES TÉCNICAS:")
print(f"   • Rate limiting necessário (1-3s entre requests)")
print(f"   • Possível bloqueio após muitas requests consecutivas")
print(f"   • Recomendado fazer em lotes")

print(f"\n🎯 RECOMENDAÇÃO:")
print(f"   Começar com estratégia EQUILIBRADA (10 artistas)")
print(f"   Focar em diversidade: 2 de cada categoria principal")

print("\n" + "=" * 70)