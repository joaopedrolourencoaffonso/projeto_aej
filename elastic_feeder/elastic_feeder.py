from flask import Flask, jsonify, request
import subprocess, json, requests

app = Flask(__name__)

@app.route('/', methods=['GET'])

def index():
        return "Hello Moon!"



@app.route('/add/<string:word>', methods=['GET', 'POST'])
def add(word):
        try:
                temp = word.split('|')
                index = temp[0]
                temp = temp[1]
                temp = temp.split(',')
                content = '{"nome":"' + str(temp[1]) + '","favorite_color":"' + str(temp[2]) + '"}'
                file = open("add.json", "w")
                file.write(content)
                file.close()
                subprocess.call('curl -H "Content-Type: application/json" --data @add.json http://localhost:9200/' + index +'/_doc/' + str(temp[0]) + '?pretty')
                return content
        except:
                return "Error"

@app.route('/exclude/<string:word>', methods=['GET', 'POST'])
def exclude(word):
        try:
                temp = word.split('|')
                index = temp[0]
                _id = temp[1]
                subprocess.call('curl -XDELETE http://localhost:9200/' + index +'/_doc/' + str(_id) + '?pretty')
                return "Sucess!"
                
        except:
                return "Error"


@app.route('/show/<string:word>', methods=['GET'])
def show(word):
        try:
                temp = word.split('|')
                index = temp[0]
                _id = temp[1]
                res = requests.get("http://localhost:9200/" + str(index) + "/_doc/" + str(_id))
                res.raise_for_status()
                obj = res.json()
                retorno = "Nome: " + str(obj["_source"]["nome"]) + " | Cor Favorita: " + str(obj["_source"]["favorite_color"])
                return retorno

        except:
                return "Error"

if __name__ == '__main__':
        app.run(debug=True)

