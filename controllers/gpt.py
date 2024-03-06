"""módulo de controller"""

import os

from langchain.chains.question_answering import load_qa_chain
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders.unstructured import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms.ollama import Ollama
from langchain_openai import OpenAI
from openai import BadRequestError  # , RateLimitError

KEY = os.environ.get("OPENAI_API_KEY")


class Model:
    """classe base para modelos de AI.
    Utiliza como modelo printipal o da OpenAI.
    Se der erro de rate-limit ele usa o do Ollama
    (precisa fazer o download: https://ollama.com/download)
    """

    def __init__(self):

        # self.document = None  # é preciso rodar _load_document

        self.llm = OpenAI(api_key=KEY, temperature=0.0)  # type:ignore
        self.backup_llm = Ollama(model="llama2")

    def _load_document(self, file_path: str):
        """método responsável por carregar o documento"""
        _loader = UnstructuredFileLoader(file_path)
        return _loader.load()

    # def _summarize_map_reduce(self):
    #     """cria uma chain com type = "map_reduce"
    #     esse método resume o conteúdo do documento
    #     Ideal para documentos grandes"""
    #     if not self.document:
    #         raise ValueError("Document not loaded")
    #     chain = load_summarize_chain(
    #         self.llm,
    #         chain_type="map_reduce",
    #         verbose=False,  # verbose=True mostra o que Langchain faz por baixo
    #     )
    #     try:
    #         return chain.invoke(self.document)
    #     except BadRequestError:
    #         txt_splitter = RecursiveCharacterTextSplitter(
    #             chunk_size=4000, chunk_overlap=0
    #         )
    #         return txt_splitter.split_documents(self.document)

    # def _summarize_stuff(self, query=None):
    #     """cria uma chain com type = "stuff"
    #     esse método resume o conteúdo do documento
    #     Não é o ideal para documentos grandes"""
    #     if not self.document:
    #         raise ValueError("Document not loaded")
    #     chain = load_summarize_chain(
    #         self.llm,
    #         chain_type="stuff",
    #         verbose=False,  # verbose=True mostra o que Langchain faz por baixo
    #     )

    #     try:
    #         invocation = {"input_documents": self.document}

    #         if query:
    #             invocation["query"] = query

    #         return chain.invoke(invocation)

    #     except BadRequestError:
    #         txt_splitter = RecursiveCharacterTextSplitter(
    #             chunk_size=4000, chunk_overlap=0
    #         )
    #         return txt_splitter.split_documents(self.document)

    def split_documents(self, file_path):
        """método responsável por dividir o documento em partes"""
        documents = self._load_document(file_path)

        txt_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
        splitted_documents = txt_splitter.split_documents(documents)

        if not splitted_documents:
            raise ValueError("No documents found - Path ", file_path)

        return splitted_documents

    def _map_rerank(self, query: str, documents):
        """cria uma chain com type = "map_rerank"
        esse método calcula a % de assertividade dado a pergunta feita
        (modelo Q&A) e retorna a resposta mais assertiva"""

        chain = load_qa_chain(self.llm, chain_type="map_rerank", verbose=False)

        return chain.invoke({"input_documents": documents, "question": query})


class GPT(Model):
    """classe responsável pelas requisições com a OpenAI"""

    def questions_and_answers_by_file(self, query, file_path: str):
        """método responsável por fazer perguntas ao modelo
        ideal para Q&A"""
        documents = self.split_documents(file_path)
        # try:
        return self._map_rerank(query, documents)

    # def ask(self, user_content: str):
    #     '''método reponsável por fazer perguntas ao modelo'''

    #     completion = self.client.chat.completions.create(
    #         model=MODEL,
    #         messages=[
    #             {'role': 'system', 'content': self._role_content},
    #             {'role': 'user', 'content': user_content}
    #         ]
    #     )
    #     return completion.choices[0].message


# if __name__ == '__main__':
#     os.system('clear')
#     gpt = GPT()
#     role_content = '''
#     A sua resposta deve ser composta de apenas 1 palavra, sempre.
#     dê a data de assinatura.
#     '''
#     gpt.ask('Rio de Janeiro, 11/02/2023')
