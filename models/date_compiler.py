'''módulo responsável por compilar datas de diferentes formatos'''
import logging
import re
from datetime import datetime


class DateCompiler:
    '''classe responsável por compilar datas de diferentes formatos'''
    _patterns = [
        # Para o formato "DD/MM/YYYY"
        r"Rio de Janeiro,"
        r"\s+(\d{2}/\d{2}/\d{4})",
        # Para o formato "DD de mês de YYYY"
        r"Rio de Janeiro,"
        r"\s+(\d{1,2})\s+de\s+(janeiro|fevereiro|março|abril|maio|junho|"
        r"julho|agosto|setembro|outubro|novembro|dezembro)\s+de\s+(\d{4})"
    ]

    _month_mapping = {

        'janeiro': '01', 'jan': '01',
        'fevereiro': '02', 'fev': '02',
        'março': '03', 'mar': '03',
        'abril': '04', 'abr': '04',
        'maio': '05', 'mai': '05',
        'junho': '06', 'jun': '06',
        'julho': '07', 'jul': '07',
        'agosto': '08', 'ago': '08',
        'setembro': '09', 'set': '09',
        'outubro': '10', 'out': '10',
        'novembro': '11', 'nov': '11',
        'dezembro': '12', 'dez': '12'
    }

    def __init__(self, document_str, document_id):
        self.document_id = document_id
        self.document_str = document_str

    def compile_dates(self):
        '''responsável por compilar as datas encontradas
        os padrões são definidos antes do inicializador
        '''

        compiled_patterns = [
            re.compile(padrao, re.IGNORECASE) for padrao in self._patterns]

        found_dates = set()
        not_found_dates = set()

        for comp_pattern in compiled_patterns:
            for comp_date in comp_pattern.findall(self.document_str):
                try:
                    # as vezes o doc tem 2 datas de assinatura
                    # ex 1QpYUQF0cjmYdVghoZ0n-mHjB4C60NLOv
                    if len(comp_date) == 3:  # Formato DD/MM/YYYY e DD/mês/YYYY
                        day, month, year = comp_date
                        month_number = self._month_mapping.\
                            get(month.lower(), month)
                        date_str = f'{day}/{month_number}/{year}'
                        date = datetime.strptime(date_str, '%d/%m/%Y').date()
                        found_dates.add((self.document_id, date))

                except ValueError as e:
                    logging.\
                        error('Erro processando a data: %s - %s', comp_date, e)
                    not_found_dates.add((self.document_id, None))

        return found_dates
