#!/usr/bin/env python

from gi.repository import Gtk as gtk


from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

import numpy as np
from numpy import arange, sin, pi

import statsmodels.api as sm

import pandas as pd
from pandas import DataFrame
import pandas.io.data

import datetime

import re

class PlotBox():
    def __init__(self):
        self.fig=Figure(figsize=(4,3), dpi=50)
        self.canvas=FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.vbox=gtk.VBox()
        self.vbox.pack_start(self.canvas, True, True, 0)
        self.vbox.pack_start(self.toolbar, False, False, 0)

class ProduceOutput():
    def __init__(self):
        self.ResultsTable=gtk.Table(3,6,True)
        
    def Label(self,txt):
        return 
        
class AdvanceGrapher(gtk.Window):
    
    def __init__(self):
        gtk.Window.__init__(self,title="AdvanceGrapher")
        self.df=DataFrame
        
        self.set_default_size(300, 600)
        
        self.mainTable=gtk.Table(16,8,True)
        self.add(self.mainTable)
        
        
        self.btnChooseFile=gtk.Button(label="File")
        self.btnChooseFile.connect("clicked",self.btnChooseFile_clicked)
        
        self.btnLoadData=gtk.Button(label="Load")
        self.btnLoadData.connect("clicked",self.btnLoadData_clicked)
        
        self.btnPlotDependentVar=gtk.Button(label="Plot")
        self.btnPlotDependentVar.connect("clicked",self.btnPlotDependentVar_clicked)
        self.btnAddToExog=gtk.Button(label="Add to Exog")
        self.btnAddToExog.connect("clicked",self.btnAddToExog_clicked)
        self.btnRemoveFromExog=gtk.Button(label="Remove from Exog")
        self.btnRemoveFromExog.connect("clicked",self.btnRemoveFromExog_clicked)
        
        self.btnFitModel=gtk.Button(label="Fit Mofel")
        self.btnFitModel.connect("clicked",self.btnFitModel_clicked)
        self.entryOrderAR=gtk.Entry()
        self.entryOrderMA=gtk.Entry()
        self.mainTable.attach(gtk.Label("AR"),0,1,10,11)
        self.mainTable.attach(gtk.Label("MA"),0,1,11,12)
        self.mainTable.attach(self.entryOrderAR,1,2,10,11)
        self.mainTable.attach(self.entryOrderMA,1,2,11,12)
        self.mainTable.attach(gtk.Label("Cutoff Time"), 0,1,12,13)
        self.CutoffTimeList=gtk.ListStore(int, str)
        self.CutoffTimeCombo = gtk.ComboBox.new_with_model_and_entry(self.CutoffTimeList)
        self.CutoffTimeCombo.set_entry_text_column(1)
        self.mainTable.attach(self.btnFitModel,0,1,13,14)
        self.mainTable.attach(self.CutoffTimeCombo,1,2,12,13)
        
        self.entryFileName=gtk.Entry()
        self.entryFileName.set_text("/home/timur/ProjectsLocal/Data/DFAST2015/DFAST2015base.csv")
        
        self.ListOfVars = gtk.ListStore(int, str)
        self.DependentVarCombo = gtk.ComboBox.new_with_model_and_entry(self.ListOfVars)
        self.DependentVarCombo.set_entry_text_column(1)
        
        self.ListOfVars.append([1,'hello'])
        self.ListOfVars.append([2,'world'])
        self.sampleTreeView=gtk.TreeView(self.ListOfVars)
        
        self.ListOfExogVars=gtk.ListStore(int, str)
        self.ListOfExogVarsCombo = gtk.ComboBox.new_with_model_and_entry(self.ListOfExogVars)
        self.ListOfExogVarsCombo.set_entry_text_column(1)
        

        self.pbox1=PlotBox()
        self.pbox2=PlotBox()
        
        self.mainTable.attach(self.btnChooseFile,0,1,0,1)
        self.mainTable.attach(self.entryFileName,2,5,0,1)
        self.mainTable.attach(self.btnLoadData,1,2,0,1)
        
        self.mainTable.attach(gtk.Label("Dependent Var"), 0,1,1,2)
        self.mainTable.attach(gtk.Label("Exogen Vars"), 0,1,4,5)
        self.mainTable.attach(self.btnAddToExog,1,2,3,4)
        self.mainTable.attach(self.ListOfExogVarsCombo, 1,2,4,5)
        self.mainTable.attach(self.btnRemoveFromExog,1,2,5,6)
        
        
        self.mainTable.attach(self.DependentVarCombo, 1,2,1,2)
        self.mainTable.attach(self.btnPlotDependentVar,1,2,2,3)
        self.mainTable.attach(self.pbox1.vbox, 2,5,1,14)
        self.mainTable.attach(self.pbox2.vbox, 5,8,7,14)
        

        self.ResultsWindow=gtk.ScrolledWindow()
        self.ResultsWindow.set_hexpand(True)
        self.ResultsWindow.set_vexpand(True)
        #self.ResultsLabel.set_justify(gtk.Justification.LEFT)
        # self.ResultsLabel.set_margin_top(0)
        #self.ResultsLabel.set_margin_left(0)
        #print dir(self.ResultsLabel)
        self.mainTable.attach(self.ResultsWindow,5,8,0,7)
        
        self.textview = gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("This is some text inside of a Gtk.TextView. "
            + "Select text and click one of the buttons 'bold', 'italic', "
            + "or 'underline' to modify the text accordingly.")
        self.ResultsWindow.add(self.textview)
        
  
        
    def btnRemoveFromExog_clicked(self,widget):
        activeIter=self.ListOfExogVarsCombo.get_active_iter()
        model=self.ListOfExogVarsCombo.get_model()
        self.ListOfExogVars.remove(activeIter)
        return 0
     
    def btnAddToExog_clicked(self,widget):
        #self.ListOfVars.append([i, self.df.columns[i]])
        #self.ListOfExogVarsCombo
        print dir(self.ListOfExogVars)
        print len(self.ListOfExogVars)
        print self.Variable
        self.ListOfExogVars.append([len(self.ListOfExogVars),self.Variable])
        return 0
       
    def btnFitModel_clicked(self,widget):
        #model = sm.tsa.arima_model.ARMA(self.df[Variable], (2, 2)).fit(trend='nc', disp=0)
        exogvars=[]
        for i in range(0,len(self.ListOfExogVars)):
            exogvars.append(self.ListOfExogVars[0].model[i][1])

        activeIter=self.CutoffTimeCombo.get_active_iter()
        cutoff=self.CutoffTimeCombo.get_model()
        cutoff2=cutoff[activeIter][0]
        print cutoff[activeIter][0]
        
        AR=int(self.entryOrderAR.get_text())
        MA=int(self.entryOrderMA.get_text())
        
        #print self.df[exogvars]
        
        if len(exogvars)>0:
            model=sm.tsa.ARMA(self.df[self.Variable][0:cutoff2],(AR,MA),exog=self.df[exogvars][0:cutoff2])
            results=model.fit()
            #oot=results.predict(start=cutoff2,exog=self.df[exogvars])
            oot=results.forecast(steps=len(self.df)-cutoff2, exog=self.df[exogvars][cutoff2:len(self.df)])
            #oot_series=pd.Series(oot[0],self.df.index[cutoff2:len(self.df)])
            
        else:
            model=sm.tsa.ARMA(self.s[0:cutoff2],(AR,MA))
            results=model.fit()
            oot=results.forecast(steps=len(self.df)-cutoff2)
            #print len(self.df)-cutoff2
            #oot_series=pd.Series(oot[0],self.df.index[cutoff2:len(self.df)])
            #self.df['forecast']=oot_series
            #oot=results.predict(start=self.df.index[cutoff2-1])
        
        oot_95l=pd.Series(oot[2][:,0],self.df.index[cutoff2:len(self.df)])
        oot_95u=pd.Series(oot[2][:,1],self.df.index[cutoff2:len(self.df)])
        oot_series=pd.Series(oot[0],self.df.index[cutoff2:len(self.df)])
        self.df['forecast']=oot_series
        self.df['95l']=oot_95l
        self.df['95u']=oot_95u
        
        #print str(results.summary())
        #print type(str(results.summary()))
        SummaryStr=str(results.summary2())
        
        #SummaryStr=re.sub('\n','',SummaryStr)
        #self.ResultsLabel.set_text(SummaryStr)
        self.textbuffer.set_text(SummaryStr)

        self.pbox2.fig.clf(keep_observers=True)
        a=self.pbox2.fig.add_subplot(111, title='Out of time Forecast')
        a.plot(self.df.index,self.df[self.Variable],label='Actual',color="blue")
        a.plot(self.df.index,self.df['forecast'],label='Forecast',color="red")
        a.plot(self.df.index,self.df['95l'],label='95% Conf',color="green",linestyle="--")
        a.plot(self.df.index,self.df['95u'],color="green",linestyle="--")
        a.legend(loc="best")
        self.pbox2.canvas.draw()
        
        print 'hello'
        print SummaryStr
        print 'world'
        print results.params[1]
        print results.pvalues
        
        return 0
    
    def btnPlotDependentVar_clicked(self,widget):
        activeIter=self.DependentVarCombo.get_active_iter()
        model=self.DependentVarCombo.get_model()
        Variable=model[activeIter][1]
        self.Variable=Variable
        self.pbox1.fig.clf(keep_observers=True)
        a=self.pbox1.fig.add_subplot(311,title=Variable)
        
        self.s = self.df[Variable]
        a.plot(self.df.index,self.df[Variable])
        
        b=self.pbox1.fig.add_subplot(312)
        sm.graphics.tsa.plot_acf(self.s,ax=b,lags=12,alpha=.05)
        b=self.pbox1.fig.add_subplot(313)
        sm.graphics.tsa.plot_pacf(self.s,ax=b,lags=12,alpha=.05)
        self.pbox1.canvas.draw()
        
        #acf=sm.tsa.stattools.acf(s,nlags=12, qstat=True, alpha=.05)
        #pacf=sm.tsa.stattools.pacf(s,nlags=12)

        return 0
    
    def DependentVarCombo_changed(self, combo):
        
        return 0
    
    
    def btnChooseFile_clicked(self,widget):
        dialog = gtk.FileChooserDialog("Please choose a file", self,
            gtk.FileChooserAction.OPEN,
            (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
             gtk.STOCK_OPEN, gtk.ResponseType.OK))
    
        self.add_filters(dialog)
    
        response = dialog.run()
        if response == gtk.ResponseType.OK:
            self.entryFileName.set_text(dialog.get_filename())
        dialog.destroy()

    
    def btnLoadData_clicked(self,widget):
        self.ListOfVars.clear()
        self.df = pd.read_csv(self.entryFileName.get_text(), index_col='Date', parse_dates=True)
        for i in range(0,len(self.df.columns)):
            self.ListOfVars.append([i, self.df.columns[i]])
            print self.df.columns[i]
            
        print self.df.index[3]
        print len(self.df.index)
        for i in range(0,len(self.df.index)):
            self.CutoffTimeList.append([i,str(self.df.index[i])])
        return 0
    
    def add_filters(self, dialog):
        filter_text = gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)


win = AdvanceGrapher()
win.connect("delete-event", gtk.main_quit)
win.show_all()
gtk.main()