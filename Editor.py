import streamlit as st
from rembg import remove
from PIL import Image, ImageDraw
import io

# Função para adicionar o fundo branco e fazer o recorte circular
def add_white_circle(img: Image, size: int):
    # Cria uma nova imagem com fundo branco
    new_img = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    
    # Ajusta o tamanho da imagem
    img = img.resize((size, size))  # Ajusta o tamanho da imagem
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    # Aplica a máscara circular
    new_img.paste(img, (0, 0), mask=mask)
    
    return new_img

# Título da aplicação
st.title("Remover Fundo e Colocar em Círculo Branco")

# Carregar imagem
uploaded_file = st.file_uploader("Escolha uma imagem", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Exibir a imagem carregada
    st.image(uploaded_file, caption="Imagem Original", use_column_width=True)
    
    # Lendo os dados da imagem carregada.
    input_image = uploaded_file.read()  # Lê os bytes da imagem carregada
    
    # Remover o fundo da imagem com rembg (comando binário).
    output_image_bytes = remove(input_image)  # O retorno é um objeto bytes
    
    # Converter os bytes em uma imagem usando io.BytesIO
    output_image = Image.open(io.BytesIO(output_image_bytes))

    # Exibir imagem sem fundo
    st.image(output_image, caption="Imagem sem Fundo", use_column_width=True)

    # Ajustar tamanho da imagem
    size = st.slider("Redimensionar imagem", min_value=100, max_value=1000, value=500)

    # Adicionar círculo branco
    final_image = add_white_circle(output_image, size)
    
    # Exibir a imagem final
    st.image(final_image, caption="Imagem Final com Círculo Branco", use_column_width=True)

    # Salvar a imagem final
    buf = io.BytesIO()
    final_image.save(buf, format="PNG")
    buf.seek(0)
    
    st.download_button("Baixar Imagem Final", buf, "imagem_final.png", "image/png")
