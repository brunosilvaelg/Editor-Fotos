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

# Carregar múltiplas imagens
uploaded_files = st.file_uploader("Escolha as imagens", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Exibir a imagem carregada
        st.image(uploaded_file, caption=f"Imagem Original: {uploaded_file.name}", use_column_width=True)
        
        # Lendo os dados da imagem carregada
        input_image = uploaded_file.read()  # Lê os bytes da imagem carregada
        
        # Remover o fundo da imagem com rembg
        output_image_bytes = remove(input_image)  # O retorno é um objeto bytes
        
        # Converter os bytes em uma imagem usando io.BytesIO
        output_image = Image.open(io.BytesIO(output_image_bytes))

        # Exibir imagem sem fundo
        st.image(output_image, caption="Imagem sem Fundo", use_column_width=True)

        # Ajustar tamanho da imagem manualmente (largura e altura)
        width = st.number_input("Largura da imagem", min_value=100, max_value=1000, value=500)
        height = st.number_input("Altura da imagem", min_value=100, max_value=1000, value=500)

        # Adicionar círculo branco
        final_image = add_white_circle(output_image, max(width, height))  # Usando a maior dimensão para o círculo
        
        # Exibir a imagem final
        st.image(final_image, caption=f"Imagem Final com Círculo Branco: {uploaded_file.name}", use_column_width=True)

        # Opção de salvar a imagem final em diferentes formatos
        export_format = st.selectbox("Escolha o formato de exportação", ["PNG", "JPG", "JPEG"])

        buf = io.BytesIO()
        if export_format == "PNG":
            final_image.save(buf, format="PNG")
            buf.seek(0)
            st.download_button(f"Baixar {uploaded_file.name} como PNG", buf, f"{uploaded_file.name}_final.png", "image/png")
        elif export_format in ["JPG", "JPEG"]:
            final_image = final_image.convert("RGB")  # Converte para RGB para exportação em JPG
            final_image.save(buf, format="JPEG")
            buf.seek(0)
            st.download_button(f"Baixar {uploaded_file.name} como JPG", buf, f"{uploaded_file.name}_final.jpg", "image/jpeg")
