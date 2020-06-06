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
       
@app.route('/search_nome/<string:word>', methods=['GET', 'POST'])
def search_nome(word):
        try:
                import subprocess, json
                #modelo de input: campo_pesquisado|busca
                file = open("filtro_match.json")
                filtro = file.read()
                file.close()
                lista = word.split("|")
                filtro = filtro.replace("$campo",str(lista[0]))
                filtro = filtro.replace("$busca",str(lista[1]))
                #return "Ok"
                file = open("filtro_match_temp.json", "w")
                file.write(filtro)
                file.close()
                resultado = subprocess.check_output('curl -XGET "localhost:9200/pessoas/_search?pretty" -H "Content-Type: application/json" --data @filtro_match_temp.json')
                #dá erro relacionado a middle bit uff-8 inválido, tenho a menor ideia do que seja
                temp = resultado.decode('utf-8')
                obj = json.loads(temp)                
                return "O resultado é " + str(obj["hits"]["total"]["value"])
        except:
                return "Error"



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
