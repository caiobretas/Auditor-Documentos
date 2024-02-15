import os


class SystemReader:
    '''Classe responsável por interações com o sistema operacional'''

    @staticmethod
    def get_files(folder_path) -> list[str]:
        '''retorna uma lista com os files em um diretório'''
        return os.listdir(folder_path)

    @staticmethod
    def read_file(file_path) -> str:
        '''retorna o conteúdo de um arquivo'''
        with open(file_path, 'r', encoding='utf8') as archive:
            return archive.read()


if __name__ == '__main__':
    for file in SystemReader.get_files('documents'):
        print(file.split('.')[0],)
