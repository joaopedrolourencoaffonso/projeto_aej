

from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
        return render_template('index.php')

@app.route('/projeto_aej/<string:entrada>', methods=['GET'])
def autenticacao(entrada):
        try:
                from elasticsearch import Elasticsearch
                es = Elasticsearch()
                lista = entrada.split("|")
                query = { "query": { "bool": { "must": [ {"match": { "id": lista[0]}}, {"match": { "password": lista[1]}} ] } } }
                res = es.search(index="autentica", body=query)
                if (res["hits"]["total"]["value"] == 1):
                        return jsonify({"resultado":"1"})
                else:
                        return jsonify({"resultado":"0"})

        except:
                return jsonify({"resultado":"-1"})
        

@app.route('/pesquisa_simples/<string:busca>', methods=['GET'])
def pesquisa_simples(busca):
        try:
                import requests, json
                #modelo de input: campo_pesquisado|busca
                lista = busca.split("|")
                temp = 'http://localhost:5000/projeto_aej/' + str(lista[0]) + "|" + str(lista[1])
                res = requests.get(temp)
                res.raise_for_status()
                resultado = res.json()
                #return str(obj['resultado'])
                if (resultado['resultado'] == "0"):
                        return jsonify({"resultado":"Error1"})
                
                if (resultado['resultado'] == "-1"):
                        return jsonify({"resultado":"Error2"})
                
                if (resultado['resultado'] == "1"):
                        filtro = "http://localhost:9200/pessoas/_count?q=$campo:$busca"
                        filtro = filtro.replace("$campo",str(lista[2]))
                        filtro = filtro.replace("$busca",str(lista[3]))
                        res = requests.get(filtro)
                        res.raise_for_status()
                        obj = res.json()
                        return jsonify({"resultado":str(obj["count"])})
                
        except:
                return jsonify({"resultado":"Error3"})

        

if __name__ == '__main__':
        app.run(debug=True)












