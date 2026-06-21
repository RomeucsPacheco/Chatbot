import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# Passo 1: Carregar variáveis de ambiente do arquivo .env
# Carrega a sua GOOGLE_API_KEY automaticamente de forma segura
load_dotenv()

# Configuração da página do Streamlit (deve ser o primeiro comando do app)
st.set_page_config(page_title="Chatbot Renault Clio", page_icon="🚗")

st.title("🚗 Chatbot do Manual do Renault Clio")
st.write("Faça perguntas e tire dúvidas baseadas no manual do proprietário.")

# Caminho para o PDF local que já está na pasta do projeto
pdf_path = "manual.pdf"

# Verificamos se o arquivo realmente existe na pasta
if not os.path.exists(pdf_path):
    st.error(f"Erro: O arquivo '{pdf_path}' não foi encontrado na pasta do projeto.")
else:
    # O Streamlit roda todo o script de cima a baixo cada vez que interagimos. 
    # O cache impede que o PDF seja re-lido e vetorizado a cada nova pergunta, economizando tempo e dinheiro!
    @st.cache_resource(show_spinner="Lendo e processando o manual do Renault Clio...")
    def setup_rag_chain():
        # Passo 2: Carregar o documento PDF diretamente do disco
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        
        # Passo 3: Dividir o texto em pedaços menores (Chunks)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        
        # Passo 4: Criar Embeddings e o Banco de dados vetorial (FAISS)
        embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
        vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
        
        # Passo 5: Criar o "Retriever" (Buscador)
        # Faz a busca nos chunks do manual e retorna os 6 mais relevantes para a pergunta do usuário
        retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
        
        # Passo 6: Definir o modelo de Inteligência Artificial (LLM) - Gemini
        llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)
        
        # Passo 7: Criar o Prompt estrito (Regra Anti-alucinação)
        system_prompt = (
            "Você é um assistente virtual especialista no manual do Renault Clio. "
            "Use os seguintes trechos de contexto recuperado do manual para responder à pergunta. "
            "Se você não souber a resposta ou se a informação não estiver no contexto abaixo, "
            "você DEVE responder EXATAMENTE com a frase: 'Não encontrei essa informação no manual'. "
            "Não tente adivinhar, não invente informações e não use conhecimentos externos sob nenhuma circunstância. "
            "\n\n"
            "Contexto:\n{context}"
        )
        
        prompt = PromptTemplate(
            input_variables=["context", "input"],
            template=system_prompt + "\n\nPergunta do usuário: {input}\nResposta:"
        )
        
        # Passo 8: Criar a corrente (Chain) RAG
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        return rag_chain

    # Inicializa o robô usando a função protegida pelo cache
    try:
        rag_chain = setup_rag_chain()
        st.success("O Chatbot está pronto!")
        
        # Passo 9: Interface de Chat (Interação com o usuário)
        user_question = st.text_input("O que você deseja saber sobre o seu Renault Clio?")
        
        if user_question:
            with st.spinner("Buscando no manual..."):
                # Executa a corrente RAG passando a pergunta digitada
                response = rag_chain.invoke({"input": user_question})
                
                # Exibe a resposta final gerada pela IA
                st.write("### Resposta:")
                st.write(response["answer"])
                
                # Transparência: Mostrar as fontes exatas (chunks)
                with st.expander("Ver fontes (Trechos do manual recuperados)"):
                    for i, doc in enumerate(response["context"]):
                        st.write(f"**Trecho {i+1} (Página {doc.metadata.get('page', 'Desconhecida')}):**")
                        st.write(doc.page_content)
                        st.divider()
    except Exception as e:
        st.error(f"Ocorreu um erro ao inicializar a IA. Verifique sua chave de API. Erro: {e}")
