from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
        return render_template('index.php')
        
@app.route('/somar/<string:numeros>', methods=['GET'])
def somar(numeros):
        numeros = numeros.split('+')
        resultado = int(numeros[0]) + int(numeros[1])
        return jsonify({'resultado':str(resultado)})
        
@app.route('/subtrair/<string:numeros>', methods=['GET'])
def subtrair(numeros):
        numeros = numeros.split('-')
        resultado = int(numeros[0]) - int(numeros[1])
        return jsonify({'resultado':str(resultado)})
        
@app.route('/multiplicar/<string:numeros>', methods=['GET'])
def multiplicar(numeros):
        numeros = numeros.split('*')
        resultado = int(numeros[0]) * int(numeros[1])
        return jsonify({'resultado':str(resultado)})
        
@app.route('/dividir/<string:numeros>', methods=['GET'])
def dividir(numeros):
        numeros = numeros.split(':')
        resultado = int(numeros[0]) / int(numeros[1])
        return jsonify({'resultado':str(resultado)})

if __name__ == '__main__':
        app.run(debug=True)
