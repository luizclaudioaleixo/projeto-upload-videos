import streamlit as st
import os
from pathlib import Path

# Configure Streamlit before any other Streamlit calls (required)
st.set_page_config(page_title="Página Principal", page_icon="🏠")

# Example credentials (replace with secure storage in production)
USERS = {"admin": "admin", "user": "user"}

def login_page():
    st.title("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

    if submit_button:
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in successfully!")
            # Atualiza o estado para simular um redirecionamento
            st.session_state.page = "main"
        else:
            st.error("Invalid username or password.")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.page == "login" and not st.session_state.logged_in:
    login_page()
else:
    # Display your main application content here or redirect
    
    # Define o cabeçalho com a imagem
    def set_header_with_image():
        st.markdown(
            """
            <style>
            .header {
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #4B0082; /* Cor de fundo do cabeçalho */
                padding: 10px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        # Exibe a imagem no cabeçalho com largura ajustada
        # Resolve caminho relativo à raiz deste arquivo
        base_dir = Path(__file__).parent
        image_path = base_dir / "imagens" / "backend.jpeg"
        if image_path.exists():
            st.image(str(image_path), use_container_width=True)
        else:
            st.write("[Imagem não encontrada]")

    # Aplica o cabeçalho com a imagem
    set_header_with_image()

    # Função para logout
    def logout():
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.page = "login"

    # Adiciona o botão "Logout" e a mensagem "Welcome," ao lado direito da página
    def add_header_with_logout_and_welcome():
        st.markdown(
            f"""
            <style>
            .header-container {{
                display: flex;
                justify-content: flex-end;
                align-items: center;
                background-color: #4B0082; /* Cor de fundo do cabeçalho */
                padding: 10px;
                color: white;
            }}
            .header-container .welcome-message {{
                margin-right: 20px;
                font-size: 16px;
            }}
            .header-container .logout-button {{
                background-color: white;
                color: #4B0082;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 14px;
            }}
            .header-container .logout-button:hover {{
                background-color: #f0f0f0;
            }}
            </style>
            <div class="header-container">
                <span class="welcome-message">Welcome, {st.session_state.username}!</span>
            </div>
            """,
            unsafe_allow_html=True
        )


        cols = st.columns(2)  # Cria 2 colunas para exibição dos vídeos
        col = cols[1 % 2]  # Alterna entre as colunas
        with col:
              with st.container():
                col1, col2 = st.columns(2)
                with col2:
                    # Botão de logout usando Streamlit
                    if st.button("Logout", key="logout_button"):
                        logout()  # Chama a função logout diretamente
                

    # Chama a função para adicionar o cabeçalho com o botão de logout e a mensagem de boas-vindas
    add_header_with_logout_and_welcome()

    # Adiciona estilo CSS para alterar a cor de fundo e a cor do texto
    def set_background_and_text_color():
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #4B0082; /* Define o fundo da página como branco */
            }
            html, body, [class*="css"] {
                color: black; /* Define a cor do texto como preto */
            }
            h1, h2, h3, h4, h5, h6 {
                color: black; /* Define a cor dos títulos como preto */
            }
            .stMarkdown {
                color: black; /* Define a cor do texto em markdown como preto */
            }
            .stButton > button, .stDownloadButton > button {
                color: black; /* Define a cor do texto dos botões como preto */
                background-color: white; /* Fundo branco */
                border: 1px solid #ccc; /* Borda cinza */
                border-radius: 5px; /* Bordas arredondadas */
                padding: 5px 10px; /* Espaçamento interno */
                font-size: 14px; /* Tamanho da fonte */
                cursor: pointer; /* Cursor de ponteiro */
            }
            .stButton > button:hover, .stDownloadButton > button:hover {
                background-color: #f0f0f0; /* Fundo cinza claro ao passar o mouse */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    class Main:
        def __init__(self, upload_dir="uploads", max_files=6, max_file_size_mb=100):
            self.upload_dir = upload_dir
            self.max_files = max_files
            self.max_file_size_mb = max_file_size_mb

            # Cria o diretório de upload se não existir (caminho relativo ao arquivo)
            base_dir = Path(__file__).parent
            self.upload_dir = str(base_dir / self.upload_dir)
            if not os.path.exists(self.upload_dir):
                os.makedirs(self.upload_dir, exist_ok=True)

        def get_uploaded_files(self):
            """Retorna a lista de arquivos já presentes no diretório de upload."""
            return [f for f in os.listdir(self.upload_dir) if f.endswith(".mp4")]

        def upload_file(self, file, file_name):
            """Faz o upload de um arquivo .mp4, respeitando as restrições."""
            if not file_name.endswith(".mp4"):
                return "Erro: Apenas arquivos .mp4 são permitidos."

            # Verifica o tamanho do arquivo
            file_size_mb = len(file.getvalue()) / (1024 * 1024)  # Converte para MB
            if file_size_mb > self.max_file_size_mb:
                return f"Erro: O arquivo excede o limite de {self.max_file_size_mb}MB."

            # Verifica o número de arquivos já presentes
            uploaded_files = self.get_uploaded_files()
            if len(uploaded_files) >= self.max_files:
                return f"Erro: O limite de {self.max_files} vídeos foi atingido."

            # Copia o arquivo para o diretório de upload
            destination_path = os.path.join(self.upload_dir, file_name)

            # Verifica se o arquivo já existe
            if os.path.exists(destination_path):
                return f"Erro: O arquivo '{file_name}' já existe no diretório de upload."

            try:
                with open(destination_path, "wb") as dest:
                    dest.write(file.getvalue())
                return f"Sucesso: O arquivo '{file_name}' foi enviado."
            except Exception as e:
                return f"Erro: Não foi possível enviar o arquivo. Detalhes: {e}"

        def delete_file(self, file_name):
            """Exclui um arquivo do diretório de upload."""
            file_path = os.path.join(self.upload_dir, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                return f"Sucesso: O arquivo '{file_name}' foi excluído."
            else:
                return f"Erro: O arquivo '{file_name}' não foi encontrado."

        def preview_videos(self):
            """Exibe uma prévia dos vídeos no diretório de upload agrupados em 2 colunas por 3 linhas."""
            uploaded_files = self.get_uploaded_files()
            if uploaded_files:
                st.markdown('<h3 style="color: black;">Prévia dos vídeos:</h3>', unsafe_allow_html=True)
                cols = st.columns(2)  # Cria 2 colunas para exibição dos vídeos
                for idx, file in enumerate(uploaded_files[:6]):  # Limita a exibição a 6 vídeos
                    video_path = os.path.join(self.upload_dir, file)
                    col = cols[idx % 2]  # Alterna entre as colunas
                    with col:
                        st.video(video_path)
                        # Botões de download e exclusão (somente para admin)
                        if st.session_state.username == "admin":
                            with st.container():
                                col1, col2 = st.columns(2)
                                with col1:
                                    with open(video_path, "rb") as video_file:
                                        video_bytes = video_file.read()
                                        st.download_button(
                                            label=f"Baixar {file}",
                                            data=video_bytes,
                                            file_name=file,
                                            mime="video/mp4"
                                        )
                                with col2:
                                    if st.button(f"Excluir {file}", key=f"delete_{file}"):
                                        result = self.delete_file(file)
                                        st.success(result)
                                        # Atualiza o estado para simular um recarregamento
                                        st.session_state["deleted"] = True

            else:
                st.write("Nenhum vídeo disponível para prévia.")

    # Streamlit App
    set_background_and_text_color()  # Define a cor de fundo para branco e texto para preto

    # Define o título com estilo inline para garantir a cor preta
    #st.markdown('<h1 style="color: black;">Upload de Vídeos (.mp4)</h1>', unsafe_allow_html=True)
    if st.session_state.username == "admin":
        # Define a descrição com estilo inline para garantir a cor preta
        st.markdown('<p style="color: black;">Faça o upload de vídeos com no máximo 100MB. O limite é de 6 vídeos.</p>', unsafe_allow_html=True)

    main = Main()

    # Exibe a prévia dos vídeos
    main.preview_videos()

    # Formulário para upload (somente para admin)
    if st.session_state.username == "admin":
        st.markdown('<h3 style="color: black;">Enviar novo vídeo:</h3>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader('<p style="color: black;">Escolha um arquivo .mp4</p>', type=["mp4"], label_visibility="collapsed")

        if uploaded_file is not None:
            file_name = uploaded_file.name
            result = main.upload_file(uploaded_file, file_name)
            st.write(result)
