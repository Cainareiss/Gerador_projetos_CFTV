import os
from PIL import Image

# Caminho do arquivo de entrada
caminho_entrada = r"C:\Users\Mariany\Desktop\PROJETO-SISTEMA003\PROJETO-SISTEMA\Ferramentas de ediçao\label.png.png"

# Caminho do diretório onde as imagens ajustadas serão salvas
diretorio_saida = r"C:\Users\Mariany\Desktop\PROJETO-SISTEMA003\PROJETO-SISTEMA\Ferramentas de ediçao\logos ajustados"

# Criar o diretório de saída, se não existir
os.makedirs(diretorio_saida, exist_ok=True)

# Abrir a imagem
imagem = Image.open(caminho_entrada)

# Dimensões finais em centímetros
largura_cm = 8.3
altura_cm = 4.4

# Resolução da imagem (DPI)
resolucao = 600

# Converter dimensões para pixels
largura_px = int((largura_cm / 2.54) * resolucao)
altura_px = int((altura_cm / 2.54) * resolucao)

# Redimensionar a imagem para as dimensões exatas (sem manter proporção)
imagem_redimensionada = imagem.resize((largura_px, altura_px))

# Caminho do arquivo ajustado
caminho_saida = os.path.join(diretorio_saida, "imagem_modificada.png")

# Salvar a imagem ajustada com 600 DPI
imagem_redimensionada.save(caminho_saida, dpi=(resolucao, resolucao))

print(f"Imagem ajustada salva em: {caminho_saida}")
