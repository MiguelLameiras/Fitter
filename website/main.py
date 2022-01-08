from flask import Flask, redirect, url_for, render_template,request
import matplotlib.pyplot as plt
import io
import base64

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
    return render_template("index.html")

@app.route("/", methods = ['POST'])
def dados_input():
    dados = request.form['data']

    dados = str(dados)
    dados = dados.replace(";"," ").split()
    dados_string = dados
    dados = [float(i) for i in dados]
    print(dados_string)
    x,y = [],[]

    num_cols = 4
    length = int((len(dados))/num_cols-num_cols)
    for i in range(0,length):
        for j in range(0,4):
            if (j == 0):
                x.append(dados[j+num_cols*i])
            if (j == 1):
                y.append(dados[j+num_cols*i])

    plt.plot(x,y)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.clf()

    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return render_template("plot_custom.html", content = dados_string, graph = plot_url,size = length, num_cols = 4)

@app.route('/plot')
def build_plot():
    img = io.BytesIO()

    leitura = read("data.csv")
    print(leitura)
    x,y = [],[]

    for i in leitura:
        for j in i[:-3]:
                x.append(float(j))

    for i in leitura:
        for j in i[1:-2]:
                y.append(float(j))           

    plt.plot(x,y)
    plt.savefig(img, format='png')
    img.seek(0)
    plt.clf()

    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return render_template("plot_excel.html", content = leitura, graph = plot_url)

if __name__ == "__main__":
    app.run(port=8100)


