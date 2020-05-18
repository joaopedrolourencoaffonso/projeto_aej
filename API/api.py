from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
        if (request.method == 'POST'):
                some_json = request.get_json()
                return jsonify({"you sent": some_json}), 201
        else:
                return jsonify({"about":"Hello World"})


@app.route('/multi/<int:num>', methods=['GET'])

def get_multiply10(num):
        return jsonify({'result': num*10})

#def hello():
#        return jsonify({"about":"Hello World!"})

if __name__ == '__main__':
        app.run(debug=True)
    #main()



#curl -H "Content-Type: application/json" -X POST --data-binary @test.json http://localhost:5000/
#{
#  "you sent": {
#    "address": "json street",
#    "name": "Jason"
#  }
#}
