"""módulo responsável por compilar strings de diferentes formatos"""

import re
from datetime import date, datetime
from pathlib import Path
from typing import Union

from openai import RateLimitError

from controllers.gpt import GPT
from entities.document_for_langchain import Document

PROMPTS_PATH = Path(__file__).parent.parent / "prompts.json"


class Compiler:
    """classe responsável por compilar strings de diferentes formatos"""

    def __init__(self):
        self._model = GPT()

    def __repr__(self):
        return f"{self.__class__.__name__}({self._model}())"


class PartCompiler(Compiler):
    """classe responsável por acionar o modelo de AI para identificar se uma
    parte pertence ou não a um documento"""

    def __init__(self):

        super().__init__()

        self.__prompt = """"
        Me diga se um dos nomes abaixo uma das partes principais que assinam o documento.

        Responda apenas sim ou não.

        Na dúvida, diga não.

        Nomes:
        """

    def compile_part_model(self, document_path, *parts):
        """retorna uma tupla com a parte e o status
        utiliza a classe GPT para compilar a string"""

        prompt = self.__prompt + f"\n\n{parts[0]}\n{parts[1]}"
        response = self._model.questions_and_answers_by_file(prompt, document_path)
        response = response["output_text"].strip().lower(), "ok"
        return response


class DateCompiler(Compiler):
    """classe responsável por compilar strings de diferentes formatos"""

    _date_patterns_ = [
        # Para o formato "DD/MM/YYYY"
        r"Rio de Janeiro," r"\s+(\d{2}/\d{2}/\d{4})",
        # Para o formato "DD de mês de YYYY"
        r"Rio de Janeiro,"
        r"\s+(\d{1,2})\s+de\s+(janeiro|fevereiro|março|abril|maio|junho|"
        r"julho|agosto|setembro|outubro|novembro|dezembro)\s+de\s+(\d{4})",
    ]

    _month_mapping = {
        "janeiro": "01",
        "jan": "01",
        "fevereiro": "02",
        "fev": "02",
        "março": "03",
        "mar": "03",
        "abril": "04",
        "abr": "04",
        "maio": "05",
        "mai": "05",
        "junho": "06",
        "jun": "06",
        "julho": "07",
        "jul": "07",
        "agosto": "08",
        "ago": "08",
        "setembro": "09",
        "set": "09",
        "outubro": "10",
        "out": "10",
        "novembro": "11",
        "nov": "11",
        "dezembro": "12",
        "dez": "12",
    }

    # def __init__(self):
    #     with open(PROMPTS_PATH, 'r', encoding='utf-8') as file:
    #         self._prompts = load(file)

    def compile_date_regexp(self, document_str) -> tuple:
        """responsável por compilar as datas encontradas
        os padrões são definidos antes do inicializador
        """

        compiled_patterns = [
            re.compile(padrao, re.IGNORECASE) for padrao in self._date_patterns_
        ]

        if not compiled_patterns:
            return None, "no date found"

        found_dates = []
        for comp_pattern in compiled_patterns:

            found_dates = list(set(comp_pattern.findall(document_str)))

            if not found_dates:
                response = None, "no date found"
                continue

            if len(found_dates) > 1:
                return found_dates, "more than one date"

            comp_date = found_dates[0]

            try:

                if not len(comp_date) == 3:  # Formato DD/MM/YYYY e DD/mês/YYYY
                    return comp_date, "unknown date format"

                day, month, year = comp_date

                month_number = self._month_mapping.get(month.lower(), month)

                date_str = f"{day}/{month_number}/{year}"

                obj = datetime.strptime(date_str, "%d/%m/%Y").date()

                response = obj, "ok"  # type:ignore

            except ValueError as ve:
                response = None, str(ve)  # type:ignore

        return response

    def compile_variables(self, category: str, file_path: str) -> Union[tuple, str]:
        """retorna uma tupla(data, cnpj/cpf)
        compila os prompts definidos em prompts.json dado o tipo do contrato
        """
        try:

            model_response = self._model.questions_and_answers_by_file(
                file_path=file_path,
                pydantic_object=Document,
                query=self._prompts[category.lower()],
            )

            compiled_date = datetime.strptime(model_response, "%d/%m/%Y").date()
            return compiled_date

        except ValueError as ve:
            return f"value error: {ve}"

        except IndexError as ie:
            return f"index error: {ie}"

        except RateLimitError as rle:
            return f"rate limit error: {rle}"

    def compile_date(self, file_path) -> Union[date, str]:
        """retorna um objeto datetime.date ou uma string de erro"""
        try:
            model_response = self._model.questions_and_answers_by_file(
                file_path=file_path, query=self._prompts["date"]
            )

            compiled_date = datetime.strptime(model_response, "%d/%m/%Y").date()
            return compiled_date

        except ValueError as ve:
            return f"value error: {ve}"

        except IndexError as ie:
            return f"index error: {ie}"

        except RateLimitError as rle:
            return f"rate limit error: {rle}"

    def compile_part(self) -> Union[str, None]:

        words = self.document_str.split()
        selected_text = ""

        token_count = 0
        for word in words:
            estimated_token_size = len(word) + 2.5
            if token_count + estimated_token_size > 4000:
                break
            selected_text += word + " "
            token_count += estimated_token_size

        else:
            selected_text = self.document_str

        gpt = GPT(
            role_content="""
                Vou te enviar a string de um documento.
                Extraia e retorne apenas o CNPJ/CPF
                ps: quero que retorne o CNPJ/CPF apenas da outra parte.
                ignore o CNPJ da Lumx Studios (42.887.120/0001-00)
                Certifique-se de fornecer as informações no seguinte formato:
                
                CNPJ/CPF: [CNPJ/CPF aqui]
                ps: deve ser enviado como INTEIRO (sem pontos ou formatações)"""
        )
        response = gpt.ask(selected_text)
        cpf_cnpj = re.search(r"CNPJ/CPF: (.*?)", str(response))
        return cpf_cnpj


class VigencyCompiler(Compiler):
    """classe responsável por acionar o modelo de AI para identificar se a vigência de um documento está correta ou não"""

    def __init__(self):
        super().__init__()
        self.__prompt = """"
        Nosso objetivo aqui é identificar a data que a vigência acaba.
        Normalmente é encontrada em uma clausula específica de vigência
        
        Se a vigência começar a valer a partir de data de assinatura, a resposta deve ser: 
        Resposta = Data de assinatura + tempo de vigência.
       
        Se não, a resposta deve ser
        Resposta = Data inicio vigência + tempo vigência.
        
        Se estiver explícito a data final da vigência, a resposta deve ser:
        Resposta = Data final vigencia.

        Responda apenas se tiver certeza.
        
        A resposta deve conter APENAS o solicitado no formato dd/mm/aaaa.
        Ex: Resposta do Chat GPT:
        20/02/2001
        """

    def compile_vigency_model(self, document_path):
        """retorna uma tupla com a vigência e o status
        utiliza a classe GPT para compilar a string"""

        prompt = self.__prompt
        response = self._model.questions_and_answers_by_file(prompt, document_path)
        response = response["output_text"].strip().lower()
        try:
            formatted_response = datetime.strptime(response, "%d/%m/%Y").date(), "ok"
        except ValueError:
            formatted_response = None, "unknown date format"
        return formatted_response


class BoardAssemblyCompiler(Compiler):
    """classe responsável por acionar o modelo de AI para identificar se a assembleia de um documento está correta ou não"""

    def __init__(self, board_assembly_mapping):

        super().__init__()

        self._summarize_prompt = """
        Avalie se o trecho abaixo contém uma assembleia de sócios
        
        Responda apenas sim ou não.

        Na dúvida, diga não.
        
        Trecho:
        """

        # self.

    def resume_and_summarize_board_assembly(self, board_assembly_docs_path):
        """utiliza a classe GPT para resumir a pauta da ata"""

        response = self._model.summarize(
            self._summarize_prompt, board_assembly_docs_path
        )
        response = response["output_text"].strip().lower()
        if response.lower() == "não":
            response = False
        else:
            response = True
        return response

    def compile_board_assembly_model(self, document_path):
        """utiliza a classe GPT para compilar a string"""

        response = self._model.questions_and_answers_by_file(
            self.__prompt, document_path
        )
        response = response["output_text"].strip().lower()
        if response.lower() == "não":
            response = False
        else:
            response = True
        return response


class ExclusivityCompiler(Compiler):

    def __init__(self):

        super().__init__()

        self.__prompt = """
        Avalie se o trecho abaixo contém cláusulas de exclusividade
        
        Responda apenas sim ou não.

        Na dúvida, diga não.
        
        Trecho:
        """

    def compile_exclusivity_model(self, document_path):
        """utiliza a classe GPT para compilar a string"""

        response = self._model.questions_and_answers_by_file(
            self.__prompt, document_path
        )
        response = response["output_text"].strip().lower()
        if response.lower() == "não":
            response = False
        else:
            response = True
        return response
