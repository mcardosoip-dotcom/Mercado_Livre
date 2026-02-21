import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import sys
import threading
import queue
import os
from datetime import datetime

# Configuração centralizada (P01 - Rotina): path relativo ao deste script
_este_dir = os.path.dirname(os.path.abspath(__file__))
_rotina = os.path.normpath(os.path.join(_este_dir, "..", "P01 - Rotina"))
if _rotina not in sys.path:
    sys.path.insert(0, _rotina)

try:
    from config_processo import (  # type: ignore
        SCRIPT_PROCESSO_COMPLETO,
        PROCESSOS_PONTUAIS,
        SCRIPT_M5P1_TRANSF_BASES,
        SCRIPT_M5P2_PROCESSO_COMPLETO,
    )
except ImportError:
    # Fallback se config_processo não estiver acessível (ex.: exe em outro ambiente)
    _base = os.path.normpath(os.path.join(_rotina))
    SCRIPT_PROCESSO_COMPLETO = os.path.join(_base, "000 - Processo completo.py")
    SCRIPT_M5P1_TRANSF_BASES = os.path.join(_base, ".M5p1 - Transf bases.py")
    SCRIPT_M5P2_PROCESSO_COMPLETO = os.path.join(_base, ".M5p2 - Processo completo.py")
    PROCESSOS_PONTUAIS = [
        ("Carga Dimensões", os.path.join(_base, "DIM", "000 - Carga de dados dimensoes.py")),
        ("eLAW atual", os.path.join(_base, "MAIN", "CARGA DE TABELAS", "eLAW", "000 - Carga de dados eLAW.py")),
        ("eLAW Legado", os.path.join(_base, "MAIN", "CARGA DE TABELAS", "eLAW", "Legado", "001 - Executa_conversão_em_massa.py")),
        ("Carga CLM", os.path.join(_base, "MAIN", "CARGA DE TABELAS", "CLM_DocuSign", "000 - Processo completo.py")),
        ("Salesforce", os.path.join(_base, "MAIN", "CARGA DE TABELAS", "Salesforce", "000 - Carga de dados Salesforce.py")),
        ("Salesforce Full", os.path.join(_base, "MAIN", "CARGA DE TABELAS", "Salesforce", "XXX_Salesforce_Full.py")),
        ("Quebra de Sigilo", os.path.join(_base, "MAIN", "CARGA DE TABELAS", "Quebra de sigilo", "000 - Carga de dados QS.py")),
        ("Consumidor.gov", os.path.join(_base, "MAIN", "CARGA DE TABELAS", "Consumidor.gov", "000 - Carga de dados Gov.py")),
        ("Mesa de entrada", os.path.join(_base, "MAIN", "CARGA DE TABELAS", "Mesa de entrada", "000_Push_e_carga_mesa_de_entrada.py")),
    ]

# Tema: simples e visual, refinado
COR_FUNDO = "#f0f2f5"
COR_PAPEL = "#ffffff"
COR_BORDA = "#d1d5db"
COR_BORDA_SUAVE = "#e5e7eb"
COR_TEXTO = "#374151"
COR_TEXTO_TITULO = "#111827"
COR_TEXTO_MUTED = "#6b7280"
COR_BOTAO = "#fff"
COR_BOTAO_HOVER = "#f3f4f6"
COR_BOTAO_BORDA = "#d1d5db"
COR_PROGRESSO = "#2563eb"
COR_TRILHA = "#e5e7eb"
COR_SUCESSO = "#059669"
COR_ERRO = "#dc2626"
COR_POPUP_BG = "#f0f2f5"
COR_POPUP_CARD = "#ffffff"
COR_ACCENT = "#2563eb"
COR_ACCENT_HOVER = "#1d4ed8"
COR_CARD_TITULO_BG = "#fafafa"

processo_ativo = None
fila_log = queue.Queue()
log_popup = None
area_log = None

def atualizar_log():
    """Atualiza a área de log (no popup) com mensagens da fila"""
    try:
        while True:
            mensagem = fila_log.get_nowait()
            if area_log is not None and area_log.winfo_exists():
                area_log.config(state='normal')
                area_log.insert('end', mensagem)
                area_log.see('end')
                area_log.config(state='disabled')
    except queue.Empty:
        pass
    root.after(100, atualizar_log)

def abrir_popup_log(nome_script):
    """Abre o popup com a tela de log para ler o que está acontecendo (reutiliza se já existir)."""
    global log_popup, area_log
    if log_popup is not None and log_popup.winfo_exists():
        area_log.config(state='normal')
        area_log.delete('1.0', 'end')
        area_log.config(state='disabled')
        log_popup.title(f"Log de Execução — {nome_script}")
        log_popup.deiconify()
        log_popup.lift()
        return
    log_popup = tk.Toplevel(root)
    log_popup.title(f"Log de Execução — {nome_script}")
    log_popup.geometry("900x500")
    log_popup.configure(bg=COR_POPUP_BG)
    log_popup.resizable(True, True)
    frame_popup = tk.Frame(log_popup, bg=COR_POPUP_BG, padx=15, pady=15)
    frame_popup.pack(fill='both', expand=True)
    tk.Label(frame_popup, text=f"Log — {nome_script}", font=("Segoe UI", 11, "bold"),
             bg=COR_POPUP_BG, fg=COR_TEXTO_TITULO).pack(anchor='w', pady=(0, 8))
    btn_limpar_popup = tk.Button(frame_popup, text="Limpar log", bg=COR_POPUP_CARD, fg=COR_TEXTO,
                                  font=("Segoe UI", 9), padx=12, pady=6, relief="flat",
                                  command=limpar_log, cursor="hand2",
                                  activebackground=COR_BORDA, activeforeground=COR_TEXTO_TITULO)
    btn_limpar_popup.pack(anchor='e', pady=(0, 8))
    area_log = scrolledtext.ScrolledText(frame_popup, wrap=tk.WORD, width=100, height=28,
                                         font=("Consolas", 9), bg=COR_PAPEL, fg=COR_TEXTO,
                                         insertbackground=COR_ACCENT, selectbackground="#cce5ff",
                                         relief="flat", state='disabled', highlightthickness=0)
    area_log.pack(fill='both', expand=True)

    def ao_fechar_popup():
        global area_log, log_popup, processo_ativo
        if processo_ativo is not None and processo_ativo.poll() is None:
            processo_ativo.terminate()
            processo_ativo = None
            barra.stop()
            label_status.config(text="Processo encerrado (janela de log fechada).", fg=COR_ERRO)
        win = log_popup
        area_log = None
        log_popup = None
        win.destroy()
    log_popup.protocol("WM_DELETE_WINDOW", ao_fechar_popup)

def ler_saida_processo(pipe, tipo='stdout'):
    """Lê a saída do processo linha por linha"""
    try:
        for linha in iter(pipe.readline, ''):
            if linha:
                timestamp = datetime.now().strftime("%H:%M:%S")
                # Remove quebras de linha extras e adiciona uma no final
                linha_limpa = linha.rstrip('\n\r') + '\n'
                mensagem = f"[{timestamp}] {linha_limpa}"
                fila_log.put(mensagem)
        pipe.close()
    except Exception as e:
        fila_log.put(f"[{datetime.now().strftime('%H:%M:%S')}] [ERRO] Erro ao ler saída: {str(e)}\n")

def monitorar_processo():
    global processo_ativo
    if processo_ativo and processo_ativo.poll() is None:
        root.after(100, monitorar_processo)
    else:
        if processo_ativo:
            codigo_saida = processo_ativo.returncode
            barra.stop()
            if codigo_saida == 0:
                label_status.config(text="Processo concluído com sucesso.", fg=COR_SUCESSO)
                fila_log.put(f"\n[{'='*60}]\n")
                fila_log.put(f"[{datetime.now().strftime('%H:%M:%S')}] Processo finalizado com sucesso (código: {codigo_saida})\n")
            else:
                label_status.config(text=f"Processo finalizado com erro (código: {codigo_saida})", fg=COR_ERRO)
                fila_log.put(f"\n[{'='*60}]\n")
                fila_log.put(f"[{datetime.now().strftime('%H:%M:%S')}] Processo finalizado com erro (código: {codigo_saida})\n")

def limpar_log():
    """Limpa a área de log (no popup)"""
    if area_log is not None and area_log.winfo_exists():
        area_log.config(state='normal')
        area_log.delete('1.0', 'end')
        area_log.config(state='disabled')

def executar_script(caminho_script):
    def thread_func():
        global processo_ativo
        nome_script = os.path.basename(caminho_script)
        label_status.config(text=f"Executando: {nome_script}...", fg=COR_ACCENT)
        barra.start()
        fila_log.put(f"\n[{'='*60}]\n")
        fila_log.put(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando execução: {nome_script}\n")
        fila_log.put(f"[{'='*60}]\n\n")
        
        try:
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            kwargs = {
                'env': env,
                'cwd': os.path.dirname(caminho_script) or None,
            }
            if sys.platform == 'win32':
                kwargs['creationflags'] = subprocess.CREATE_NEW_CONSOLE

            processo_ativo = subprocess.Popen(
                ['python', '-u', caminho_script],
                **kwargs
            )

            root.after(100, monitorar_processo)
        except Exception as e:
            barra.stop()
            label_status.config(text="Erro ao iniciar processo.", fg=COR_ERRO)
            fila_log.put(f"[{datetime.now().strftime('%H:%M:%S')}] ERRO: {str(e)}\n")
    
    threading.Thread(target=thread_func, daemon=True).start()

def fechar():
    global processo_ativo
    if processo_ativo and processo_ativo.poll() is None:
        processo_ativo.terminate()
    root.destroy()

def botao_simples(parent, texto, comando):
    """Botão só texto, sem ícone."""
    btn = tk.Button(parent, text=texto, font=("Segoe UI", 10), fg=COR_TEXTO,
                    bg=COR_BOTAO, activebackground=COR_BOTAO_HOVER, activeforeground=COR_TEXTO,
                    relief="solid", borderwidth=1, padx=12, pady=8, cursor="hand2",
                    command=comando, highlightthickness=0)
    btn.bind("<Enter>", lambda e: btn.config(bg=COR_BOTAO_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=COR_BOTAO))
    return btn

def botao_primario(parent, texto, comando):
    """Botão de ação principal (destaque)."""
    btn = tk.Button(parent, text=texto, font=("Segoe UI", 10, "bold"), fg="white",
                    bg=COR_ACCENT, activebackground=COR_ACCENT_HOVER, activeforeground="white",
                    relief="flat", borderwidth=0, padx=16, pady=8, cursor="hand2",
                    command=comando, highlightthickness=0)
    btn.bind("<Enter>", lambda e: btn.config(bg=COR_ACCENT_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=COR_ACCENT))
    return btn

def criar_card(container, titulo):
    """Card com borda suave e faixa de título."""
    card = tk.Frame(container, bg=COR_PAPEL, highlightbackground=COR_BORDA, highlightthickness=1)
    card.pack(fill='x', pady=(0, 14))
    # Faixa do título
    faixa = tk.Frame(card, bg=COR_CARD_TITULO_BG, height=36)
    faixa.pack(fill='x')
    faixa.pack_propagate(False)
    tk.Label(faixa, text=titulo, font=("Segoe UI", 11, "bold"),
             bg=COR_CARD_TITULO_BG, fg=COR_TEXTO_TITULO).pack(anchor='w', padx=20, pady=8)
    inner = tk.Frame(card, bg=COR_PAPEL, padx=20, pady=16)
    inner.pack(fill='x')
    return inner

def secao(container, titulo, botoes):
    """Seção: título + linha de botões (lista de (texto, comando))."""
    f = tk.Frame(container, bg=COR_FUNDO)
    f.pack(fill='x', pady=(0, 18))
    tk.Label(f, text=titulo, font=("Segoe UI", 11, "bold"), bg=COR_FUNDO, fg=COR_TEXTO_TITULO).pack(anchor='w', pady=(0, 8))
    linha = tk.Frame(f, bg=COR_FUNDO)
    linha.pack(fill='x')
    for texto, cmd in botoes:
        botao_simples(linha, texto, cmd).pack(side='left', padx=(0, 10), pady=2)
    return f

# PROCESSOS_PONTUAIS vem de config_processo (P01 - Rotina)

def secao_processo_pontual(container):
    """Seção 'Processo pontual' com combobox e botão Executar."""
    inner = criar_card(container, "Processo pontual")
    linha = tk.Frame(inner, bg=COR_PAPEL)
    linha.pack(fill='x')
    tk.Label(linha, text="Processo:", font=("Segoe UI", 10), bg=COR_PAPEL, fg=COR_TEXTO_MUTED).pack(side='left', padx=(0, 8), pady=4)
    nomes = [nome for nome, _ in PROCESSOS_PONTUAIS]
    var_combo = tk.StringVar(value=nomes[0] if nomes else "")
    combo = ttk.Combobox(linha, textvariable=var_combo, values=nomes, state="readonly",
                         font=("Segoe UI", 10), width=26)
    combo.pack(side='left', padx=(0, 12), pady=4)

    def executar_selecionado():
        sel = var_combo.get()
        for nome, script in PROCESSOS_PONTUAIS:
            if nome == sel:
                executar_script(script)
                return

    botao_primario(linha, "Executar", executar_selecionado).pack(side='left', pady=4)
    return inner.master

# Interface — simples e visual, sem imagens
root = tk.Tk()
root.title("Legal Analytics — Automação de Processos")
root.configure(bg=COR_FUNDO)
root.geometry("880x540")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", fechar)
root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)

container_principal = tk.Frame(root, bg=COR_FUNDO)
container_principal.pack(fill='both', expand=True, padx=28, pady=24)

tk.Label(container_principal, text="Automação de Processos",
         font=("Segoe UI", 20, "bold"), bg=COR_FUNDO, fg=COR_TEXTO_TITULO).pack(anchor='w')
tk.Frame(container_principal, bg=COR_ACCENT, height=2, width=56).pack(anchor='w', pady=(6, 0))
tk.Label(container_principal, text="Legal Analytics",
         font=("Segoe UI", 10), bg=COR_FUNDO, fg=COR_TEXTO_MUTED).pack(anchor='w', pady=(10, 22))

# Processo pontual (bloco opcional por checkbox)
secao_processo_pontual(container_principal)

# Máquina Local (Processo completo)
inner_local = criar_card(container_principal, "Máquina Local")
linha_local = tk.Frame(inner_local, bg=COR_PAPEL)
linha_local.pack(fill='x')
botao_simples(linha_local, "Processo completo", lambda: executar_script(SCRIPT_PROCESSO_COMPLETO)).pack(side='left', padx=(0, 10), pady=2)

# Máquina 5
inner_m5 = criar_card(container_principal, "Máquina 5")
linha_m5 = tk.Frame(inner_m5, bg=COR_PAPEL)
linha_m5.pack(fill='x')
botao_simples(linha_m5, "M5p1 — Transf bases", lambda: executar_script(SCRIPT_M5P1_TRANSF_BASES)).pack(side='left', padx=(0, 10), pady=2)
botao_simples(linha_m5, "M5p2 — Processo completo", lambda: executar_script(SCRIPT_M5P2_PROCESSO_COMPLETO)).pack(side='left', padx=(0, 10), pady=2)

# Status
card_status = tk.Frame(container_principal, bg=COR_CARD_TITULO_BG, highlightbackground=COR_BORDA_SUAVE, highlightthickness=1)
card_status.pack(fill='x', pady=(18, 0))

frame_status = tk.Frame(card_status, bg=COR_CARD_TITULO_BG)
frame_status.pack(fill='x', padx=20, pady=14)

label_status = tk.Label(frame_status, text="Aguardando ação…", bg=COR_CARD_TITULO_BG, fg=COR_TEXTO_MUTED, font=("Segoe UI", 10))
label_status.pack(side='left')

style = ttk.Style()
style.theme_use('default')
style.configure("TProgressbar", thickness=6, troughcolor=COR_TRILHA, background=COR_PROGRESSO, bordercolor=COR_CARD_TITULO_BG)
barra = ttk.Progressbar(frame_status, mode='indeterminate', length=260)
barra.pack(side='left', padx=(12, 0))

# Inicia a atualização do log
root.after(100, atualizar_log)

root.mainloop()
