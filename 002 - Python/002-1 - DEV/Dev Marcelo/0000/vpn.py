# Monitor de Inatividade - Desconexão Automática da VPN GlobalProtect
#
# Funciona em Windows e macOS.
#
# Requisitos:
#   pip install pystray Pillow
#
# Windows - Gerar executável (.exe):
#   pip install pyinstaller
#   pyinstaller --onefile --noconsole --name "VPN_Monitor" vpn.py
#
# Windows - Iniciar automaticamente:
#   Win+R → shell:startup → copie o VPN_Monitor.exe para essa pasta
#
# macOS - Iniciar automaticamente:
#   Adicione ao "Login Items" em Ajustes do Sistema > Geral > Itens de login

import os
import subprocess
import sys
import threading
import time
from PIL import Image, ImageDraw
import pystray

IS_WINDOWS = sys.platform == "win32"
IS_MAC = sys.platform == "darwin"

if IS_WINDOWS:
    import ctypes

# ─── Configurações ────────────────────────────────────────────────────────────
INACTIVITY_LIMIT_SECONDS = 60    # TESTE: 1 minuto  (produção: 2 * 3600)
CHECK_INTERVAL_SECONDS   = 5     # TESTE: 5 segundos  (produção: 60)

# Caminhos do GlobalProtect por plataforma
GLOBALPROTECT_PATHS_WIN = [
    r"C:\Program Files\Palo Alto Networks\GlobalProtect\PanGPA.exe",
    r"C:\Program Files (x86)\Palo Alto Networks\GlobalProtect\PanGPA.exe",
]
GLOBALPROTECT_PATHS_MAC = [
    "/Applications/GlobalProtect.app/Contents/MacOS/GlobalProtect",
    "/Applications/GlobalProtect.app/Contents/Resources/globalprotect",
]

# ─── Estado global ─────────────────────────────────────────────────────────────
_running    = True
_tray_icon  = None


# ─── Detecção de inatividade ──────────────────────────────────────────────────
def _get_idle_seconds_win() -> float:
    """Windows: usa GetLastInputInfo para tempo sem mouse/teclado."""
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(lii)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    elapsed_ms = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return elapsed_ms / 1000.0


def _get_idle_seconds_mac() -> float:
    """macOS: usa IOHIDSystem (HIDIdleTime) para tempo sem mouse/teclado."""
    try:
        result = subprocess.run(
            ["ioreg", "-r", "-c", "IOHIDSystem", "-d", "4"],
            capture_output=True, text=True, timeout=2
        )
        if result.returncode != 0:
            return 0.0
        for line in result.stdout.splitlines():
            if "HIDIdleTime" in line:
                parts = line.split("=")
                if len(parts) >= 2:
                    # HIDIdleTime está em nanossegundos
                    return int(parts[1].strip()) / 1_000_000_000
    except (subprocess.TimeoutExpired, ValueError, FileNotFoundError):
        pass
    return 0.0


def get_idle_seconds() -> float:
    """Retorna quantos segundos o usuário está inativo (sem mouse/teclado)."""
    if IS_WINDOWS:
        return _get_idle_seconds_win()
    if IS_MAC:
        return _get_idle_seconds_mac()
    return 0.0


# ─── Desconexão da VPN ────────────────────────────────────────────────────────
def disconnect_vpn():
    """Desconecta a VPN GlobalProtect (Windows ou macOS)."""
    if IS_WINDOWS:
        for path in GLOBALPROTECT_PATHS_WIN:
            if os.path.exists(path):
                subprocess.run([path, "disconnect"], capture_output=True)
                return
        subprocess.run(["net", "stop", "PanGPS"], capture_output=True)
        return

    if IS_MAC:
        for path in GLOBALPROTECT_PATHS_MAC:
            if os.path.exists(path):
                subprocess.run([path, "disconnect"], capture_output=True)
                return
        # Fallback: tentar comando no PATH (se GlobalProtect CLI estiver instalado)
        subprocess.run(["globalprotect", "disconnect"], capture_output=True)


# ─── Notificações ─────────────────────────────────────────────────────────────
def show_balloon(title: str, message: str):
    """Exibe notificação balloon no system tray via pystray."""
    if _tray_icon is not None:
        try:
            _tray_icon.notify(message, title)
        except Exception:
            pass


def show_disconnected():
    show_balloon(
        "🔴 VPN Monitor - Desconectada",
        "VPN GlobalProtect desconectada por inatividade de 2 horas."
    )


# ─── Loop de monitoramento ────────────────────────────────────────────────────
def monitor_loop():
    """Thread daemon: verifica inatividade a cada CHECK_INTERVAL_SECONDS."""
    global _running

    while _running:
        idle = get_idle_seconds()

        if idle >= INACTIVITY_LIMIT_SECONDS:
            disconnect_vpn()
            show_disconnected()
            # Aguarda o usuário retornar antes de voltar a monitorar
            time.sleep(INACTIVITY_LIMIT_SECONDS)

        time.sleep(CHECK_INTERVAL_SECONDS)


# ─── Ícone do system tray ─────────────────────────────────────────────────────
def create_icon_image(color: str = "#2ECC71") -> Image.Image:
    """Gera um ícone circular simples com a cor indicada."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, size - 4, size - 4], fill=color)
    return img


def on_disconnect_now(icon, item):
    """Ação do menu: desconectar VPN imediatamente."""
    disconnect_vpn()
    show_balloon("VPN Monitor", "VPN desconectada manualmente.")


def on_quit(icon, item):
    """Ação do menu: encerrar o monitor."""
    global _running
    _running = False
    icon.stop()


def build_menu() -> pystray.Menu:
    return pystray.Menu(
        pystray.MenuItem("VPN Monitor - Ativo", None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Desconectar VPN agora", on_disconnect_now),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Sair", on_quit),
    )


# ─── Ponto de entrada ─────────────────────────────────────────────────────────
def main():
    global _tray_icon

    # Inicia a thread de monitoramento como daemon
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()

    # Cria e executa o ícone da bandeja (bloqueia a thread principal)
    _tray_icon = pystray.Icon(
        name="VPN_Monitor",
        icon=create_icon_image("#2ECC71"),
        title="VPN Monitor",
        menu=build_menu(),
    )
    _tray_icon.run()


if __name__ == "__main__":
    main()
