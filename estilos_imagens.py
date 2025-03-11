import streamlit as st
from together import Together
import requests
from PIL import Image
from io import BytesIO

# Estilos de imagem
estilos_imagem = [
    "Fotografia", 
    "Pintura a carvão",
    "Realismo", "Surrealismo", "Abstracionismo", "Minimalismo", "Cartoon",
    "Mangá/Anime", "Ilustração Infantil", "Ilustração Técnica", "Ilustração de Moda",
    "Ilustração Editorial",
    "Realismo", "Impressionismo", "Expressionismo", "Cubismo", "Surrealismo",
    "Abstracionismo", "Pop Art", "Arte Moderna", "Arte Contemporânea", "Barroco",
    "Rococó", "Renascimento", "Pintura a Oleo",
    "Pixel Art", "3D Rendering", "Digital Painting", "Vetorização", "Arte Generativa",
    "Colagem", "Mosaico", "Grafite/Street Art", "Escultura", "Gravura",
    "Fantasia/Ficção Científica", "Abstrato", "Comida/Gastronomia", 
    "Publicidade/Comercial", "Minimalista", "Vintage/Retrô", "Clássico",
    "Moderno", "Industrial", "Boho/Bohemian", "Grunge", "Steampunk", "Cyberpunk"
]


with st.sidebar:
    st.sidebar.header("Gerador de Imagens")
    st.sidebar.write("""

    - Caso tenha alguma idéia para publicarmos, envie uma mensagem para: 11-990000425 (Willian)
    - Contribua com qualquer valor para mantermos a pagina no ar. PIX (wpyagami@gmail.com)
    """)

# Título da aplicação
st.title("Gerador de Imagens")

# Campo para inserir a chave de API
APIK = st.secrets["together"]

# Campo para inserir o tema do desenho
tema = st.text_input("Tema do Desenho (ex: um pássaro voando entre nuvens):")

# Componente multiselect para estilos de imagem
estilos_selecionados = st.multiselect(
    "Estilos de Imagem:",
    options=estilos_imagem,
    default=["Ilustração Editorial"]  # Estilo padrão - MUST be one of the options.
)


# Botão para gerar o desenho
if st.button("Gerar Desenho"):
    # Verifica se a chave de API e o tema foram fornecidos
    if APIK and tema:
        # Constrói o prompt com o tema e estilos selecionados
        prompt = f"Crie uma imagem em alte resolução. A imagem deve representar {tema}."

        # Adiciona os estilos ao prompt
        if estilos_selecionados:
            prompt += " No estilo de: " + ", ".join(estilos_selecionados) + "."

        try:
            # Inicializa o cliente da API com a chave fornecida
            client = Together(api_key=APIK)

            # Gera a imagem usando a API do Together
            response = client.images.generate(
                prompt=prompt,
                model="black-forest-labs/FLUX.1-schnell-Free",
                steps=4,
                width=1024,
                height=768,
                n=1
            )

            # Obtém a URL da imagem gerada e faz o download
            imurl = response.data[0].url
            my_res = requests.get(imurl)
            my_img = Image.open(BytesIO(my_res.content))

            # Exibe a imagem na interface
            st.image(my_img, caption="Desenho Gerado")

            # Campo para inserir o nome do arquivo PDF (opcional)
            savename = st.text_input("Nome do arquivo PDF (ex: img.pdf):", value="img.pdf")

            # Converte a imagem para PDF em memória
            pdf_bytes = BytesIO()
            my_img.save(pdf_bytes, format='PDF')
            pdf_bytes.seek(0)

            # Botão para baixar o PDF diretamente
            st.download_button(
                label="Baixar Imagem em PDF",
                data=pdf_bytes,
                file_name=savename if savename else "img.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            # Exibe mensagens de erro em caso de falha
            st.error(f"Ocorreu um erro: {e}")
            st.info("Verifique se sua chave de API é válida em https://api.together.ai/settings/api-keys")
    else:
        st.warning("Por favor, forneça a chave de API e o tema do desenho.")