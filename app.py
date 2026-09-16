import os

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

app = Flask(__name__)
app.json.ensure_ascii = False


def conecta():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


@app.route("/imoveis", methods=["GET"])
def listar_imoveis():
    conexao = conecta()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM imoveis")
    imoveis = cursor.fetchall()
    cursor.close()
    conexao.close()

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
    return jsonify(imovel), 200


if __name__ == "__main__":
    app.run(debug=True)
