from flask import Flask, redirect, flash,url_for, render_template,request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import os
import base64
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from scipy.interpolate import CubicSpline
import numpy as np
from scipy.optimize import curve_fit

UPLOAD_FOLDER = '/static'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
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

def Fit_to_Function(x,y):
    #Fazer plot do ficheiro
    img = io.BytesIO()
    parametros,seila = curve_fit(func, x, y)
    x_continuo = np.linspace(min(x),max(x),1000)
    plt.plot(x,y,'o',x_continuo, func(x_continuo,*parametros), '-',)
    plt.legend(['Data', 'Fit'], loc='best')
    plt.savefig(img, format='png')
    img.seek(0)
    plt.clf()

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url, parametros

def Interpolate(x,y):
    #Fazer plot do ficheiro
    img = io.BytesIO()
    cs = CubicSpline(x,y,bc_type='natural')
    x_continuo = np.linspace(min(x),max(x),1000)
    plt.plot(x,y,'o',x_continuo, cs(x_continuo), '-',)
    plt.legend(['Data', 'Cubic Spline'], loc='best')
    plt.savefig(img, format='png')
    img.seek(0)
    plt.clf()

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url

def func(x,a,b):
    return a+b*x 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")    

@app.route("/plot", methods = ['POST'])
def plot():
    if request.method == "POST" and request.form['FileorText'] == "Input":
        dados = request.form['data']

        dados = str(dados)
        dados = dados.replace(";"," ").replace(","," ").split()
        dados_string = dados
        dados = [float(i) for i in dados]
        x,y = [],[]

        num_cols = 4
        length = int((len(dados))/num_cols)
        for i in range(0,length):
            for j in range(0,4):
                if (j == 0):
                    x.append(dados[j+num_cols*i])
                if (j == 1):
                    y.append(dados[j+num_cols*i])

        if request.form['FitorInterpolate'] == "Fit":
            temp_graph, temp_pars = Fit_to_Function(x,y)    
            return render_template("plot_custom.html", content = dados_string, graph = temp_graph, size = length, num_cols = 4, freepars = temp_pars, num_pars = len(temp_pars))

        elif request.form['FitorInterpolate'] == "Interpolate":
            temp_graph = Interpolate(x,y)   
            return render_template("plot_custom.html", content = dados_string, graph = temp_graph, size = length, num_cols = 4, num_pars = 0) 

    elif request.method == "POST" and request.form['FileorText'] == "File":
        #Upload do ficheiro
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)
            leitura = read(uploaded_file.filename)
            x,y = [],[]

            for i in leitura:
                for j in i[:-3]:
                    x.append(float(j))

            for i in leitura:
                for j in i[1:-2]:
                        y.append(float(j))  

            if request.form['FitorInterpolate'] == "Fit":
                temp_graph, temp_pars = Fit_to_Function(x,y)             
                return render_template("plot_excel.html", content = leitura, graph = temp_graph, freepars = temp_pars, num_pars = len(temp_pars))
            
            elif request.form['FitorInterpolate'] == "Interpolate":
                temp_graph = Interpolate(x,y)             
                return render_template("plot_excel.html", content = leitura, graph = temp_graph, num_pars = 0) 

if __name__ == "__main__":
    app.run(debug = True)


