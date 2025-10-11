import json
from datetime import datetime

# Análise do arquivo JSON
print("📄 ANÁLISE DO ARQUIVO JSON")
print("=" * 80)

with open("letras_sertanejo_20250930_175739.json", 'r', encoding='utf-8') as f:
    dados_json = json.load(f)

print(f"🔍 ESTRUTURA DO JSON:")
print(f"   Tipo de dados: {type(dados_json)}")

if isinstance(dados_json, list):
    print(f"   É uma lista com {len(dados_json)} elementos")
    
    # Verificar estrutura de uma música
    if dados_json:
        exemplo_musica = dados_json[0]
        print(f"\n📝 ESTRUTURA DE UMA MÚSICA:")
        for chave in exemplo_musica.keys():
            valor = exemplo_musica[chave]
            if isinstance(valor, str) and len(valor) > 50:
                valor_resumido = valor[:50] + "..."
            else:
                valor_resumido = valor
            print(f"   {chave}: {valor_resumido}")
    
    # Verificar tamanho das letras no JSON
    print(f"\n📏 ANÁLISE DE TAMANHOS:")
    for i, musica in enumerate(dados_json):
        titulo = musica['titulo'][:30]
        letra_tamanho = len(musica['letra'])
        palavras = len(musica['letra'].split())
        print(f"   {i+1}. {titulo}: {letra_tamanho} caracteres, {palavras} palavras")
        
elif isinstance(dados_json, dict):
    print(f"   Chaves principais: {list(dados_json.keys())}")
    
    if 'metadata' in dados_json:
        metadata = dados_json['metadata']
        print(f"\n📊 METADADOS:")
        for chave, valor in metadata.items():
            print(f"   {chave}: {valor}")

    if 'musicas' in dados_json:
        musicas = dados_json['musicas']
        print(f"\n🎵 DADOS DAS MÚSICAS:")
        print(f"   Quantidade: {len(musicas)}")
        
        # Verificar estrutura de uma música
        if musicas:
            exemplo_musica = musicas[0]
            print(f"\n📝 ESTRUTURA DE UMA MÚSICA:")
            for chave in exemplo_musica.keys():
                valor = exemplo_musica[chave]
                if isinstance(valor, str) and len(valor) > 50:
                    valor_resumido = valor[:50] + "..."
                else:
                    valor_resumido = valor
                print(f"   {chave}: {valor_resumido}")
        
        # Verificar tamanho das letras no JSON
        print(f"\n📏 COMPARAÇÃO DE TAMANHOS:")
        for i, musica in enumerate(musicas):
            titulo = musica['titulo'][:30]
            letra_tamanho = len(musica['letra'])
            print(f"   {i+1}. {titulo}: {letra_tamanho} caracteres")

print(f"\n💾 INFORMAÇÕES DO ARQUIVO:")
import os
tamanho_arquivo = os.path.getsize("letras_sertanejo_20250930_175739.json")
print(f"   Tamanho do arquivo JSON: {tamanho_arquivo:,} bytes")
print(f"   Tamanho em KB: {tamanho_arquivo/1024:.1f} KB")

print("\n" + "=" * 80)
print("✅ JSON analisado com sucesso!")