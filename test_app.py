from unittest.mock import MagicMock, patch

import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


IMOVEL = {
    "id": 1,
    "logradouro": "das Flores",
    "tipo_logradouro": "Rua",
    "bairro": "Centro",
    "cidade": "Sao Paulo",
    "cep": "01000-000",
    "tipo": "apartamento",
    "valor": 450000.0,
    "data_aquisicao": "2023-05-10",
}


@patch("app.conecta")
def test_listar_imoveis(mock_conecta, client):
    # Given
    mock_conexao = MagicMock()
    mock_cursor = MagicMock()
    mock_conexao.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [IMOVEL]
    mock_conecta.return_value = mock_conexao

    # When
    resposta = client.get("/imoveis")

    # Then
    assert resposta.status_code == 200
    assert resposta.get_json() == [IMOVEL]
    mock_cursor.execute.assert_called_once_with("SELECT * FROM imoveis")


@patch("app.conecta")
def test_listar_imoveis_sem_resultado(mock_conecta, client):
    # Given
    mock_conexao = MagicMock()
    mock_cursor = MagicMock()
    mock_conexao.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    mock_conecta.return_value = mock_conexao

    # When
    resposta = client.get("/imoveis")

    # Then
    assert resposta.status_code == 404
    assert resposta.get_json() == {"erro": "nenhum imovel encontrado"}


@patch("app.conecta")
def test_buscar_imovel(mock_conecta, client):
    # Given
    mock_conexao = MagicMock()
    mock_cursor = MagicMock()
    mock_conexao.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = IMOVEL
    mock_conecta.return_value = mock_conexao

    # When
    resposta = client.get("/imoveis/1")

    # Then
    assert resposta.status_code == 200
    assert resposta.get_json() == IMOVEL
    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE id = %s", (1,)
    )


@patch("app.conecta")
def test_buscar_imovel_inexistente(mock_conecta, client):
    # Given
    mock_conexao = MagicMock()
    mock_cursor = MagicMock()
    mock_conexao.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    mock_conecta.return_value = mock_conexao

    # When
    resposta = client.get("/imoveis/999")

    # Then
    assert resposta.status_code == 404
    assert resposta.get_json() == {"erro": "imovel nao encontrado"}
