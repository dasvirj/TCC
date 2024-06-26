from app import app
from flask import jsonify, render_template, request
import algoritmo_genetico
@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar():
    dados_recebidos = request.json
    #matriz, tamanho, geracoes, semestre_inicial
    resultado = algoritmo_genetico.ag(dados_recebidos, 100, 2000, 2)
    return jsonify(resultado)
        