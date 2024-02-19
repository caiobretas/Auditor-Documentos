'''módulo responsável por interações com o sistema operacional'''

import os

import aiofiles


class System:
    '''Classe responsável por interações com o sistema operacional'''

    @staticmethod
    def get_files(folder_path) -> list[str]:
        '''retorna uma lista com os files em um diretório'''
        return os.listdir(folder_path)

    @staticmethod
    async def async_read_file(file_path):
        '''retorna o conteúdo de um arquivo de forma async'''
        async with aiofiles.open(file_path, 'r') as f:
            return await f.read()

    @staticmethod
    def read_file(file_path) -> str:
        '''retorna o conteúdo de um arquivo'''
        with open(file_path, 'r', encoding='utf8') as archive:
            return archive.read()
