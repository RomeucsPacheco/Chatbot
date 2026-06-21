# Corporate Chatbot - Manual do Renault Clio

Este projeto é um chatbot educacional desenvolvido para o projeto final da disciplina de introdução a inteligencia artificial. Ele utiliza a técnica de RAG (**Retrieval-Augmented Generation**) para ler, processar e responder perguntas exclusivamente com base em um documento PDF fornecido (o manual do proprietário do Renault Clio).

O projeto prioriza código limpo, linear e altamente explicativo, utilizando **Python**, **Streamlit** (para interface), **LangChain** (para orquestração do RAG) e a API do **Google Gemini** em conjunto com **HuggingFace** (para contornar limitações de taxa gratuita).

## Pré-requisitos

- Python 3.9 ou superior instalado na máquina.
- Uma chave de API do Google Gemini. Se você não tem uma, pode gerá-la gratuitamente no [Google AI Studio](https://aistudio.google.com/).

## Como Instalar e Rodar o Projeto

1. **Clone o repositório e acesse a pasta:**
   ```bash
   git clone https://github.com/RomeucsPacheco/Chatbot.git
   cd Chatbot
   ```

2. **(Recomendado) Crie e ative um ambiente virtual:**
   Para garantir que as dependências do projeto não entrem em conflito com outros projetos Python na sua máquina.
   ```bash
   python -m venv venv
   
   # No Windows:
   venv\Scripts\activate
   
   # No Mac/Linux:
   source venv/bin/activate
   ```

3. **Instale as bibliotecas necessárias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure sua chave da API:**
   Como as chaves não são enviadas ao GitHub por segurança, você precisará configurar a sua. Crie um arquivo chamado `.env` na raiz do projeto e adicione a chave gerada:
   ```env
   GOOGLE_API_KEY=sua_chave_aqui
   ```

5. **Execute a aplicação:**
   ```bash
   streamlit run app.py
   ```
   *Ao rodar este comando, o navegador padrão será aberto com a interface da aplicação. O arquivo `manual.pdf` já está incluso no repositório e será lido automaticamente.*

## Como usar a aplicação

1. Com a aplicação aberta, o sistema processará o documento `manual.pdf` automaticamente (leitura, divisão de texto e vetorização usando modelos multilingues). Ele usará cache para não precisar ler o PDF toda vez.
2. No campo de texto central, digite sua pergunta (ex: "Qual a pressão correta dos pneus?").
3. **Regra de Ouro (Anti-alucinação):** A inteligência artificial foi instruída de forma estrita para só usar as informações do PDF. Se a resposta não estiver no manual (ex: como emparelhar Bluetooth, que costuma ficar em um manual separado do rádio), ela responderá exatamente: *"Não encontrei essa informação no manual"*.


