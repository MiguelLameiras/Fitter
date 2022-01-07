from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


def check_float(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:
        return False

def read(file_path):
  
  file = open(file_path,'r')
  leitura = []
  for line in file:
    lido = line.strip().split(";")
    if(check_float(lido[0]) == False):
        leitura.append(lido)
    else:
        leitura.append(lido)

  file.close()

  return leitura



@app.route("/")
def home():
    leitura = read("data.csv")
    return render_template("index.html",content = leitura)

if __name__ == "__main__":
    app.run(port=8100)