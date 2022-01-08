from flask import Flask, redirect, url_for, render_template
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

@app.route('/plot')
def build_plot():
    img = io.BytesIO()

    leitura = read("data.csv")

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

    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return render_template("plot.html", content = leitura, graph = plot_url)

if __name__ == "__main__":
    app.run(port=8100)


