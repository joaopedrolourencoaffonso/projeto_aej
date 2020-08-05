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
                if lista[0] == "1" :  #filtra todos os nascimentos entre duas datas. ex: 1|1998-01-16|2000-01-01
                        query = { "query": { "range" : { "data_de_nascimento" : { "gte" : str(lista[1]), "lt" : str(lista[2]) } } } }
                        res = es.search(index="pessoas", body=query)
                        return str(res["hits"]["total"]["value"])
                        
                if lista[0] == "2":  #filtra todos os nascimentos entre duas datas mais alguns fatores a sua escolha ex: 1|1998-01-16|2000-01-01|sobrenome|alonso|genero|f
                        query = { "query": { "bool": { "must": [ { "range" : { "data_de_nascimento" : { "gte" : str(lista[1]), "lt" : str(lista[2]) } } } ] } } }
                        i = 1
                        while i < len(lista):
                                query["query"]["bool"]["must"].append({ 'match': { str(lista[i]): str(lista[i+1]) } })
                                i = i + 2
                                
                        res = es.search(index="pessoas", body=query)
                        return str(res["hits"]["total"]["value"])
                
                if lista[0] == "3":  #filtra baseado em fatores a sua escolha ex: 3|sobrenome|alonso|genero|f
                        query = { "query": { "bool": { "must": [ ] } } }
                        i = 1
                        while i < len(lista):
                                query["query"]["bool"]["must"].append({ 'match': { str(lista[i]): str(lista[i+1]) } }) #query 'ou' ao invés de 'e'
                                i = i + 2

                        if lista[1] == "id": # concluo que ninguém vai tentar filtrar usando o "id", já que eles são únicos, vão devolver apenas um resultado
                                res = es.search(index="pessoas", body=query)
                                temp = str(res['hits']['hits'][0])
                                temp = temp.split("'")
                                return str(temp[23])

                        else:
                                res = es.search(index="pessoas", body=query)
                                return str(res["hits"]["total"]["value"])

                if lista[0] == "4": #query de nome mais comum no momento
                        query = {"_source": [ "nome", "falecimento.data" ],"size": 100,"query" : { "bool" : { "must" : [ {"match" : {"id": str(lista[1])}}]}}}
                        res = es.search(index="pessoas", body=query)
                        temp = str(res['hits']['hits'][0]).split("'")
                        return (temp[19],temp[25])
                
                if lista[0] == "5": #query maleável do tipo "and" (devolve o json resultante de uma pesquisa)
                        import json
                        query = {"_source": [ ],"size": 100,"query" : { "bool" : { "must" : [ ]}}}
                        i = 2
                        while i < len(lista): #5|2|nome|falecimento.data|sobrenome|Almeida|genero|m
                                if i <= int(lista[1]) + 1:
                                        query["_source"].append( lista[i] )
                                        i = i + 1
                                        
                                elif i < len(lista):
                                        query["query"]["bool"]["must"].append({ 'match': { str(lista[i]): str(lista[i+1]) } })
                                        i = i + 2
                                        
                                else:
                                        break
                                        
                        res = es.search(index="pessoas", body=query)
                        return res
                if lista[0] == "6": #query maleável do tipo "ou" (devolve o json resultante de uma pesquisa)
                        import json
                        query = {"_source": [ ],"size": 100,"query" : { "bool" : { "should" : [ ]}}}
                        i = 2
                        while i < len(lista): #6|2|nome|falecimento.data|sobrenome|Almeida|genero|m
                                if i <= int(lista[1]) + 1:
                                        query["_source"].append( lista[i] )
                                        i = i + 1
                                        
                                elif i < len(lista):
                                        query["query"]["bool"]["should"].append({ 'match': { str(lista[i]): str(lista[i+1]) } })
                                        i = i + 2
                                        
                                else:
                                        break
                                        
                        res = es.search(index="pessoas", body=query)
                        return res
                
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

@app.route('/idade_media/<string:filtro>', methods=['GET'])
def idade_media(filtro):
        try:
                #exemplo de query: genero|f|falecimento.data|2999-01-01
                filtro = "5|1|data_de_nascimento|" + str(filtro)
                res = search_fields(filtro)
                i = 0
                total = 0
                if int(res["hits"]["total"]["value"]) == 0:
                        return "0"      #se nada for encontrado, a API simplesmente retorna 0
                else:
                        while i < int(res["hits"]["total"]["value"]):
                                temp = str(res['hits']['hits'][1]['_source']['data_de_nascimento'])
                                total = total + int(calcula_idade(temp))
                                i = i + 1

                        media = total / int(res["hits"]["total"]["value"])
                        return str(media)
                #return res['hits']['hits'][8]['_source']['data_de_nascimento']
        except:
                return "Error"

        
@app.route('/familia/<string:_id>', methods=['GET'])
def familia(_id):
        try:
                if str(_id) == "0000":
                        return "Usuário desconhecido ou inexistente"
                else:
                        #############################################################################pessoa
                        query = "5|4|nome|sobrenome|familia.pai|familia.mae|id|"
                        temp =  query + str(_id)
                        pessoa = search_fields(temp)
                        nome = pessoa['hits']['hits'][0]['_source']['nome']
                        sobrenome = pessoa['hits']['hits'][0]['_source']['sobrenome']
                        id_pai = pessoa['hits']['hits'][0]['_source']['familia']['pai']
                        id_mae = pessoa['hits']['hits'][0]['_source']['familia']['mae']
                        #############################################################################pai
                        temp = query + str(id_pai)
                        pessoa = search_fields(temp)
                        nome_pai = pessoa['hits']['hits'][0]['_source']['nome']
                        sobrenome_pai = pessoa['hits']['hits'][0]['_source']['sobrenome']
                        id_avo_paterno = pessoa['hits']['hits'][0]['_source']['familia']['pai']
                        id_avo_paterna = pessoa['hits']['hits'][0]['_source']['familia']['mae']
                        #############################################################################mae
                        temp = query + str(id_mae)
                        pessoa = search_fields(temp)
                        nome_mae = pessoa['hits']['hits'][0]['_source']['nome']
                        sobrenome_mae = pessoa['hits']['hits'][0]['_source']['sobrenome']
                        id_avo_materno = pessoa['hits']['hits'][0]['_source']['familia']['pai']
                        id_avo_materna = pessoa['hits']['hits'][0]['_source']['familia']['mae']
                        #############################################################################avo_paterno
                        temp = query + str(id_avo_paterno)
                        pessoa = search_fields(temp)
                        nome_avo_paterno = pessoa['hits']['hits'][0]['_source']['nome']
                        sobrenome_avo_paterno = pessoa['hits']['hits'][0]['_source']['sobrenome']
                        #############################################################################avo_paterna
                        temp = query + str(id_avo_paterna)
                        pessoa = search_fields(temp)
                        nome_avo_paterna = pessoa['hits']['hits'][0]['_source']['nome']
                        sobrenome_avo_paterna = pessoa['hits']['hits'][0]['_source']['sobrenome']
                        #############################################################################avo_materno
                        temp = query + str(id_avo_materno)
                        pessoa = search_fields(temp)
                        nome_avo_materno = pessoa['hits']['hits'][0]['_source']['nome']
                        sobrenome_avo_materno = pessoa['hits']['hits'][0]['_source']['sobrenome']
                        ############################################################################avo_materna
                        temp = query + str(id_avo_materna)
                        pessoa = search_fields(temp)
                        nome_avo_materna = pessoa['hits']['hits'][0]['_source']['nome']
                        sobrenome_avo_materna = pessoa['hits']['hits'][0]['_source']['sobrenome']
                        ############################################################################retorno
                        retorno = str(nome) + " " + str(sobrenome) + "|" + str(nome_pai) + " " + str(sobrenome_pai) + "|" + str(nome_mae) + " " + str(sobrenome_mae)
                        retorno = retorno + "|" + str(nome_avo_paterno) + " " + str(sobrenome_avo_paterno) + "|" + str(nome_avo_paterna) + " " + str(sobrenome_avo_paterna)
                        retorno = retorno + "|" + str(nome_avo_materno) + " " + str(sobrenome_avo_materno) + "|" + str(nome_avo_materna) + " " + str(sobrenome_avo_materna)
                        return str(retorno)
                        
                
        except:
                return "Error"        
        
if __name__ == '__main__':
        app.run(debug=True)
