import sys, webbrowser, requests, json, subprocess

def main():
        for num in range(1,100):
                res = requests.get("http://api.icndb.com/jokes/random/")
                res.raise_for_status()
                obj = res.json()
                print(obj["value"]["joke"])
                joke = obj["value"]["joke"]
                string = '{ "joke":"' + str(joke) + '" }'
                file = open("database.json", "w")
                file.write(string)
                file.close()
                numero = str(num)
                subprocess.call('curl -H "Content-Type: application/json" --data @chuck.json http://localhost:9200/jokes/_doc/' + numero + '?pretty')
        

if __name__ == '__main__':
    main()

