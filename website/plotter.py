from dependencies import *

class Plot:
    def __init__(self,x,y,xerr,yerr,expression = None,parameters = None, error_bars = None):
        self.x = x
        self.y = y
        self.xerr = xerr
        self.yerr = yerr
        self.error_bars = error_bars
        self.expression = expression
        self.parameters = parameters

    def Fit_to_Function(self):
        #Fazer plot do ficheiro
        img = io.BytesIO()
        #Calcular o fit da função
        function = ExpressionModel(self.expression)
        params = self.parameters
        result = function.fit(self.y, params, x=self.x)
        #Criar uma função continua com o fit
        x_continuo = np.linspace(min(self.x),max(self.x),1000)
        new_prediction = result.eval(x=x_continuo)
        #Plot do fit
        if(self.error_bars == "Yes"):
            plt.errorbar(self.x, self.y, xerr = self.xerr, yerr = self.yerr,fmt='o', capthick=1, capsize=5)
            plt.plot(x_continuo,new_prediction, 'r')
        else:
            plt.plot(self.x,self.y,'o',x_continuo,new_prediction, 'r')
        plt.legend(['Data', 'Fit'], loc='best')
        plt.savefig(img, format='png')
        img.seek(0)
        plt.clf()

        plot_url = base64.b64encode(img.getvalue()).decode()
        
        return plot_url, result.fit_report()

    def Interpolate(self):
        #Fazer plot do ficheiro
        img = io.BytesIO()
        cs = CubicSpline(self.x,self.y,bc_type='natural')
        x_continuo = np.linspace(min(self.x),max(self.x),1000)
        #Plot do fit
        if(self.error_bars == "Yes"):
            plt.errorbar(self.x, self.y, xerr = self.xerr, yerr = self.yerr,fmt='o', capthick=1, capsize=5)
            plt.plot(x_continuo,cs(x_continuo), 'r')
        else:
            plt.plot(self.x,self.y,'o',x_continuo,cs(x_continuo), 'r')
        plt.legend(['Data', 'Cubic Spline'], loc='best')
        plt.savefig(img, format='png')
        img.seek(0)
        plt.clf()

        plot_url = base64.b64encode(img.getvalue()).decode()

        return plot_url

    def Scatter(self):
        #Fazer plot do ficheiro
        img = io.BytesIO()
        #Plot do fit
        if(self.error_bars == "Yes"):
            plt.errorbar(self.x, self.y, xerr = self.xerr, yerr = self.yerr,fmt='o', capthick=1, capsize=5)
        else:
            plt.plot(self.x,self.y,'o')
        plt.legend(['Data'], loc='best')
        plt.savefig(img, format='png')
        img.seek(0)
        plt.clf()

        plot_url = base64.b64encode(img.getvalue()).decode()

        return plot_url