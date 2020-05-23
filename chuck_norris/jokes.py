from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
        title = "index"
        return render_template("index.html", title=title)


@app.route('/jokes_api')
def jokes_api():
        import webbrowser, random, requests, json
        num = random.randint(1,100)
        res = requests.get("http://localhost:9200/jokes/_doc/" + str(num))
        res.raise_for_status()
        obj = res.json()
        return jsonify(piada=obj["_source"]["joke"])


@app.route('/jokes')
def jokes():
        return render_template('jokes.html')



if __name__ == "__main__":
    app.run(debug=True)
