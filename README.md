# Projeto de Auditoria de Documentos

## Descrição
Este repositório contém o código para um sistema automatizado de auditoria de documentos. O sistema consulta um banco de dados para obter metadados e IDs de documentos armazenados no Google Drive, baixa esses documentos, extrai o texto e utiliza a OpenAI API para auditar as informações contidas nos documentos.

## Funcionalidades
- Consulta automática a banco de dados de documentos.
- Integração com a Google Drive API para acesso e download de documentos PDF.
- Extração de texto de documentos PDF usando PyMuPDF.
- Processamento e análise de texto utilizando a OpenAI API.
- Notificação de resultados via e-mail e SMS usando a Twilio API.

## Pré-requisitos
- Python 3.9+
- Conta no Google Cloud com acesso à Google Drive API
- Acesso à API da OpenAI
- Credenciais para a Twilio API

## Configuração

### Instalação de Dependências
Instale todas as dependências necessárias com o seguinte comando:
```bash
pip install -r requirements.txt
