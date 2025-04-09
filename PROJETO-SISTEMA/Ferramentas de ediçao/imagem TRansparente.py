from PIL import Image

# Abrir a imagem
imagem = Image.open("Zeo store´s_logo.png").convert("RGBA")

# Obter as dimensões originais da imagem
largura, altura = imagem.size

# Definir o novo tamanho desejado
novo_largura = 171
novo_altura = 35

# Calcular o fator de escala para ajustar a largura ou altura sem distorcer
if largura / altura > novo_largura / novo_altura:
    # A largura é o fator limitante
    nova_altura = int(novo_largura * altura / largura)
    nova_largura = novo_largura
else:
    # A altura é o fator limitante
    nova_largura = int(novo_altura * largura / altura)
    nova_altura = novo_altura

# Redimensionar a imagem mantendo a proporção
imagem_redimensionada = imagem.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)

# Criar uma nova imagem com o tamanho desejado (171x50), com fundo transparente
imagem_final = Image.new("RGBA", (novo_largura, novo_altura), (0, 0, 0, 0))

# Colocar a imagem redimensionada no centro
offset_x = (novo_largura - nova_largura) // 2
offset_y = (novo_altura - nova_altura) // 2
imagem_final.paste(imagem_redimensionada, (offset_x, offset_y), imagem_redimensionada)

# Salvar a imagem ajustada com fundo transparente
imagem_final.save("imagem_modificada.png", "PNG")
