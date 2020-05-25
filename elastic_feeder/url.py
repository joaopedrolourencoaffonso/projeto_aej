from flask import Flask

app = Flask(__name__)

@app.route('/default', defaults={'name':"Pretty"})
@app.route('/default/<name>')
def default(name):
        return 'the value is: ' + name


@app.route('/string/<string:name>')
def string(name):
        return "The String is: " + name

@app.route('/intro/<int:mynum>')
def introroute(mynum):
        return 'The number is: ' + str(mynum)

@app.route('/float/<float:myfloat>')
def myfloat(myfloat):
        return "the float: " + str(myfloat)

@app.route('/pathroute/<path:mypath>')
def pathroute(mypath):
        return 'The path is: ' + mypath

@app.route('/combine/<string:mystring>/<int:myint>')
def combine(mystring, myint):
        return 'The string is: ' + str(mystring) + "The int is: " + str(myint)

if __name__ == '__main__':
        app.run(debug=True)
