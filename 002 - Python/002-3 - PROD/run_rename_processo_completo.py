# -*- coding: utf-8 -*-
"""Renomeia 001->Step1 etc na pasta LA PBD - Processo Completo."""
import os
import re

# Caminho da pasta (evita problemas de encoding no terminal)
base = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P02 - Data Flow [Códigos]\LA  PBD - Processo Completo"
if not os.path.isdir(base):
    print("Pasta nao encontrada:", base)
    exit(1)
for name in os.listdir(base):
    if name.startswith('_') or not name.endswith('.sql'):
        continue
    m = re.match(r'^(\d+)\s+-\s+(.+)$', name)
    if m:
        num = int(m.group(1))
        rest = m.group(2)
        new_name = f"Step{num} - {rest}"
        old_path = os.path.join(base, name)
        new_path = os.path.join(base, new_name)
        try:
            os.rename(old_path, new_path)
            print(f"OK: {name} -> {new_name}")
        except Exception as e:
            print(f"ERRO {name}: {e}")
print("Concluido.")
