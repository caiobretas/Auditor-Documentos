'''módulo de controller'''
import os

from openai import OpenAI

KEY = os.environ.get('OPENAI_API_KEY')
MODEL='gpt-3.5-turbo'


class GPT:
    '''classe responsável pelas requisições com a OpenAI'''
    def __init__(self):
        self.client = OpenAI(api_key=KEY)

    def ask(self,
            user_content: str,
            role_content: str = 'Você é um assistente'):
        '''método reponsável por fazer perguntas ao modelo'''

        completion = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {'role': 'system', 'content': role_content},
                {'role': 'user', 'content': user_content}
            ]
        )
        print(completion.choices[0].message)

# if __name__ == '__main__':
#     os.system('clear')
#     gpt = GPT()
#     role_content = '''
#     A sua resposta deve ser composta de apenas 1 palavra, sempre.
#     dê a data de assinatura.
#     '''
#     gpt.ask('Rio de Janeiro, 11/02/2023')

