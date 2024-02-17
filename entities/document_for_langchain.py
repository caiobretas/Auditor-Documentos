from langchain_core.pydantic_v1 import BaseModel, Field


# alterar nome para documento e cadastrar os atributos
class Document(BaseModel):

    cpf_cnpj: str = Field(description='campo destinado ao cpf/cnpj')
    data: str = Field(description='campo destinado para a data')
