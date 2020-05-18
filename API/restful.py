from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
        def get(self):
                return {'about':'Hello World'}

        def post(self):
                some_json = request.get_json()
                return {'you sent': some_json}, 201

class Multi(Resource):
        def get(self, num):
                return {'result': num*6}

api.add_resource(HelloWorld, '/')
api.add_resource(Multi, '/multi/<int:num>')

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
