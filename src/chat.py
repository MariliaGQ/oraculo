import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

CONFIG_MODELOS =  {'Groq': {'modelos':['gemma2-9b-it', 'llama-3.3-70b-versatile'], 'chat': ChatGroq},
                    'OpenAI': {'modelos': ['gpt-4o-mini', 'gpt-4o'], 'chat': ChatOpenAI}}

TIPOS_ARQUIVOS_VALIDOS = [
    'Site',
    'Youtube',
    'PDF',
    'CSV',
    'TXT'
]

MEMORIA = ConversationBufferMemory()

def carrega_modelo(provedor, modelo, api_key):
    chat = CONFIG_MODELOS[provedor]['chat'](model =modelo, api_key=api_key)
    st.session_state['chat'] = chat
    
def pagina_chat():
    st.header('🤖 Bem-vindo ao Oráculo', divider = True)

    chat_model = st.session_state.get('chat')

    memoria = st.session_state.get('memoria', MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    input_usuario = st.chat_input('Digite sua mensagem aqui...')
    if input_usuario:
        # Adiciona a mensagem do usuário à lista de mensagens
        
        chat = st.chat_message('human')
        chat.markdown(input_usuario)

        chat = st.chat_message('ai')
        resposta = chat.write_stream(chat_model.stream(input_usuario))

        memoria.chat_memory.add_user_message(input_usuario)
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria'] = memoria
        #st.rerun()

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
    
    if st.button('Carregar oraculo', use_container_width=True):
        carrega_modelo(provedor, modelo, api_key) 


def main():
    with st.sidebar:
        sidebar()
    pagina_chat()    


if __name__ == '__main__':
    main()