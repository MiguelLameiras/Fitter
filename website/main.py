from ctypes import sizeof
import re
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
from lmfit.models import ExpressionModel
from lmfit import Parameters,model

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

def Fit_to_Function(expression,x,y,parameters):
    #Fazer plot do ficheiro
    img = io.BytesIO()
    #Calcular o fit da função
    function = ExpressionModel(expression)
    params = parameters
    result = function.fit(y, params, x=x)
    #Criar uma função continua com o fit
    x_continuo = np.linspace(min(x),max(x),1000)
    new_prediction = result.eval(x=x_continuo)
    #Plot do fit
    plt.plot(x,y,'o',x_continuo,new_prediction, 'r')
    plt.legend(['Data', 'Fit'], loc='best')
    plt.savefig(img, format='png')
    img.seek(0)
    plt.clf()

    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return plot_url, result.fit_report()

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

def Scatter(x,y):
    #Fazer plot do ficheiro
    img = io.BytesIO()
    plt.plot(x,y,'o')
    plt.legend(['Data'], loc='best')
    plt.savefig(img, format='png')
    img.seek(0)
    plt.clf()

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url

def func(x,a,b):
    return a*np.sin(b*x) 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")    

@app.route("/plot", methods = ['POST'])
def plot():
    x,y = [],[]
    if request.method == "POST" and request.form['FileorText'] == "Input":
        dados = request.form['data']
        custom = True

        dados = str(dados)
        dados = dados.replace(";"," ").replace(","," ").split()
        leitura = dados
        dados = [float(i) for i in dados]

        num_cols = 4
        for i in range(0,int((len(dados))/num_cols)):
            for j in range(0,4):
                if (j == 0):
                    x.append(dados[j+num_cols*i])
                if (j == 1):
                    y.append(dados[j+num_cols*i])

    elif request.method == "POST" and request.form['FileorText'] == "File":
        custom = False
        #Upload do ficheiro
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)
            leitura = read(uploaded_file.filename)

            for i in leitura:
                for j in i[:-3]:
                    x.append(float(j))

            for i in leitura:
                for j in i[1:-2]:
                    y.append(float(j))

    if request.form['FitorInterpolate'] == "Fit":
        parameters = Parameters()
        for i in range(1,4):
            parameters.add(request.form[str("param" + str(i))], value = float(request.form[str("value" + str(i))]))
        temp_graph, report = Fit_to_Function(request.form['function'],x,y,parameters)             
        return render_template("plot.html", content = leitura, graph = temp_graph, size = len(x) ,num_cols = 4, fit_report = report,function = request.form['function'], Custom = custom,Report = True)
    
    elif request.form['FitorInterpolate'] == "Interpolate":
        temp_graph = Interpolate(x,y)             
        return render_template("plot.html", content = leitura, graph = temp_graph, num_pars = 0, Custom = custom)
    
    elif request.form['FitorInterpolate'] == "Plot":
        temp_graph = Scatter(x,y)             
        return render_template("plot.html", content = leitura, graph = temp_graph, num_pars = 0, Custom = custom) 

if __name__ == "__main__":
    app.run(debug = True)


