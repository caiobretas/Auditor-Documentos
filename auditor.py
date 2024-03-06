"""módulo que contém a classe responsável pela auditoria"""

import os
import asyncio
import datetime
from pandas import DataFrame
from main import (
    DOCUMENTS_PATH,
    contacts_mapping,
    docs_categories_mapping,
    docs_vigency_mapping,
    downloaded_files_mapping,
)
from models.compilers import DateCompiler, PartCompiler, VigencyCompiler
from models.system import System

date_compiler = DateCompiler()
part_compiler = PartCompiler()
vigency_compiler = VigencyCompiler()


class Auditor:
    """classe responsável por auditar os documentos"""

    def __init__(self):

        # # abaixo, vamos definir alguns mappings úteis
        self.result_mapping = {}

        self._files_to_audit = downloaded_files_mapping

    async def save_results(self, results: dict):
        """método responsável por salvar os resultados das auditorias no
        mapping de resultados"""
        for k, v in results.items():
            # verifica se a chave já existe no mapping de resultados
            if k in self.result_mapping:
                # se já estiver, busca ele e adiciona os valores
                self.result_mapping[k].update(v)
            else:
                # se não estiver, adiciona a chave e o valor
                self.result_mapping[k] = v

    async def audit_vigencies(self, document_path, google_id):
        # Compilador encontra a vigencia na string e compara com a informação do banco
        # Apenas os documentos das categorias abaixo serão analisados.
        accepted_categories = ("NDA",)

        document_cat = docs_categories_mapping[google_id]
        document = docs_vigency_mapping[google_id]

        vigency, vigency_status = "", ""

        if document_cat.categoria2 in accepted_categories:
            vigency, vigency_status = vigency_compiler.compile_vigency_model(
                document_path=document_path
            )
        else:
            vigency, vigency_status = None, "not accepted category"

        if isinstance(vigency, datetime.date):
            if vigency != document.datafinal_vigencia:
                vigency_status = "wrong vigency"

        result = {google_id: {"vigency": vigency, "vigency_status": vigency_status}}
        print(result)
        await self.save_results(result)

    async def audit_signature_date(self, document_str, google_id):
        # Compilador encontra a data na string.

        document = docs_vigency_mapping[google_id]

        date, date_status = "", ""
        date, date_status = date_compiler.compile_date_regexp(document_str=document_str)

        if isinstance(date, datetime.date):

            if date != document.data_assinatura:

                date_status = "wrong date"

        result = {google_id: {"date": date, "date_status": date_status}}
        print(result)
        await self.save_results(result)

    async def audit_parts(self, file_path, google_id):

        saved_part_id = docs_categories_mapping[google_id].categoria5
        saved_part = contacts_mapping.get(saved_part_id)

        if saved_part:  # busca tanto o nome qto o nome amigável
            saved_part_names = [saved_part.nomeamigavel, saved_part.nome]

        else:
            saved_part_names = [None, None]

        part, part_status = "", ""
        part, part_status = part_compiler.compile_part_model(
            file_path, *saved_part_names
        )

        if part in ("não", "no"):  # se não encontrar a parte no documento
            if not saved_part_id:  # e não tiver id da parte cadastrado no doc
                part, part_status = None, "no part found"
            part, part_status = saved_part.nomeamigavel, "wrong"

        result = {google_id: {"part": part, "part_status": part_status}}
        print(result)
        await self.save_results(result)

    async def _create_tasks(self):
        """método responsável por crias as coroutines"""

        tasks = [
            asyncio.create_task(self.async_audit(f"{DOCUMENTS_PATH}{file_path}.txt"))
            for file_path in downloaded_files_mapping
        ]

        await asyncio.gather(*tasks)

    async def async_audit(self, file_path):
        """método responsável por auditar os documentos (ASYNC)"""
        # lê o arquivo e retorna a string dele
        document_str = await System.async_read_file(file_path)
        google_id = file_path.split(".")[0].split("/")[1]

        # # estação de auditoria
        await asyncio.gather(
            # self.audit_signature_date(document_str, google_id),
            # self.audit_parts(file_path, google_id),
            self.audit_vigencies(file_path, google_id),
        )

    def audit(self):
        """método responsável por auditar os documentos"""
        asyncio.run(self._create_tasks())

    def report(self):
        """método responsável por gerar o relatório"""
        report_path = "result.xlsx"
        df = (
            DataFrame.from_dict(self.result_mapping, orient="index")
            .reset_index()
            .rename(columns={"index": "google_id"})
        )
        df.to_excel(report_path, index=False, engine="openpyxl")


auditor = Auditor()
auditor.audit()
auditor.report()

os.system("clear")
print("Audit finished!")
