from flask import Flask, jsonify, request, render_template

def id_function(num):
        if num < 10:
                _id = "000" + str(num)
                return _id
        elif (num < 100) and (num > 9):
                _id = "00" + str(num)
                return _id
        else:
                if (99 < num) and (num < 1000):
                        _id = "0" + str(num)
                        return _id
                else:
                        return "0001"
def pesquisa(_id):
        import requests, json
        res = requests.get("http://localhost:9200/pessoas/_doc/" + str(_id))
        res.raise_for_status()
        obj = res.json()
        return str(obj["_source"]["familia"]["pai"]) + "|" + str(obj["_source"]["familia"]["mae"]) + "|" + str(obj["_source"]["nome"]) + " " + str(obj["_source"]["sobrenome"])        
        
        
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
        return render_template('index.php')


@app.route('/search_id/<int:num>', methods=['GET', 'POST'])
def search_id(num):
        try:
                import requests, json
                #modelo de input: numero da id sem os zeros
                _id = id_function(num)
                res = requests.get("http://localhost:9200/pessoas/_doc/" + str(_id))
                res.raise_for_status()
                obj = res.json()
                nome = str(obj["_source"]["nome"])
                return "Nome: " + str(nome)
        except:
                return "Error "


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

@app.route('/add/<string:word>', methods=['GET', 'POST'])
def add(word):
        try:
                import subprocess
                #modelo do input na url: id|nome|sobrenome
                file = open("add_pessoa.json")
                add_pessoa = file.read()
                file.close()
                lista = word.split("|")
                _id = str(id_function(int(lista[0])))
                nome = str(lista[1])
                sobrenome = str(lista[2])
                add_pessoa = add_pessoa.replace("$_id", _id)
                add_pessoa = add_pessoa.replace("$nome", nome)
                add_pessoa = add_pessoa.replace("$sobrenome", sobrenome)
                #basta adicionar mais campos
                file = open("add.json","w")
                file.write(add_pessoa)
                file.close()
                subprocess.call('curl -H "Content-Type: application/json" --data @add.json http://localhost:9200/pessoas/_doc/' + _id + '?pretty')
                return "Adicionado com sucesso!"
                
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
                        return "Erro nos termos de busca ou entrada inexistente"
                else:
                        return "O resultado é " + str(obj["count"])
        except:
                return "Error"

@app.route('/search_date_range/<string:dates>', methods=['GET', 'POST'])
def search_date_range(dates):
        try:
                from elasticsearch import Elasticsearch
                es = Elasticsearch()
                lista = dates.split("|")
                res = es.search(index="pessoas", body={ "query": { "range" : { "data_de_nascimento" : { "gte" : str(lista[0]), "lt" : str(lista[1]) } } } })
                #acessando a url /search_date_range/1990-11-01|2020-01-21 <--exemplo
                if int(res["hits"]["total"]["value"]) == 0:
                        return "Erro nos termos de busca ou entrada inexistente."
                else:
                        return "O resultado é " + str(res["hits"]["total"]["value"])

        except:
                return "Error"

@app.route('/populacao', methods=['GET'])
def populacao():
        try:
                import requests, json
                res = requests.get("http://localhost:9200/pessoas/_count?q=falecimento.data:2999-01-01")
                res.raise_for_status()
                obj = res.json()
                return "A população atual é " + str(obj["count"])              
        except:
                return "Error"
        
@app.route('/nome/<int:num>', methods=['GET'])
def nome(num):
        try:
                num = int(num)
                import requests, json
                lista = {}
                #se num = 1, ele devolve o nome mais comum da história, se num = 2, ele devolve o nome mais comum no momento
                res = requests.get("http://localhost:9200/pessoas/_count?q=nome:*")
                res.raise_for_status()
                obj = res.json()
                tamanho = range(1, int(obj["count"]))

                if num == 1:
                        for i in tamanho:
                                _id = str(id_function(i))
                                #return "Ok " + _id
                                res = requests.get("http://localhost:9200/pessoas/_doc/" + str(_id))
                                res.raise_for_status()
                                obj = res.json()
                                nome = str(obj["_source"]["nome"])
                        
                                if nome not in lista.keys():
                                        lista[nome] = 1
                                else:
                                        lista[nome] = lista[nome] + 1

                        popular = max(lista, key=lista.get)
                        return "O nome mais comum ao longo da história é: '" + str(popular) + "'"

                if num == 2:                
                        for i in tamanho:
                                _id = str(id_function(i))
                                #return "Ok " + _id
                                res = requests.get("http://localhost:9200/pessoas/_doc/" + str(_id))
                                res.raise_for_status()
                                obj = res.json()
                                nome = str(obj["_source"]["nome"])

                                if obj["_source"]["falecimento"]["data"] == "2999-01-01":
                                        if nome not in lista.keys():
                                                lista[nome] = 1
                                        else:
                                                lista[nome] = lista[nome] + 1

                        popular = max(lista, key=lista.get)
                        return "O nome mais comum no momento é: '" + str(popular) + "'"

                else:
                        return "Erro, rever a url."
                
        except:
                return "Error"
        
@app.route('/idade/<int:_id>', methods=['GET'])
def idade(_id):
        try:
                import requests, json
                from datetime import date, datetime
                #basta colocar o número da id
                _id = id_function(_id)
                res = requests.get("http://localhost:9200/pessoas/_doc/" + str(_id))
                res.raise_for_status()
                obj = res.json()
                if str(obj["_source"]["falecimento"]["data"]) == "2999-01-01":
                        nascimento = str(obj["_source"]["data_de_nascimento"])
                        temp = nascimento.split("-")
                        nascimento = datetime(int(temp[0]), int(temp[1]), int(temp[2]))
                        today = date.today()
                        idade = today.year - nascimento.year - ((today.month, today.day) < (nascimento.month, nascimento.day))
                        return "A idade de " + str(obj["_source"]["nome"]) + " " + str(obj["_source"]["sobrenome"]) + " é " + str(idade) + " anos."
                else:
                        return "" + str(obj["_source"]["nome"]) + " " + str(obj["_source"]["sobrenome"]) + " morreu em " + str(obj["_source"]["falecimento"]["data"]) + " ."
                
        except:
                return "Error"

@app.route('/idade_media/<string:filtro>', methods=['GET'])
def idade_media(filtro):
        try:
                from datetime import date, datetime
                from elasticsearch import Elasticsearch
                es = Elasticsearch()
                if filtro == "1":
                        idade_total = 0
                        res = es.search(index="pessoas", body={"_source": [ "data_de_nascimento" ],"size": 100,"query" : { "bool" : { "must" : [ {"match" : {"falecimento.data": "2999-01-01"}}]}}})
                        for i in res['hits']['hits']:
                                x = str(i)
                                nascimento = str(x[104:114])
                                temp = nascimento.split("-")
                                nascimento = datetime(int(temp[0]), int(temp[1]), int(temp[2]))
                                today = date.today()
                                idade = today.year - nascimento.year - ((today.month, today.day) < (nascimento.month, nascimento.day))
                                idade_total = int(idade_total) + int(idade)
                                #return "Ok"

                        idade_media = idade_total / int(res['hits']['total']['value'])
                        return str(idade_media)
                
                else:
                        filtro = filtro.split("|")
                        campo = str(filtro[0])
                        busca = str(filtro[1])
                        idade_total = 0
                        res = es.search(index="pessoas", body={"_source": [ "data_de_nascimento" ],"size": 100,"query" : { "bool" : { "must" : [ {"match" : {"falecimento.data": "2999-01-01"}}, {"match" : { campo : busca }}]}}})
                        for i in res['hits']['hits']:
                                x = str(i)
                                nascimento = str(x[110:120])
                                temp = nascimento.split("-")
                                nascimento = datetime(int(temp[0]), int(temp[1]), int(temp[2]))
                                today = date.today()
                                idade = today.year - nascimento.year - ((today.month, today.day) < (nascimento.month, nascimento.day))
                                idade_total = int(idade_total) + int(idade)
                                #return "Ok"

                        idade_media = idade_total / int(res['hits']['total']['value'])
                        return str(idade_media)
                
        except:
                return "Error"
        

@app.route('/and_search/<string:data>', methods=['GET'])
def and_search(data):
        try:
                #1 - Essa API é capaz defazer queries 'and'
                #2 - modelo de input: se houver apenas um campo de busca, você joga: campo|busca, se houver dois, você joga campo1|busca1|campo2|busca2 e assim por diante até quatro campos
                from elasticsearch import Elasticsearch
                es = Elasticsearch()
                lista = data.split("|")

                if len(lista) == 2:
                        campo = lista[0]
                        busca = lista[1]

                        res = es.search(index="pessoas", body={"query":{"match": {campo:busca}}}) #eu já tenho uma api que faz isso, mas achei válido fazer também
                        return "O resultado é: " + str(res['hits']['total']['value'])
                
                if len(lista) == 4:
                        campo1 = str(lista[0])
                        busca1 = str(lista[1])
                        campo2 = str(lista[2])
                        busca2 = str(lista[3])

                        res = es.search(index="pessoas", body={"query":{"bool":{"must":[{"match":{campo1:busca1}},{"match":{campo2:busca2}}]}}})
                        return "O resultado é: " + str(res['hits']['total']['value'])

                if len(lista) == 6:
                        campo1 = str(lista[0])
                        busca1 = str(lista[1])
                        campo2 = str(lista[2])
                        busca2 = str(lista[3])
                        campo3 = str(lista[4])
                        busca3 = str(lista[5])

                        res = es.search(index="pessoas", body={"query":{"bool":{"must":[{"match":{campo1:busca1}},{"match":{campo2:busca2}},{"match":{campo3:busca3}}]}}})
                        return "O resultado é: " + str(res['hits']['total']['value'])

                if len(lista) == 8:
                        campo1 = str(lista[0])
                        busca1 = str(lista[1])
                        campo2 = str(lista[2])
                        busca2 = str(lista[3])
                        campo3 = str(lista[4])
                        busca3 = str(lista[5])
                        campo4 = str(lista[6])
                        busca4 = str(lista[7])

                        res = es.search(index="pessoas", body={"query":{"bool":{"must":[{"match":{campo1:busca1}},{"match":{campo2:busca2}},{"match":{campo3:busca3}},{"match":{campo4:busca4}}]}}})
                        return "O resultado é: " + str(res['hits']['total']['value'])

                if len(lista) not in [2,4,6,8]:
                        return "Reveja sua pesquisa"
                
        except:
                return "Error"

@app.route('/or_search/<string:data>', methods=['GET'])
def or_search(data):
        try:
                #1 - Essa API é capaz defazer queries 'and'
                #2 - modelo de input: se houver apenas um campo de busca, você joga: campo|busca, se houver dois, você joga campo1|busca1|campo2|busca2 e assim por diante até quatro campos
                from elasticsearch import Elasticsearch
                es = Elasticsearch()
                lista = data.split("|")

                if len(lista) == 2:
                        campo = lista[0]
                        busca = lista[1]

                        res = es.search(index="pessoas", body={"query":{"bool":{"should":[{"match": {campo:busca}}]}}}) 
                        return "O resultado é: " + str(res['hits']['total']['value'])

                if len(lista) == 4:
                        campo1 = str(lista[0])
                        busca1 = str(lista[1])
                        campo2 = str(lista[2])
                        busca2 = str(lista[3])

                        res = es.search(index="pessoas", body={"query":{"bool":{"should":[{"match":{campo1:busca1}},{"match":{campo2:busca2}}]}}})
                        return "O resultado é: " + str(res['hits']['total']['value'])

                if len(lista) == 6:
                        campo1 = str(lista[0])
                        busca1 = str(lista[1])
                        campo2 = str(lista[2])
                        busca2 = str(lista[3])
                        campo3 = str(lista[4])
                        busca3 = str(lista[5])

                        res = es.search(index="pessoas", body={"query":{"bool":{"should":[{"match":{campo1:busca1}},{"match":{campo2:busca2}},{"match":{campo3:busca3}}]}}})
                        return "O resultado é: " + str(res['hits']['total']['value'])

                if len(lista) == 8:
                        campo1 = str(lista[0])
                        busca1 = str(lista[1])
                        campo2 = str(lista[2])
                        busca2 = str(lista[3])
                        campo3 = str(lista[4])
                        busca3 = str(lista[5])
                        campo4 = str(lista[6])
                        busca4 = str(lista[7])

                        res = es.search(index="pessoas", body={"query":{"bool":{"should":[{"match":{campo1:busca1}},{"match":{campo2:busca2}},{"match":{campo3:busca3}},{"match":{campo4:busca4}}]}}})
                        return "O resultado é: " + str(res['hits']['total']['value'])

                if len(lista) not in [2,4,6,8]:
                        return "Reveja sua pesquisa"
                
        except:
                return "Error"
        
@app.route('/cidade/<int:num>', methods=['GET'])
def cidade(num):
        try:
                num = int(num)
                import requests, json
                lista = {}
                #não precisa de intervalo
                res = requests.get("http://localhost:9200/pessoas/_count?q=endereco.cidade:*")
                res.raise_for_status()
                obj = res.json()
                tamanho = range(1, int(obj["count"]))

                if num == 1:
                        for i in tamanho:
                                _id = str(id_function(i))
                                #return "Ok " + _id
                                res = requests.get("http://localhost:9200/pessoas/_doc/" + str(_id))
                                res.raise_for_status()
                                obj = res.json()
                                cidade = str(obj["_source"]["endereco"]["cidade"])
                        
                                if cidade not in lista.keys():
                                        lista[cidade] = 1
                                else:
                                        lista[cidade] = lista[cidade] + 1

                        popular = max(lista, key=lista.get)
                        return "A cidade mais populosa ao longo da história é: '" + str(popular) + "'"

                if num == 2:                
                        for i in tamanho:
                                _id = str(id_function(i))
                                #return "Ok " + _id
                                res = requests.get("http://localhost:9200/pessoas/_doc/" + str(_id))
                                res.raise_for_status()
                                obj = res.json()
                                cidade = str(obj["_source"]["endereco"]["cidade"])

                                if obj["_source"]["falecimento"]["data"] == "2999-01-01":
                                        if cidade not in lista.keys():
                                                lista[cidade] = 1
                                        else:
                                                lista[cidade] = lista[cidade] + 1

                        popular = max(lista, key=lista.get)
                        return "A cidade mais populosa no momento é: '" + str(popular) + "'"

                else:
                        return "Erro, rever a url."
                
        except:
                return "Error"        

@app.route('/familia/<int:num>', methods=['GET', 'POST'])
def familia(num):
        try:
                ##Essa api vai traçar a arvóre genealógica de qualquer pessoa, até os níveis dos avós, baseado em sua id. 
                ##Para usar, basta chamar: /familia/{id_desejada} ex: /familia/5
                _id = id_function(num)
                if str(_id) == "0000":
                        return "Usuário desconhecido ou inexistente"
                else:
                        pessoa = pesquisa(_id)
                        pessoa = pessoa.split("|")
                        pai = pesquisa(pessoa[0])
                        mae = pesquisa(pessoa[1])
                        ##
                        pai = pai.split("|")
                        mae = mae.split("|")
                        ##
                        pai_do_pai = pesquisa(pai[0])
                        mae_do_pai = pesquisa(pai[1])
                        ##
                        pai_da_mae = pesquisa(mae[0])
                        mae_da_mae = pesquisa(mae[1])
                        ##
                        pai_do_pai = pai_do_pai.split("|")
                        mae_do_pai = mae_do_pai.split("|")
                        pai_da_mae = pai_da_mae.split("|")
                        mae_da_mae = mae_da_mae.split("|")
                        ##
                        string = "Nome: " + pessoa[2]
                        string = string + "| Pai: " + pai[2]
                        string = string + "| Mãe: " + mae[2]
                        string = string + "| Avô Paterno: " + pai_do_pai[2]
                        string = string + "| Avó Paterna: " + mae_do_pai[2]
                        string = string + "| Avô Materno: " + pai_da_mae[2]
                        string = string + "| Avó Materna: " + mae_da_mae[2]
                        return string
                
        except:
                return "Error"
  
@app.route('/upload')
def upload_file():
        return render_template('upload.php')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
        from werkzeug.utils import secure_filename
        if request.method == 'POST':
                f = request.files['file']
                f.save(secure_filename(f.filename))
                return 'file uploaded successfully'

        
#@app.route('/search/<string:word>', methods=['GET'])
#def search(word):
#        try:
#                temp = word.split('|')
#                index = temp[0]
#                cor = temp[1]
#                filtro = '{ "query": { "match": { "favorite_color": "' + str(cor) + '" } } }'
#                file = open("filtro.json", "w")
#                file.write(filtro)
#                file.close()
#                resultado = subprocess.check_output('curl -XGET "localhost:9200/add/_search?pretty" -H "Content-Type: application/json" --data @filtro.json')
#                temp = resultado.decode('utf-8')
#                obj = json.loads(temp)
#                ###########
#                return "O número de pessoas que gosta de " + str(cor) + " é " + str(obj["hits"]["total"]["value"])
#
#        except:
#                return "Error"
#
#
        



if __name__ == '__main__':
        app.run(debug=True)

#possibilidade para extrair os  nomes: quebrar os elementos em lists e depois requebrar
#Exemplo interessante:
#x =  obj["hits"]["hits"]
#for i in x:
#        print(i)
#taca um split


#PASSADO

#@app.route('/search_nome/<string:word>', methods=['GET', 'POST']) ##usa query para pesquisar em qualquer campo
#def search_nome(word):
#        try:
#                import subprocess, json
#                #modelo de input: campo_pesquisado|busca
#                file = open("filtro_match.json")
#                filtro = file.read()
#                file.close()
#                lista = word.split("|")
#                filtro = filtro.replace("$campo",str(lista[0]))
#                filtro = filtro.replace("$busca",str(lista[1]))
#                #return "Ok"
#                file = open("filtro_match_temp.json", "w")
#                file.write(filtro)
#                file.close()
#                resultado = subprocess.check_output('curl -XGET "localhost:9200/pessoas/_search?pretty" -H "Content-Type: application/json" --data @filtro_match_temp.json')
#                #dá erro relacionado a middle bit uff-8 inválido, tenho a menor ideia do que seja
#                temp = resultado.decode('utf-8')
#                obj = json.loads(temp)                
#                return "O resultado é " + str(obj["hits"]["total"]["value"])
#        except:
#                return "Error"


#@app.route('/populacao', methods=['GET']) ##usa query para pesquisar a população atual
#def populacao():
#        try:
#              import subprocess, json
#              #não precisa de input, retorna a população atual
#              resultado = subprocess.check_output('curl -XGET "localhost:9200/pessoas/_search?pretty" -H "Content-Type: application/json" --data @populacao.json')
#              temp = resultado.decode('utf-8')
#              obj = json.loads(temp)
#              return "A população atual é " + str(obj["hits"]["total"]["value"])
#              
#        except:
#                return "Error" 




#@app.route('/idade_media', methods=['GET'])
#def idade_media():
#import json, subprocess
                #from datetime import date, datetime
                #resultado = subprocess.check_output('curl -XGET "localhost:9200/pessoas/_search?pretty" -H "Content-Type: application/json" --data @_source.json')
                #temp = resultado.decode('utf-8')
                #obj = json.loads(temp)
                #idade_total = 0
                #for element in obj['hits']['hits']:
                #        temp = str(element)
                #        temp = temp.split(",")
                #        #return "Ok"
                #        temp = temp[4]
                #        nascimento = str(temp[36:46])
                #        temp = nascimento.split("-")
                #        nascimento = datetime(int(temp[0]), int(temp[1]), int(temp[2]))
                #        today = date.today()
                #        idade = today.year - nascimento.year - ((today.month, today.day) < (nascimento.month, nascimento.day))
                #        idade_total = int(idade_total) + int(idade)
                #
                #idade_media = idade_total / int(obj['hits']['total']['value'])
                #return "A idade média da população é:" + str(idade_media)
		
		
#Velo search_date_range		
#import subprocess, json
#                #acessando a url /search_date_range/1990-11-01|2020-01-21 <--exemplo
#                lista = dates.split("|")
#                file = open("filtro_data.json")
#                filtro = file.read()
#                file.close()
#                filtro = filtro.replace("$data_inicial",str(lista[0]))
#                filtro = filtro.replace("$data_final",str(lista[1]))
#                file = open("filtro_data_temp.json", "w")
#                file.write(filtro)
#                file.close()
#                resultado = subprocess.check_output('curl -XGET "localhost:9200/pessoas/_search?pretty" -H "Content-Type: application/json" --data @filtro_data_temp.json')
#                temp = resultado.decode('utf-8')
#                obj = json.loads(temp)
#                if int(obj["hits"]["total"]["value"]) == 0:
#                        return "Erro nos termos de busca ou entrada inexistente."
#                else:
#                        return "O resultado é " + str(obj["hits"]["total"]["value"])
