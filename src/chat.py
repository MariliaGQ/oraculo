import streamlit as st

MENSAGENS_EXEMPLO = [
    ('user', 'Olá'),
    ('assistant', 'Tudo bem?'),
    ('user', 'tudo certo')
]

CONFIG_MODELOS =  {'Groq': {'modelos':['gemma2-9b-it', 'llama-3.3-70b-versatile']},
                    'OpenAI': {'modelos': ['gpt-4o-mini', 'gpt-4o']}}

TIPOS_ARQUIVOS_VALIDOS = [
    'Site',
    'Youtube',
    'PDF',
    'CSV',
    'TXT'
]


def pagina_chat():
    st.header('🤖 Bem-vindo ao Oráculo', divider = True)

    mensagens = st.session_state.get('mensagens', MENSAGENS_EXEMPLO)

    for mensagem in mensagens:
        chat = st.chat_message(mensagem[0])
        chat.markdown(mensagem[1])

    input_usuario = st.chat_input('Digite sua mensagem aqui...')
    if input_usuario:
        # Adiciona a mensagem do usuário à lista de mensagens
        mensagens.append(('user', input_usuario))
        st.session_state['mensagens'] = mensagens
        st.rerun()

def sidebar():
    tabs = st.sidebar.tabs(['Upload Arquivos', 'Seleção de Modelos'])  
    with tabs[0]:
        tipo_arquivo = st.selectbox("Selecione o tipo de arquivo", TIPOS_ARQUIVOS_VALIDOS) 
        if tipo_arquivo == 'Site':
            arquivo = st.text_input("Cole o link do site aqui")
        if tipo_arquivo == 'Youtube':
            arquivo = st.text_input("Cole o link do vídeo aqui")           
        if tipo_arquivo == 'PDF':
            arquivo = st.file_uploader("Envie o arquivo PDF aqui", type='pdf')
        if tipo_arquivo == 'CSV':
            arquivo = st.file_uploader("Envie o arquivo CSV aqui", type='csv')
        if tipo_arquivo == 'TXT':
            arquivo = st.file_uploader("Envie o arquivo TXT aqui", type='txt')
    with tabs[1]:
        provedor = st.selectbox("Selecione o provedor", CONFIG_MODELOS.keys())
        modelo = st.selectbox("Selecione o modelo", CONFIG_MODELOS[provedor]['modelos'])
        api_key = st.text_input("Cole sua chave de API aqui", value=st.session_state.get(f'api_key_{provedor}', ''))

        st.session_state[f'api_key_{provedor}'] = api_key
     


def main():
    pagina_chat()
    with st.sidebar:
        sidebar()


if __name__ == '__main__':
    main()