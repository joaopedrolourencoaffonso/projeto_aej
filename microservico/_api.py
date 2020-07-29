from flask import Flask, jsonify, request, render_template


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
        return render_template('index.php')


@app.route('/delete_id/<int:_id>', methods=['GET', 'POST'])
def delete_id(_id):
        try:
                import subprocess
                #modelo do input: _id
                _id = id_function(_id)
                subprocess.call('curl -XDELETE http://localhost:9200/pessoas/_doc/' + str(_id) + '?pretty')
                return "Deleted with sucess" #seria interessante colocar um request aqui para ter certeza que realmente deletou, mas por enquanto isso aqui vai servir
        except:
                return "Error"


@app.route('/search_field/<string:word>', methods=['GET', 'POST'])
def search_field(word):
        try:
                import requests, json
                #modelo de input: campo_pesquisado|busca
                lista = word.split("|")
                filtro = "http://localhost:9200/pessoas/_count?q=$campo:$busca"
                filtro = filtro.replace("$campo",str(lista[0]))
                filtro = filtro.replace("$busca",str(lista[1]))
                res = requests.get(filtro)
                res.raise_for_status()
                obj = res.json()

                if str(obj["count"]) == "0":
                        return "Error"
                else:
                        return str(obj["count"])
                
        except:
                return "Error"


@app.route('/populacao', methods=['GET'])
def populacao():
        try:
                populacao = search_field("falecimento.data|2999-01-01") #/search_field
                return "A população atual é " + populacao
        
        except:
                return "Error"


@app.route('/calcula_idade/<string:data>', methods=['GET'])
def calcula_idade(data):
        try:
                from datetime import date, datetime
                nascimento = str(data)
                temp = nascimento.split("-")
                nascimento = datetime(int(temp[0]), int(temp[1]), int(temp[2]))
                today = date.today()
                idade = today.year - nascimento.year - ((today.month, today.day) < (nascimento.month, nascimento.day))
                return str(idade)
                
        except:
                return "Error"


@app.route('/idade/<string:_id>', methods=['GET'])
def idade(_id):
        try:
                import requests, json
                res = requests.get("http://localhost:9200/pessoas/_doc/" + str(_id))
                res.raise_for_status()
                obj = res.json()
                if str(obj["_source"]["falecimento"]["data"]) == "2999-01-01":
                        idade = calcula_idade(obj["_source"]["data_de_nascimento"]) #/calcula_idade
                        return "A idade de " + str(obj["_source"]["nome"]) + " " + str(obj["_source"]["sobrenome"]) + " é " + str(idade) + " anos."
                else:
                        return "" + str(obj["_source"]["nome"]) + " " + str(obj["_source"]["sobrenome"]) + " morreu em " + str(obj["_source"]["falecimento"]["data"]) + " ."
                
        except:
                return "Error"

@app.route('/search_fields/<string:search>', methods=['GET'])
def search_fields(search):
        try:
                from elasticsearch import Elasticsearch
                es = Elasticsearch()
                lista = search.split("|")
                if lista[0] == "1" :  #query de data. ex: 1|1998-01-16|2000-01-01
                        query = { "query": { "range" : { "data_de_nascimento" : { "gte" : str(lista[1]), "lt" : str(lista[2]) } } } }
                        res = es.search(index="pessoas", body=query)
                        return str(res["hits"]["total"]["value"])
                        
                if lista[0] == "2":  #query de data ex: 1|1998-01-16|2000-01-01|sobrenome|alonso|genero|f
                        query = { "query": { "bool": { "must": [ { "range" : { "data_de_nascimento" : { "gte" : str(lista[1]), "lt" : str(lista[2]) } } } ] } } }
                        i = 3
                        while i < len(lista):
                                query["query"]["bool"]["must"].append({ 'match': { str(lista[i]): str(lista[i+1]) } })
                                i = i + 2
                                
                        res = es.search(index="pessoas", body=query)
                        return str(res["hits"]["total"]["value"])
                
                else:
                        return "Error"
                

        except:
                return "Error"


@app.route('/search_date_range/<string:dates>', methods=['GET'])
def search_date_range(dates):
        try:
                search = "1|" + str(dates)
                results = search_fields(search)
                return str(results)

        except:
                return "Error"



if __name__ == '__main__':
        app.run(debug=True)
