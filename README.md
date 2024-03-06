# Projeto de Auditoria de Documentos

## Descrição
Este repositório contém o código para um sistema automatizado de auditoria de documentos.
O sistema consulta um banco de dados para obter metadados e Google IDs de documentos armazenados no Google Drive, baixa os bytes, transforma em string, e audita as informações com a API da Open AI e Regexp.

## Funcionalidades
- Consulta automática a banco de dados de documentos.
- Manejo do banco de dados com a SQLALCHEMY ORM
- Integração com a Google Drive API para acesso e download de documentos PDF.
- Extração de texto de documentos PDF usando PyMuPDF.
- Processamento e análise de texto utilizando a OpenAI API.
- Notificação de resultados via e-mail e SMS usando a Gmail API.

## Pré-requisitos
- Python 3.9+
- Conta no Google Cloud com acesso à Google Drive e Gmail API
- Acesso à API da OpenAI
<!-- - Instalação e Execução Ollama AI -->

## Configuração
- Personalizar as entidades conforme necessidade em entities/
- Personalizar as classes de repositório dado as entidades em repositories/
- Personalizar os padrões dos compilers em models/compilers

### Instalação de Dependências
Instale todas as dependências necessárias com o seguinte comando:
```bash
pip install --upgrade -r requirements.txt