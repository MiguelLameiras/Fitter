from pyexpat.errors import XML_ERROR_ABORTED
from dependencies import *

class Plot:
    def __init__(self,x,y,xerr,yerr,xerror = None, yerror = None,expression = None,parameters = None,xlog = None , ylog = None, Title = "Title", xaxisTitle = "X-Axis", yaxisTitle = "Y-Axis"):
        self.x = x
        self.y = y
        self.xerr = xerr
        self.yerr = yerr
        self.xerror = xerror
        self.yerror = yerror
        self.expression = expression
        self.parameters = parameters
        self.Title = Title
        self.xaxisTitle = xaxisTitle
        self.yaxisTitle = yaxisTitle
        self.datacolor = 'black'
        self.fitcolor = 'blue'
        self.xlog = xlog
        self.ylog = ylog
        self.xmin = 0
        self.ymin = -2
        self.xmax = 10
        self.ymax = 2
        self.xauto = 0
        self.yauto = 0
        self.xticks = 1
        self.yticks = 1

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
            if(self.xerror == "Yes" and self.yerror == "Yes" ):
                plt.errorbar(self.x, self.y, xerr = self.xerr, yerr = self.yerr,markersize=3,fmt='.',color = self.datacolor ,ecolor = self.datacolor, capthick=1, capsize=5)
                plt.plot(x_continuo,new_prediction, 'r',linewidth=1.3, color = self.fitcolor)
            elif(self.xerror == "Yes"):
                plt.errorbar(self.x, self.y, xerr = self.xerr,markersize=3,fmt='.',color = self.datacolor ,ecolor = self.datacolor, capthick=1, capsize=5)
                plt.plot(x_continuo,new_prediction, 'r',linewidth=1.3, color = self.fitcolor)
            elif(self.yerror == "Yes"):
                plt.errorbar(self.x, self.y, yerr = self.yerr,markersize=3,fmt='.',color = self.datacolor ,ecolor = self.datacolor, capthick=1, capsize=5)
                plt.plot(x_continuo,new_prediction, 'r',linewidth=1.3, color = self.fitcolor)
            else:
                plt.plot(self.x,self.y,'.', markersize=3,color = self.datacolor)
                plt.plot(x_continuo,new_prediction, 'r',linewidth=1.3,color = self.fitcolor)

        elif(plot == "Interpolate" ):      
            cs = CubicSpline(self.x,self.y,bc_type='natural')
            x_continuo = np.linspace(min(self.x),max(self.x),1000)
            #Plot do fit
            if(self.xerror == "Yes" and self.yerror == "Yes" ):
                plt.errorbar(self.x, self.y, xerr = self.xerr, yerr = self.yerr,fmt = '.', markersize=3,color = self.datacolor ,ecolor = self.datacolor, capthick=1, capsize=5)
                plt.plot(x_continuo,cs(x_continuo), 'r',color = self.fitcolor)
            elif(self.xerror == "Yes"):
                plt.errorbar(self.x, self.y, xerr = self.xerr,fmt = '.', markersize=3,color = self.datacolor ,ecolor = self.datacolor, capthick=1, capsize=5)
                plt.plot(x_continuo,cs(x_continuo), 'r',color = self.fitcolor)
            elif(self.yerror == "Yes"):
                plt.errorbar(self.x, self.y, yerr = self.yerr,fmt = '.', markersize=3,color = self.datacolor ,ecolor = self.datacolor, capthick=1, capsize=5)
                plt.plot(x_continuo,cs(x_continuo), 'r',color = self.fitcolor)
            else:
                plt.plot(self.x,self.y, '.',markersize=3,color = self.datacolor)
                plt.plot(x_continuo,cs(x_continuo), 'r',color = self.fitcolor)  
        
        if(plot == "Scatter" ):  
            #Plot do fit
            if(self.xerror == "Yes" and self.yerror == "Yes" ):
                plt.errorbar(self.x, self.y,markersize=3, xerr = self.xerr, yerr = self.yerr,fmt='.',color = self.datacolor ,ecolor = self.datacolor,capthick=1, capsize=5)
            elif(self.xerror == "Yes"):
                plt.errorbar(self.x, self.y,markersize=3, xerr = self.xerr,fmt='.',color = self.datacolor ,ecolor = self.datacolor,capthick=1, capsize=5)
            elif(self.yerror == "Yes"):
                plt.errorbar(self.x, self.y,markersize=3, yerr = self.yerr,fmt='.',color = self.datacolor ,ecolor = self.datacolor,capthick=1, capsize=5)
            else:
                plt.plot(self.x,self.y, '.',markersize=3,color = self.datacolor)      

        #Titulos dos eixos
        plt.title(self.Title, fontsize=18)
        plt.xlabel(self.xaxisTitle, fontsize=18)
        plt.ylabel(self.yaxisTitle, fontsize=18)
        #Adicionar Legenda
        plt.legend(['Arduino Data', 'Fit'], loc='best')

        ax = plt.gca()
        if(self.xlog): ax.set_xscale(self.xlog)
        else:
            if(self.xauto == 0):
                ax.set_xlim([self.xmin, self.xmax])
                ax.xaxis.set_major_locator(tck.MultipleLocator(base=self.xticks))# this locator puts ticks at regular intervals
        if(self.ylog): ax.set_yscale(self.ylog)
        else:
            if(self.yauto == 0):
                ax.set_ylim([self.ymin, self.ymax])
                ax.yaxis.set_major_locator(tck.MultipleLocator(base=self.yticks))# this locator puts ticks at regular intervals

        
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
