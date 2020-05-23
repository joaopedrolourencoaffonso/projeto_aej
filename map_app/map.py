from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
        title = "index"
        return render_template("index.html", title=title)


#@app.route('/api')
#def api():
#        import webbrowser, random, requests, json
#        num = random.randint(1,100)
#        res = requests.get("http://localhost:9200/jokes/_doc/" + str(num))
#        res.raise_for_status()
#        obj = res.json()
#        return jsonify(piada=obj["_source"]["joke"])


@app.route('/map')
def map():
        import webbrowser, requests
        res = requests.get("https://api.wheretheiss.at/v1/satellites/25544")
        obj = res.json()
        var1 = str(obj["longitude"])
        var2 = str(obj["latitude"])
        return render_template('map.html', var1=var1, var2=var2)



if __name__ == "__main__":
    app.run(debug=True)
