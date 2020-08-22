

from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
        return render_template('index.php')


###APIs que interagem com a base de dados
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

                        if (lista[2] == "5"):
                                resultado = nome(lista[3])
                                return resultado
                        
                        if (lista[2] == "6"):
                                resultado = familia(lista[3])
                                return resultado
                        
                        if (lista[2] == "7"):
                                resultado = idade_media(lista[3])
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
                                return jsonify({"resultado":"Erro, a base de dados está lotada."})

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
                #return jsonify({"resultado": str(res["hits"]["total"]["value"])})
                return json.loads('{"resultado":"' + str(res["hits"]["total"]["value"]) + '"}')

        except:
                return jsonify({"resultado":"Erro de execução"})

@app.route('/pesquisa_avancada/<string:busca>', methods=['GET'])
def pesquisa_avancada(busca):
        try:                    #0|2|nome|falecimento.data|sobrenome|Almeida|genero|m$1990-01-01$2020-01-01
                from elasticsearch import Elasticsearch
                es = Elasticsearch()
                busca = busca.split("$")
                lista = busca[0].split("|")
                query = {"_source": [ ],"size": 10000,"query" : { "bool" : { "must" : [ ]}}}
                i = 1
                
                if len(busca) == 3:
                        query["query"]["bool"]["must"].append({ 'range' : { 'data_de_nascimento' : { 'gte' : str(busca[1]), 'lt' : str(busca[2])} } })
                
                
                while i < len(lista):
                        #print(i)
                        if i <= int(lista[0]):
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
                lista = {}
                num = int(num)

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

                                string = "1|nome|id|" + str(_id) #0|1|data_de_nascimento|id|
                                res = pesquisa_avancada(string)
                                nome = str(res['hits']['hits'][0]['_source']['nome'])
                                y = list(lista.keys())
                                if nome in y:
                                        lista[nome] = lista[nome] + 1
                                else:
                                        lista[nome] = 1

                        popular = max(lista, key=lista.get)
                        return jsonify({"resultado":popular})

                elif num == 2:
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

                                string = "2|nome|falecimento.data|id|" + str(_id) #0|1|data_de_nascimento|id|
                                res = pesquisa_avancada(string)

                                if res['hits']['hits'][0]['_source']['falecimento']['data'] != '2999-01-01':
                                        continue
                                else:
                                        nome = str(res['hits']['hits'][0]['_source']['nome'])
                                        y = list(lista.keys())
                                        if nome in y:
                                                lista[nome] = lista[nome] + 1
                                        else:
                                                lista[nome] = 1

                        popular = max(lista, key=lista.get)
                        return jsonify({"resultado":popular})

                else:
                                return jsonify({"resultado":"Error de escolha de opção, as únicas válidas são 1 ou 2"})
                
        except:
                return jsonify({"resultado":"Error de execucao"})


@app.route('/familia/<string:_id>', methods=['GET'])
def familia(_id):
        try:
                if str(_id) == "0000":
                        return jsonify({"resultado":"Usuário desconhecido ou inexistente"})
                else:
                        #############################################################################pessoa
                        query = "4|nome|sobrenome|familia.pai|familia.mae|id|"
                        temp =  query + str(_id)
                        pessoa = pesquisa_avancada(temp)
                        nome = pessoa['hits']['hits'][0]['_source']['nome']
                        sobrenome = pessoa['hits']['hits'][0]['_source']['sobrenome']
                        id_pai = pessoa['hits']['hits'][0]['_source']['familia']['pai']
                        id_mae = pessoa['hits']['hits'][0]['_source']['familia']['mae']
                        #############################################################################pai
                        temp = query + str(id_pai)
                        pessoa = pesquisa_avancada(temp)
                        nome_pai = pessoa['hits']['hits'][0]['_source']['nome']
                        sobrenome_pai = pessoa['hits']['hits'][0]['_source']['sobrenome']
                        id_avo_paterno = pessoa['hits']['hits'][0]['_source']['familia']['pai']
                        id_avo_paterna = pessoa['hits']['hits'][0]['_source']['familia']['mae']
                        #############################################################################mae
                        temp = query + str(id_mae)
                        pessoa = pesquisa_avancada(temp)
                        nome_mae = pessoa['hits']['hits'][0]['_source']['nome']
                        sobrenome_mae = pessoa['hits']['hits'][0]['_source']['sobrenome']
                        id_avo_materno = pessoa['hits']['hits'][0]['_source']['familia']['pai']
                        id_avo_materna = pessoa['hits']['hits'][0]['_source']['familia']['mae']
                        #############################################################################avo_paterno
                        temp = query + str(id_avo_paterno)
                        pessoa = pesquisa_avancada(temp)
                        nome_avo_paterno = pessoa['hits']['hits'][0]['_source']['nome']
                        sobrenome_avo_paterno = pessoa['hits']['hits'][0]['_source']['sobrenome']
                        #############################################################################avo_paterna
                        temp = query + str(id_avo_paterna)
                        pessoa = pesquisa_avancada(temp)
                        nome_avo_paterna = pessoa['hits']['hits'][0]['_source']['nome']
                        sobrenome_avo_paterna = pessoa['hits']['hits'][0]['_source']['sobrenome']
                        #############################################################################avo_materno
                        temp = query + str(id_avo_materno)
                        pessoa = pesquisa_avancada(temp)
                        nome_avo_materno = pessoa['hits']['hits'][0]['_source']['nome']
                        sobrenome_avo_materno = pessoa['hits']['hits'][0]['_source']['sobrenome']
                        ############################################################################avo_materna
                        temp = query + str(id_avo_materna)
                        pessoa = pesquisa_avancada(temp)
                        nome_avo_materna = pessoa['hits']['hits'][0]['_source']['nome']
                        sobrenome_avo_materna = pessoa['hits']['hits'][0]['_source']['sobrenome']
                        ############################################################################retorno
                        #retorno = str(nome) + " " + str(sobrenome) + "|" + str(nome_pai) + " " + str(sobrenome_pai) + "|" + str(nome_mae) + " " + str(sobrenome_mae)
                        #retorno = retorno + "|" + str(nome_avo_paterno) + " " + str(sobrenome_avo_paterno) + "|" + str(nome_avo_paterna) + " " + str(sobrenome_avo_paterna)
                        #retorno = retorno + "|" + str(nome_avo_materno) + " " + str(sobrenome_avo_materno) + "|" + str(nome_avo_materna) + " " + str(sobrenome_avo_materna)
                        #return str(retorno)
                        retorno = {}
                        retorno["nome"] = str(nome) + " " + str(sobrenome)
                        retorno["pai"] = str(nome_pai) + " " + str(sobrenome_pai)
                        retorno["mae"] = str(nome_mae) + " " + str(sobrenome_mae)
                        retorno["avo_paterno"] = str(nome_avo_paterno) + " " + str(sobrenome_avo_paterno)
                        retorno["avo_paterna"] = str(nome_avo_paterna) + " " + str(sobrenome_avo_paterna)
                        retorno["avo_materno"] = str(nome_avo_materno) + " " + str(sobrenome_avo_materno)
                        retorno["avo_materna"] = str(nome_avo_materna) + " " + str(sobrenome_avo_materna)
                        return jsonify(retorno)
                        
        except:
                return jsonify({"resultado":"Error de execucao"})



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
                return jsonify({"resultado":"Error de execucao"})


@app.route('/idade_media/<string:filtro>', methods=['GET'])
def idade_media(filtro):
        try:
                #exemplo de query: genero|f|falecimento.data|2999-01-01
                filtro = "1|data_de_nascimento|falecimento.data|2999-01-01|" + str(filtro)
                res = pesquisa_avancada(filtro)
                i = 0
                total = 0
                #return res
                if int(res["hits"]["total"]["value"]) == 0:
                        return jsonify({"resultado":"A query não retornou resultados"})      #se nada for encontrado, a API simplesmente retorna 0
                else:
                        while i < int(res["hits"]["total"]["value"]):
                                temp = str(res['hits']['hits'][i]['_source']['data_de_nascimento'])
                                total = total + int(calcula_idade(temp))
                                i = i + 1

                media = total / int(res["hits"]["total"]["value"])
                return jsonify({"resultado":str(media)})
                                
        except:
                return jsonify({"resultado":"Error de execucao"})
        

if __name__ == '__main__':
        app.run(debug=True)










#modelo de input: campo_pesquisado|busca
                
                #temp = 'http://localhost:5000/projeto_aej/' + str(lista[0]) + "|" + str(lista[1])
                #res = requests.get(temp)
                #res.raise_for_status()
                #resultado = res.json()
                #return str(obj['resultado'])
                #if (resultado['resultado'] == "0"):
                #        return jsonify({"resultado":"Error1"})
                #
                #if (resultado['resultado'] == "-1"):
                #        return jsonify({"resultado":"Error2"})
                #
                #if (resultado['resultado'] == "1"):
