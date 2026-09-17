# API Imobiliária

Projeto 2 de Programação Eficaz. Uma API RESTful feita em Flask que responde em
JSON com os imóveis de uma empresa imobiliária. Os dados ficam guardados num
MySQL hospedado na Aiven, e a API está no ar numa EC2 da AWS.

API no ar: http://3.85.232.176/imoveis

## Rotas

| Método | Rota | O que faz | Códigos |
|--------|------|-----------|---------|
| GET | /imoveis | lista todos os imóveis | 200, 404 |
| GET | /imoveis/\<id\> | um imóvel pelo id | 200, 404 |
| POST | /imoveis | cadastra um imóvel | 201, 400 |
| PUT | /imoveis/\<id\> | atualiza um imóvel | 200, 400, 404 |
| DELETE | /imoveis/\<id\> | remove um imóvel | 204, 404 |
| GET | /imoveis/tipo/\<tipo\> | imóveis de um tipo | 200, 404 |
| GET | /imoveis/cidade/\<cidade\> | imóveis de uma cidade | 200, 404 |

Toda resposta com imóvel traz um campo `_links` apontando para o próprio
recurso, para a lista completa e para as buscas por tipo e por cidade.

Exemplo de `GET /imoveis/1`:

    {
      "id": 1,
      "logradouro": "Nicole Common",
      "tipo_logradouro": "Travessa",
      "bairro": "Lake Danielle",
      "cidade": "Judymouth",
      "cep": "85184",
      "tipo": "casa em condominio",
      "valor": 488424.0,
      "data_aquisicao": "2017-07-29",
      "_links": {
        "self": "/imoveis/1",
        "todos": "/imoveis",
        "tipo": "/imoveis/tipo/casa%20em%20condominio",
        "cidade": "/imoveis/cidade/Judymouth"
      }
    }

Para cadastrar ou atualizar, o corpo é um JSON com os oito campos acima
(sem o `id`).

## Como rodar

Instale as dependências:

    pip install -r requirements.txt

Crie um arquivo `.env` na raiz seguindo o `.env.example`, com as credenciais
do banco. Depois:

    python app.py

A API fica disponível em http://localhost:5000.

## Testes

    pytest

Os testes usam mock da conexão, então rodam sem banco.
