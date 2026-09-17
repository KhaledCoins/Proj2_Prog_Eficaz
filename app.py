import os

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, jsonify, request, url_for

load_dotenv()

app = Flask(__name__)
app.json.ensure_ascii = False

CAMPOS = [
    "logradouro",
    "tipo_logradouro",
    "bairro",
    "cidade",
    "cep",
    "tipo",
    "valor",
    "data_aquisicao",
]


def conecta():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


def com_links(imovel):
    imovel["_links"] = {
        "self": url_for("buscar_imovel", imovel_id=imovel["id"]),
        "todos": url_for("listar_imoveis"),
        "tipo": url_for("buscar_por_tipo", tipo=imovel["tipo"]),
        "cidade": url_for("buscar_por_cidade", cidade=imovel["cidade"]),
    }
    return imovel


def consulta(sql, *parametros):
    conexao = conecta()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute(sql, *parametros)
    imoveis = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [com_links(imovel) for imovel in imoveis]


@app.route("/imoveis", methods=["GET"])
def listar_imoveis():
    imoveis = consulta("SELECT * FROM imoveis")

    if not imoveis:
        return jsonify({"erro": "nenhum imovel encontrado"}), 404
    return jsonify(imoveis), 200


@app.route("/imoveis/<int:imovel_id>", methods=["GET"])
def buscar_imovel(imovel_id):
    conexao = conecta()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (imovel_id,))
    imovel = cursor.fetchone()
    cursor.close()
    conexao.close()

    if imovel is None:
        return jsonify({"erro": "imovel nao encontrado"}), 404
    return jsonify(com_links(imovel)), 200


@app.route("/imoveis", methods=["POST"])
def cadastrar_imovel():
    dados = request.get_json(silent=True)
    if not dados or any(campo not in dados for campo in CAMPOS):
        return jsonify({"erro": "dados incompletos"}), 400

    conexao = conecta()
    cursor = conexao.cursor()
    cursor.execute(
        """
        INSERT INTO imoveis
            (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        tuple(dados[campo] for campo in CAMPOS),
    )
    conexao.commit()
    dados["id"] = cursor.lastrowid
    cursor.close()
    conexao.close()

    com_links(dados)
    return jsonify(dados), 201, {"Location": dados["_links"]["self"]}


@app.route("/imoveis/<int:imovel_id>", methods=["PUT"])
def atualizar_imovel(imovel_id):
    dados = request.get_json(silent=True)
    if not dados or any(campo not in dados for campo in CAMPOS):
        return jsonify({"erro": "dados incompletos"}), 400

    conexao = conecta()
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM imoveis WHERE id = %s", (imovel_id,))
    existe = cursor.fetchone()

    if existe is None:
        cursor.close()
        conexao.close()
        return jsonify({"erro": "imovel nao encontrado"}), 404

    cursor.execute(
        """
        UPDATE imoveis
        SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s,
            cep = %s, tipo = %s, valor = %s, data_aquisicao = %s
        WHERE id = %s
        """,
        tuple(dados[campo] for campo in CAMPOS) + (imovel_id,),
    )
    conexao.commit()
    cursor.close()
    conexao.close()

    dados["id"] = imovel_id
    return jsonify(com_links(dados)), 200


@app.route("/imoveis/<int:imovel_id>", methods=["DELETE"])
def remover_imovel(imovel_id):
    conexao = conecta()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id = %s", (imovel_id,))
    conexao.commit()
    removidos = cursor.rowcount
    cursor.close()
    conexao.close()

    if removidos == 0:
        return jsonify({"erro": "imovel nao encontrado"}), 404
    return "", 204


@app.route("/imoveis/tipo/<tipo>", methods=["GET"])
def buscar_por_tipo(tipo):
    imoveis = consulta("SELECT * FROM imoveis WHERE tipo = %s", (tipo,))

    if not imoveis:
        return jsonify({"erro": "nenhum imovel encontrado"}), 404
    return jsonify(imoveis), 200


@app.route("/imoveis/cidade/<cidade>", methods=["GET"])
def buscar_por_cidade(cidade):
    imoveis = consulta("SELECT * FROM imoveis WHERE cidade = %s", (cidade,))

    if not imoveis:
        return jsonify({"erro": "nenhum imovel encontrado"}), 404
    return jsonify(imoveis), 200


if __name__ == "__main__":
    app.run(debug=True)
