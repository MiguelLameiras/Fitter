from dependencies import *

class Plot:
    def __init__(self,x,y,xerr,yerr,expression = None,parameters = None, error_bars = None, Title = "Title", xaxisTitle = "X-Axis", yaxisTitle = "Y-Axis"):
        self.x = x
        self.y = y
        self.xerr = xerr
        self.yerr = yerr
        self.error_bars = error_bars
        self.expression = expression
        self.parameters = parameters
        self.Title = Title
        self.xaxisTitle = xaxisTitle
        self.yaxisTitle = yaxisTitle
        self.datacolor = 'black'
        self.fitcolor = 'blue'

    def Make_Plot(self,plot):
        #Fazer plot do ficheiro
        img = io.BytesIO()
        if(plot == "Fit" ):
            #Calcular o fit da função
            function = ExpressionModel(self.expression)
            params = self.parameters
            result = function.fit(self.y, params, x=self.x)
            #Criar uma função continua com o fit
            x_continuo = np.linspace(min(self.x),max(self.x),1000)
            new_prediction = result.eval(x=x_continuo)
            #Plot do fit
            if(self.error_bars == "Yes"):
                plt.errorbar(self.x, self.y, xerr = self.xerr, yerr = self.yerr,fmt='.',color = self.datacolor ,ecolor = self.datacolor, capthick=1, capsize=5)
                plt.plot(x_continuo,new_prediction, 'r', color = self.fitcolor)
            else:
                plt.plot(self.x,self.y,'.',color = self.datacolor)
                plt.plot(x_continuo,new_prediction, 'r',color = self.fitcolor)

        elif(plot == "Interpolate" ):      
            cs = CubicSpline(self.x,self.y,bc_type='natural')
            x_continuo = np.linspace(min(self.x),max(self.x),1000)
            #Plot do fit
            if(self.error_bars == "Yes"):
                plt.errorbar(self.x, self.y, xerr = self.xerr, yerr = self.yerr,fmt='.',color = self.datacolor ,ecolor = self.datacolor, capthick=1, capsize=5)
                plt.plot(x_continuo,cs(x_continuo), 'r',color = self.fitcolor)
            else:
                plt.plot(self.x,self.y,'.',color = self.datacolor)
                plt.plot(x_continuo,cs(x_continuo), 'r',color = self.fitcolor)  
        
        if(plot == "Scatter" ):  
            #Plot do fit
            if(self.error_bars == "Yes"):
                plt.errorbar(self.x, self.y, xerr = self.xerr, yerr = self.yerr,fmt='.',color = self.datacolor ,ecolor = self.datacolor,capthick=1, capsize=5)
            else:
                plt.plot(self.x,self.y,'.',color = self.datacolor)      

        #Titulos dos eixos
        plt.title(self.Title, fontsize=18)
        plt.xlabel(self.xaxisTitle, fontsize=18)
        plt.ylabel(self.yaxisTitle, fontsize=18)
        #Adicionar Legenda
        plt.legend(['Data', 'Fit'], loc='best')

        ax = plt.gca()
        ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
        ax.yaxis.set_minor_locator(tck.AutoMinorLocator())

        plt.savefig(img, format='png', dpi = 300)
        img.seek(0)
        plt.clf()

        plot_url = base64.b64encode(img.getvalue()).decode()
        
        if(plot == "Fit"):
            return plot_url, result.fit_report()

        else:
            return plot_url
