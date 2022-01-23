from dependencies import *

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

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")    

@app.route("/plot", methods = ['POST'])
def plot():
    x,y,errx,erry = [],[],[],[]
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
                if (j == 2):
                    errx.append(dados[j+num_cols*i])
                if (j == 3):
                    erry.append(dados[j+num_cols*i])

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
                for j in i[1:-2]:
                    y.append(float(j))
                for j in i[2:-1]:
                    errx.append(float(j))
                for j in i[3:]:
                    erry.append(float(j))

    checked = 'errbar' in request.form
    if(checked): checked = request.form["errbar"]

    graph = Plot(x,y,errx,erry,error_bars = checked)

    graph.Title = request.form['Title']
    graph.xaxisTitle = request.form['X-Axis']
    graph.yaxisTitle = request.form['Y-Axis']

    graph.datacolor = request.form['data_colors']
    graph.fitcolor = request.form['fit_colors']

    if request.form['FitorInterpolate'] == "Fit":
        parameters = Parameters()
        for i in range(1,4):
            parameters.add(request.form[str("param" + str(i))], value = float(request.form[str("value" + str(i))]))
        graph.parameters = parameters
        graph.expression = request.form['function']
        temp_graph, report = graph.Make_Plot("Fit")             
        return render_template("plot.html", content = leitura, graph = temp_graph, size = len(x) ,num_cols = 4, fit_report = report,function = request.form['function'], Custom = custom,Report = True)
    
    elif request.form['FitorInterpolate'] == "Interpolate":
        temp_graph = graph.Make_Plot("Interpolate")            
        return render_template("plot.html", content = leitura, graph = temp_graph,size = len(x) ,num_cols = 4, num_pars = 0, Custom = custom)
    
    elif request.form['FitorInterpolate'] == "Plot":
        temp_graph = graph.Make_Plot("Scatter")            
        return render_template("plot.html", content = leitura, graph = temp_graph,size = len(x) , num_cols = 4,num_pars = 0, Custom = custom) 

if __name__ == "__main__":
    app.run(debug = True)


