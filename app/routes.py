from app import app
from flask import jsonify, render_template, request
import algoritmo_genetico
import time
@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar():
    # receber o semestre 1 ou 2 - ok
    # exibir as 10 primeiras soluções
    dados_recebidos = request.json
    semestre = dados_recebidos.get('semestre')
    #matriz, tamanho, geracoes, semestre_inicial
    inicio = time.time()
    resultado = algoritmo_genetico.ag(dados_recebidos, 100, 10000, int(semestre))
    fim = time.time()
    print("Tempo de execucao:", fim-inicio)
    return jsonify(resultado)
        