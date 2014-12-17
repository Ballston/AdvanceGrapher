#!/usr/bin/env python

from gi.repository import Gtk as gtk


from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

import numpy as np
from numpy import arange, sin, pi

import pandas as pd
from pandas import DataFrame
import pandas.io.data

import datetime



class AdvanceGrapher(gtk.Window):
    
    def __init__(self):
        gtk.Window.__init__(self,title="AdvanceGrapher")
        self.df=DataFrame
        
        self.set_default_size(800, 800)
        
        self.mainTable=gtk.Table(12,4,True)
        self.add(self.mainTable)
        
        
        self.btnChooseFile=gtk.Button(label="File")
        self.btnChooseFile.connect("clicked",self.btnChooseFile_clicked)
        
        self.btnLoadData=gtk.Button(label="Load")
        self.btnLoadData.connect("clicked",self.btnLoadData_clicked)
        
        self.btnPlotDependentVar=gtk.Button(label="Plot")
        self.btnPlotDependentVar.connect("clicked",self.btnPlotDependentVar_clicked)
        
        
        
        self.entryFileName=gtk.Entry()
        self.entryFileName.set_text("/home/timur/ProjectsLocal/Data/DFAST2015/DFAST2015base.csv")
        
        self.ListOfVars = gtk.ListStore(int, str)
        self.DependentVarCombo = gtk.ComboBox.new_with_model_and_entry(self.ListOfVars)
        self.DependentVarCombo.set_entry_text_column(1)
        
        self.ListOfVars.append([1,'hello'])
        self.ListOfVars.append([2,'world'])
        self.sampleTreeView=gtk.TreeView(self.ListOfVars)
        #self.selector=self.sampleTreeView.get_selection()
        #self.selector.set_mode(gtk.SelectionMode.MULTIPLE)
        #self.sampleTreeview.insert_column('hello',1)
        
        self.fig=Figure(figsize=(4,3), dpi=100)
        self.canvas=FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.vbox=gtk.VBox()
        self.vbox.pack_start(self.canvas, True, True, 0)
        self.vbox.pack_start(self.toolbar, False, False, 0)
        
        self.mainTable.attach(self.btnChooseFile,0,1,0,1)
        self.mainTable.attach(self.entryFileName,2,5,0,1)
        self.mainTable.attach(self.btnLoadData,1,2,0,1)
        
        self.mainTable.attach(gtk.Label("Dependent Var"), 0,1,1,2)
        self.mainTable.attach(self.DependentVarCombo, 1,2,1,2)
        
        self.mainTable.attach(self.btnPlotDependentVar,1,2,2,3)
        
        self.mainTable.attach(self.vbox, 2,6,1,8)
        
        self.mainTable.attach(self.sampleTreeView,1,2,3,8)
        #return None
    
    def btnPlotDependentVar_clicked(self,widget):
        activeIter=self.DependentVarCombo.get_active_iter()
        model=self.DependentVarCombo.get_model()
        Variable=model[activeIter][1]
          
        a=self.fig.add_subplot(111,title=Variable)
        a.clear()
        a=self.fig.add_subplot(111,title=Variable)
        t = self.df[Variable]
        s = self.df[Variable]
        a.plot(self.df.index,self.df[Variable])
        self.canvas.draw()
        
        
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