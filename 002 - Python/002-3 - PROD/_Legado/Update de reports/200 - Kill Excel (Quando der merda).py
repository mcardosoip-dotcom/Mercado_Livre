# ================================================
# Descrição :  Durante o processo de atualização dos acompanhamentos, o Excel pode travar 
#              e deixar uma pilha presa na memória; este processo elimina qualquer tipo 
#              de pilha para que o script possa ser executado novamente
# Autor : Marcelo Cardoso
# ================================================

import os
import signal
import psutil

def encerrar_excel():
    encerrados = 0
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and 'EXCEL.EXE' in proc.info['name'].upper():
                os.kill(proc.info['pid'], signal.SIGTERM)
                encerrados += 1
                print(f"Processo encerrado: PID {proc.info['pid']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if encerrados == 0:
        print("Nenhum processo do Excel estava em execução.")
    else:
        print(f"{encerrados} processo(s) do Excel encerrado(s).")

if __name__ == "__main__":
    encerrar_excel()
