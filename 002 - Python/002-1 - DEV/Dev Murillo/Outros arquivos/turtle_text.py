import turtle
from PIL import Image, ImageDraw, ImageFont # Biblioteca Pillow

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
PIXEL_SIZE = 8       # Tamanho do quadradinho na tela
GRID_SIZE = 16       # Resolução da grade (16x16)
FONTE_ARQUIVO = "arial.ttf" # Ou "consola.ttf", "cour.ttf" (Courier)
TAMANHO_FONTE = 12   # Tamanho da letra dentro do grid 16x16

# Configuração da Tela Turtle
tela = turtle.Screen()
tela.setup(1000, 400)
tela.bgcolor("black")
tela.title("Rasterizador Automático de Fontes")
tela.tracer(0) # Desliga animação para renderizar instantâneo

t = turtle.Turtle()
t.shape("square")
t.shapesize(PIXEL_SIZE / 20) # Ajusta o tamanho do quadrado
t.color("#00FF00")           # Verde Matrix
t.penup()
t.hideturtle()

# ==============================================================================
# LÓGICA DE RASTERIZAÇÃO (A MÁGICA)
# ==============================================================================

def obter_pixels_da_letra(caractere):
    """
    Cria uma imagem fantasma na memória, desenha a letra nela
    e retorna uma lista de coordenadas onde os pixels estão ativos.
    """
    # 1. Cria uma imagem em branco (Preto e Branco - mode '1')
    imagem = Image.new('1', (GRID_SIZE, GRID_SIZE), 0)
    desenho = ImageDraw.Draw(imagem)
    
    try:
        # 2. Carrega a fonte do Windows
        fonte = ImageFont.truetype(FONTE_ARQUIVO, TAMANHO_FONTE)
    except IOError:
        # Fallback caso não ache a fonte
        print("⚠️ Fonte não encontrada, usando padrão.")
        fonte = ImageFont.load_default()

    # 3. Desenha a letra na imagem (centralizando verticalmente de forma simples)
    # O offset (2, 0) empurra um pouco para direita para não cortar
    desenho.text((2, 0), caractere, font=fonte, fill=1)
    
    # 4. Escaneia a imagem e guarda onde tem "tinta" (pixel = 1)
    pixels_ativos = []
    largura, altura = imagem.size
    
    for y in range(altura):
        for x in range(largura):
            # Se o pixel for > 0 (tem cor)
            if imagem.getpixel((x, y)) > 0:
                pixels_ativos.append((x, y))
                
    return pixels_ativos

def desenhar_frase(texto):
    cursor_x = -((len(texto) * GRID_SIZE * PIXEL_SIZE) / 2) # Centraliza na tela
    start_y = 50
    
    print(f"🖨️ Processando: '{texto}' usando fonte {FONTE_ARQUIVO}...")
    
    for letra in texto:
        # Obtém os pontos automaticamente da fonte
        pontos = obter_pixels_da_letra(letra)
        
        for p in pontos:
            x_grid, y_grid = p
            
            # Converte coordenadas da imagem (Top-Left 0,0) para Turtle (Center 0,0)
            # Invertemos o Y porque imagem cresce para baixo, Turtle cresce para cima
            screen_x = cursor_x + (x_grid * PIXEL_SIZE)
            screen_y = start_y - (y_grid * PIXEL_SIZE)
            
            t.goto(screen_x, screen_y)
            t.stamp()
            
        # Avança o cursor para a próxima letra
        cursor_x += (GRID_SIZE * PIXEL_SIZE)
        
    tela.update()

# ==============================================================================
# EXECUÇÃO
# ==============================================================================

# Pode escrever qualquer coisa, inclusive acentos e símbolos!
entrada = turtle.textinput("Terminal", "Digite o texto:")

if not entrada:
    entrada = "Atenção: A,g,ç,%,@"

desenhar_frase(entrada)

turtle.done()