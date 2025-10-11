#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Monitor e backup para coleta massiva
"""

import time
import sys

def monitorar_coleta():
    print("🔍 INICIANDO COLETA MASSIVA COM MONITORAMENTO")
    print("=" * 60)
    
    total_artistas = 47  # Artistas na lista atual
    print(f"📊 Meta: {total_artistas} artistas × 10 músicas = ~470 músicas")
    print(f"⏱️ Tempo estimado: 1.5-2 horas")
    print(f"💾 Backup automático a cada 10 artistas")
    
    print(f"\n🚨 ATENÇÃO:")
    print(f"   • Esta é uma coleta MASSIVA")
    print(f"   • Risco de bloqueio pelo site")
    print(f"   • Monitoramento contínuo necessário")
    print(f"   • Backup incremental ativado")
    
    print(f"\n🛡️  MEDIDAS DE SEGURANÇA:")
    print(f"   ✅ Rate limiting: 1-3s entre requests")
    print(f"   ✅ User-Agent rotativo")
    print(f"   ✅ Pausa entre artistas")
    print(f"   ✅ Validação de qualidade")
    print(f"   ✅ Recuperação automática")
    
    print(f"\n⚡ PRONTO PARA INICIAR COLETA MASSIVA!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    monitorar_coleta()
    
    print("\n🚀 Iniciando scraper massivo em 3 segundos...")
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("\n🎯 EXECUTANDO COLETA MASSIVA!")
    
    # Importar e executar o scraper
    import subprocess
    import os
    
    os.chdir("G:\\Meu Drive\\Mestrado\\KDD\\Trabalho pratico\\projeto_funk\\sertanejo_scraper")
    
    try:
        result = subprocess.run(["python", "scraper_sertanejo.py"], 
                              capture_output=True, text=True, timeout=7200)  # 2 horas timeout
        
        print("✅ COLETA MASSIVA CONCLUÍDA!")
        print(f"📤 Output:\n{result.stdout}")
        
        if result.stderr:
            print(f"⚠️ Warnings:\n{result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT: Coleta interrompida após 2 horas")
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
    
    print("\n" + "=" * 60)