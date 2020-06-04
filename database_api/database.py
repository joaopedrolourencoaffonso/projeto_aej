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

                _id = id_function(num)
                res = requests.get("http://localhost:9200/pessoas/_doc/" + str(_id))
                res.raise_for_status()
                obj = res.json()
                lista = str(obj["_source"]["pessoa"][0]).split(":")
                nome = lista[2].split(",")
                return "Nome: " + str(nome[0])
        except:
                return "Error "




#@app.route('/add/<string:word>', methods=['GET', 'POST'])
#def add(word):
#        try:
#                temp = word.split('|')
#                index = temp[0]
#                temp = temp[1]
#                temp = temp.split(',')
#                content = '{"nome":"' + str(temp[1]) + '","favorite_color":"' + str(temp[2]) + '"}'
#                file = open("add.json", "w")
#                file.write(content)
#                file.close()
#                subprocess.call('curl -H "Content-Type: application/json" --data @add.json http://localhost:9200/' + index +'/_doc/' + str(temp[0]) + '?pretty')
#                return content
#        except:
#                return "Error"

#@app.route('/exclude/<string:word>', methods=['GET', 'POST'])
#def exclude(word):
#        try:
#                temp = word.split('|')
#                index = temp[0]
#                _id = temp[1]
#                subprocess.call('curl -XDELETE http://localhost:9200/' + index +'/_doc/' + str(_id) + '?pretty')
#                return "Sucess!"
#                
#        except:
#                return "Error"
#
#
#@app.route('/show/<string:word>', methods=['GET'])
#def show(word):
#        try:
#                temp = word.split('|')
#                index = temp[0]
#                _id = temp[1]
#                res = requests.get("http://localhost:9200/" + str(index) + "/_doc/" + str(_id))
#                res.raise_for_status()
#                obj = res.json()
#                retorno = "Nome: " + str(obj["_source"]["nome"]) + " | Cor Favorita: " + str(obj["_source"]["favorite_color"])
#                return retorno
#
#        except:
#                return "Error"
#
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
