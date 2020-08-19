
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
        return render_template('index.php')

@app.route('/projeto_aej/<string:entrada>', methods=['GET'])
def autenticacao(entrada):
        try:
                #modelo de entrada seria: 0001&&apeacjpla&&insira_id_da_API_aqui&&insira_query_aqui
                from elasticsearch import Elasticsearch
                es = Elasticsearch()
                lista = entrada.split("&&")
                query = { "query": { "bool": { "must": [ {"match": { "id": lista[0]}}, {"match": { "password": lista[1]}} ] } } }
                res = es.search(index="autentica", body=query)
                if (res["hits"]["total"]["value"] == 1):
                        if (lista[2] == "1"):   #0001&&apeacjpla&&1&&{"nome":"José", "sobrenome":"Alonso",....}
                                resultado = cadastro(lista[3])
                                return resultado
                        
                        if (lista[2] == "2"):   #0001&&apeacjpla&&2&&0045
                                resultado = delete(lista[3])
                                return resultado

                        if (lista[2] == "3"):
                                resultado = pesquisa(lista[3])
                                return resultado
                        
                        if (lista[2] == "4"):
                                resultado = pesquisa_avancada(lista[3])
                                return resultado
                        else:
                                return jsonify({"resultado":"Essa API não existe"})
                else:
                        return jsonify({"resultado":"Erro de autentificação"})

        except:
                return jsonify({"resultado":"Erro de execução 3"})
        

@app.route('/cadastro/<string:pessoa>', methods=['GET'])
def cadastro(pessoa):
        try:
                from elasticsearch import Elasticsearch
                es = Elasticsearch()
                import json
                query_id = {"query" : { "match_all" : {} } }
                res = es.search(index="pessoa", body=query_id)
                num = int(res["hits"]["total"]["value"]) + 1
                
                if num < 10:
                        _id = "000" + str(num)
                        
                elif (num < 100) and (num > 9):
                        _id = "00" + str(num)
                        
                else:
                        if (99 < num) and (num < 1000):
                                _id = "0" + str(num)
                                
                        else:
                                return "Erro, a base de dados está lotada."

                pessoa = pessoa.replace("'", '\"')
                pessoa = json.loads(pessoa)
                pessoa['id'] = str(_id)
                es.index(index='pessoa',id=str(_id),body=pessoa)
                
                return jsonify({"resultado":"Adicionado com sucesso!"})
        except:
                return jsonify({"resultado":"Erro de execução"})


@app.route('/delete/<string:_id>', methods=['GET'])
def delete(_id):
        try:
                from elasticsearch import Elasticsearch
                es = Elasticsearch()
                es.delete(index="pessoa", doc_type="_doc",id=str(_id))
                return jsonify({"resultado":"A entrada com id: " + str(_id) + ", foi efetuada"})
        
        except:
                return jsonify({"resultado":"Erro de execução"})
 

@app.route('/pesquisa/<string:busca>', methods=['GET'])
def pesquisa(busca):
        try:
                from elasticsearch import Elasticsearch
                es = Elasticsearch()
                import json
                
                lista = busca.split("|")
                query = { "query": { "bool": { "must": [ ] } } }
                if lista[0] == "0":
                        i = 1
                        
                else:
                        query["query"]["bool"]["must"].append({ 'range' : { 'data_de_nascimento' : { 'gte' : str(lista[1]), 'lt' : str(lista[2])} } })
                        i = 3
                
                while i < len(lista):
                        query["query"]["bool"]["must"].append({ 'match': { str(lista[i]): str(lista[i+1]) } })
                        i = i + 2

                res = es.search(index="pessoas", body=query)
                return json.loads('{"resultado":"' + str(res["hits"]["total"]["value"]) + '"}'

        except:
                return jsonify({"resultado":"Erro de execução"})

@app.route('/pesquisa_avancada/<string:busca>', methods=['GET'])
def pesquisa_avancada(busca):
        try:
                from elasticsearch import Elasticsearch
                es = Elasticsearch()
                busca = busca.split("$")
                lista = busca[0].split("|")
                query = {"_source": [ ],"size": 10000,"query" : { "bool" : { "must" : [ ]}}}
                i = 2

                if len(busca) == 3:
                        query["query"]["bool"]["must"].append({ 'range' : { 'data_de_nascimento' : { 'gte' : str(busca[1]), 'lt' : str(busca[2])} } })
                
                
                while i < len(lista): #0|2|nome|falecimento.data|sobrenome|Almeida|genero|m
                        if i <= int(lista[1]) + 1:
                                query["_source"].append(lista[i])
                                i = i + 1

                        elif i < len(lista):
                                query["query"]["bool"]["must"].append({ 'match': { str(lista[i]): str(lista[i+1]) } })
                                i = i + 2
                        else:
                                break

                res = es.search(index="pessoas", body=query)
                return res

        except:
                return jsonify({"resultado":"Erro de execução"})

#############################

####APIs que interagem com as APIs acima
        
@app.route('/nome/<int:num>', methods=['GET'])
def nome(num):
        try:
                #import requests, json
                #se num = 1, ele devolve o nome mais comum da história, se num = 2, ele devolve o nome mais comum no momento
                res = pesquisa("1|1900-01-01|3000-01-01")
                tamanho = range(1, int(res["resultado"])) 
                lista = {"anonimo":1}
                j = 0
                
                if num == 1:
                        for i in tamanho:
                                if i < 10:
                                        _id = "000" + str(i)
                                elif (i < 100) and (i > 9):
                                        _id = "00" + str(i)
                                else:
                                        if (99 < i) and (i < 1000):
                                                _id = "0" + str(i)
                                        else:
                                                return "Erro"

                                string = "0|1|nome|id|" + str(_id) #0|1|data_de_nascimento|id|
                                res = pesquisa_avancada(string)
                                nome = str(res['hits']['hits'][0]['_source']['nome'])
                                y = list(lista.keys())
                                if nome in y:
                                        lista[nome] = lista[nome] + 1
                                else:
                                        lista[nome] = 1

                        popular = max(lista, key=lista.get)
                        return jsonify({"resultado":popular})

                else:
                        return jsonify({"resultado":"Error de escolha de opção, as únicas válidas são 1 ou 0"})
                
        except:
                return jsonify({"resultado":"Error de execucao"})

if __name__ == '__main__':
        app.run(debug=True)
