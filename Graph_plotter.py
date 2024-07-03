import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox as tkMessageBox
from matplotlib import pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import backend_bases, ticker
import numpy as np
from sympy import sec, asec, csc, acsc, cot, acot, solveset, S, diff
from sympy.abc import x
from scipy.stats import binom, norm, uniform
from shapely.geometry import LineString
import math, os, sys

class Design:
    def __init__(self, window):
        # default widgets that will appear upon first opening the window
        self.window = window
        self.window.title("Create new graph")
        self.txt_dim = tk.Label(window, text="Select 2D or 3D:")
        self.txt_dim.config(font=("Gadugi", 12))
        self.txt_dim.place(x=3, y=0)
        self.btn_2d = tk.Button(window, text="2D", width=8, height=1, command=self.chooseFunction)
        self.btn_2d.config(font=("Gadugi", 12))
        self.btn_2d.place(x=3, y=25)
        self.btn_3d = tk.Button(window, text="3D", width=8, height=1, command=self.create3D)
        self.btn_3d.config(font=("Gadugi", 12))
        self.btn_3d.place(x=93, y=25)
        # widgets that will appear depending on the user inputs
        # created here but displayed when appropriate
        ## function selection widgets
        self.txt_fun = tk.Label(window,text="Select function:")
        self.txt_fun.config(font=("Gadugi", 12))
        self.var = tk.IntVar()
        self.rbtn_one = tk.Radiobutton(window, text="Cartesian", variable=self.var, value=1, command=self.enterCartesianDomain)
        self.rbtn_one.config(font=("Gadugi", 12))
        self.rbtn_two = tk.Radiobutton(window, text="Distribution", variable=self.var, value=2, command=self.distribution)
        self.rbtn_two.config(font=("Gadugi", 12))
        self.rbtn_three = tk.Radiobutton(window, text="Parametric", variable=self.var, value=3, command=self.enterDomain)
        self.rbtn_three.config(font=("Gadugi", 12))
        self.rbtn_four = tk.Radiobutton(window, text="Table of values", variable=self.var, value=4, command=self.table)
        self.rbtn_four.config(font=("Gadugi", 12))
        ### enter domain
        self.txt_xdomain = tk.Label(window, text="Enter domain of x:")
        self.txt_xdomain.config(font=("Gadugi", 12))
        self.btn_xdomain = tk.Button(window, text="Enter", width=5, height=1, command=self.cartesianDomain)
        self.btn_xdomain.config(font=("Gadugi", 12))
        #self.txt_lowest = tk.Label(window, text="Lowest:")
        #self.txt_lowest.config(font=("Gadugi", 12))
        #self.ent_lowest = tk.Entry(window, width=3, font="Gadugi", justify="left")
        #self.txt_highest = tk.Label(window, text="Highest:")
        #self.txt_highest.config(font=("Gadugi", 12))
        #self.ent_highest = tk.Entry(window, width=3, font="Gadugi", justify="left")
        ## cartesian widgets
        self.txt_car = tk.Label(window, text="Select equation:")
        self.txt_car.config(font=("Gadugi", 12))
        self.e = tk.StringVar()
        self.e.set("Equation")
        self.opt_car = ["Algebraic fraction", "Circular", "Exponential", "Logarithmic", "Polynomial", "Reciprocal", "Trigonometric"]
        self.om_car = tk.OptionMenu(window, self.e, *self.opt_car)
        self.om_car.config(font=("Gadugi", 12))
        self.btn_enter = tk.Button(window, text="Enter", width=5, height=1, command=self.selectEquation)
        self.btn_enter.config(font=("Gadugi", 11))
        self.txt_eq = tk.Label(window, text="Enter equation:")
        self.txt_eq.config(font=("Gadugi", 12))
        ### polynomial
        self.txt_eqy = tk.Label(window, text="y =")
        self.txt_eqy.config(font=("Gadugi", 13))
        self.txt_eqx = tk.Label(window, text="x   +       x   +       x   +       x   +")
        self.txt_eqx.config(font=("Gadugi", 13))
        self.txt_four = tk.Label(window, text="4")
        self.txt_four.config(font=("Gadugi", 8))
        self.ent_x4 = tk.Entry(window, width=2, font="Gadugi", justify="right")
        self.txt_three = tk.Label(window, text="3")
        self.txt_three.config(font=("Gadugi", 8))
        self.ent_x3 = tk.Entry(window, width=2, font="Gadugi", justify="right")
        self.txt_two = tk.Label(window, text="2")
        self.txt_two.config(font=("Gadugi", 8))
        self.ent_x2 = tk.Entry(window, width=2, font="Gadugi", justify="right")
        self.ent_x1 = tk.Entry(window, width=2, font="Gadugi", justify="right")
        self.ent_x0 = tk.Entry(window, width=2, font="Gadugi", justify="right")
        ### circular
        self.txt_ceq = tk.Label(window, text="(x -       )  +  (y -      )   = ")
        self.txt_ceq.config(font=("Gadugi", 13))
        self.ent_x = tk.Entry(window, width=2, font="Gadugi", justify="center")
        self.txt_twox = tk.Label(window, text="2")
        self.txt_twox.config(font=("Gadugi", 8))
        self.ent_y = tk.Entry(window, width=2, font="Gadugi", justify="center")
        self.txt_twoy = tk.Label(window, text="2")
        self.txt_twoy.config(font=("Gadugi", 8))
        self.ent_r = tk.Entry(window, width=2, font="Gadugi", justify="center")
        ### algebraic fraction
        self.txt_afeqx = tk.Label(window, text="x   +       x   +       x   +       x   +")
        self.txt_afeqx.config(font=("Gadugi", 13))
        self.txt_affour = tk.Label(window, text="4")
        self.txt_affour.config(font=("Gadugi", 8))
        self.ent_afx4 = tk.Entry(window, width=2, font="Gadugi", justify="right")
        self.txt_afthree = tk.Label(window, text="3")
        self.txt_afthree.config(font=("Gadugi", 8))
        self.ent_afx3 = tk.Entry(window, width=2, font="Gadugi", justify="right")
        self.txt_aftwo = tk.Label(window, text="2")
        self.txt_aftwo.config(font=("Gadugi", 8))
        self.ent_afx2 = tk.Entry(window, width=2, font="Gadugi", justify="right")
        self.ent_afx1 = tk.Entry(window, width=2, font="Gadugi", justify="right")
        self.ent_afx0 = tk.Entry(window, width=2, font="Gadugi", justify="right")
        self.line = tk.Label(window, text="_______________________________________________________________")
        ### exponential
        self.txt_exp = tk.Label(window, text="Select form of equation:")
        self.txt_exp.config(font=("Gadugi", 12))
        self.rbtn_five = tk.Radiobutton(window, text="a", variable=self.var, value=5, command=self.ax)
        self.rbtn_five.config(font=("Gadugi", 12))
        self.txt_ax = tk.Label(window, text="x")
        self.txt_ax.config(font=("Gadugi", 8))
        self.rbtn_six = tk.Radiobutton(window, text="x", variable=self.var, value=6, command=self.xa)
        self.rbtn_six.config(font=("Gadugi", 12))
        self.txt_xa = tk.Label(window, text="a")
        self.txt_xa.config(font=("Gadugi", 8))
        self.txt_xax = tk.Label(window, text="x")
        self.txt_xax.config(font=("Gadugi", 13))
        self.txt_plus = tk.Label(window, text="+")
        self.txt_plus.config(font=("Gadugi", 13))
        self.txt_axx = tk.Label(window, text="x")
        self.txt_axx.config(font=("Gadugi", 10))
        self.ent_power = tk.Entry(window, width=1, font="Gadugi", justify="left")
        ### logarithmic
        self.txt_log = tk.Label(window, text="log")
        self.txt_log.config(font=("Gadugi", 13))
        self.txt_obracket = tk.Label(window, text="(")
        self.txt_obracket.config(font=("Gadugi", 13))
        self.txt_cbracket = tk.Label(window, text=")")
        self.txt_cbracket.config(font=("Gadugi", 13))
        ### trigonometric
        self.t = tk.StringVar()
        self.t.set("Trigonometric function")
        self.opt_trig = ("Sin", "Cos", "Tan", "Sec", "Cosec", "Cot")    
        self.om_trig = tk.OptionMenu(window, self.t, *self.opt_trig)
        self.om_trig.config(font=("Gadugi", 12))
        self.trig = ""
        self.txt_entertf = tk.Label(window, text="Select trigonometric function:")
        self.txt_entertf.config(font=("Gadugi", 12))
        self.btn_entertrig = tk.Button(window, text="Enter", width=5, height=1, command=self.selectTrigEquation)
        self.btn_entertrig.config(font=("Gadugi", 11))
        self.txt_sin = tk.Label(window, text="sin")
        self.txt_sin.config(font=("Gadugi", 13))
        self.txt_cos = tk.Label(window, text="cos")
        self.txt_cos.config(font=("Gadugi", 13))
        self.txt_tan = tk.Label(window, text="tan")
        self.txt_tan.config(font=("Gadugi", 13))
        self.txt_sec = tk.Label(window, text="sec")
        self.txt_sec.config(font=("Gadugi", 13))
        self.txt_csc = tk.Label(window, text="csc")
        self.txt_csc.config(font=("Gadugi", 13))
        self.txt_cot = tk.Label(window, text="cot")
        self.txt_cot.config(font=("Gadugi", 13))
        ## distribution widgets
        self.txt_dist = tk.Label(window, text="Select distribution:")
        self.txt_dist.config(font=("Gadugi", 12))
        self.rbtn_seven = tk.Radiobutton(window, text="Binomial", variable=self.var, value=7, command=self.enterBinomial)
        self.rbtn_seven.config(font=("Gadugi", 12))
        self.rbtn_eight = tk.Radiobutton(window, text="Normal", variable=self.var, value=8, command=self.enterNormal)
        self.rbtn_eight.config(font=("Gadugi", 12))
        self.rbtn_nine = tk.Radiobutton(window, text="Uniform", variable=self.var, value=9, command=self.enterUniform)
        self.rbtn_nine.config(font=("Gadugi", 12))
        ### binomial distribution
        self.txt_bdn = tk.Label(window, text="Enter number of trials:")
        self.txt_bdn.config(font=("Gadugi", 12))
        self.txt_bdp = tk.Label(window, text="Enter probability:")
        self.txt_bdp.config(font=("Gadugi", 12))
        ### normal distribution
        self.txt_ndm = tk.Label(window, text="Enter mean:")
        self.txt_ndm.config(font=("Gadugi", 12))
        self.txt_ndv = tk.Label(window,text="Enter variance:")
        self.txt_ndv.config(font=("Gadugi", 12))
        ### uniform distribution
        self.txt_uda = tk.Label(window, text="Enter lower value of x:")
        self.txt_uda.config(font=("Gadugi", 12))
        self.txt_udb = tk.Label(window, text="Enter upper value of x:")
        self.txt_udb.config(font=("Gadugi", 12))
        ## parametric widgets
        self.par = False
        self.pary = False    # for the parametric equations:
        self.pxrec = False   # if x-equation is reciprocal
        self.pxaf = False    # if x-equation is algebraic fraction
        self.pxax = False    # if x-equation is exponential with form a^x
        self.pxxa = False    # if x-equation is exponential with form x^a
        self.pxlog = False   # if x-equation is logarithmic
        self.pxpol = False   # if x-equation is polynomial
        self.pxtrig = False  # if x-equation is trigonometric
        self.pyrec = False   # if y-equation is reciprocal
        self.pyaf = False    # if y-equation is algebraic fraction
        self.pyax = False    # if y-equation is exponential with form a^x
        self.pyxa = False    # if y-equation is exponential with form x^a
        self.pylog = False   # if y-equation is logarithmic
        self.pypol = False   # if y-equation is polynomial
        self.pytrig = False  # if y-equation is trigonometric
        self.txt_eqforx = tk.Label(window, text="Enter equation for x:")
        self.txt_eqforx.config(font=("Gadugi", 12))
        self.txt_eqfory = tk.Label(window, text="Enter equation for y:")
        self.txt_eqfory.config(font=("Gadugi", 12))
        self.btn_enterpary = tk.Button(window, text="Equation of y",width=10, height=1, command=self.createXPlots)
        self.btn_enterpary.config(font=("Gadugi", 12))
        self.txt_enterd = tk.Label(window, text="Enter domain of t:")
        self.txt_enterd.config(font=("Gadugi", 12))
        self.btn_enterd = tk.Button(window, text="Enter", width=5, height=1, command=self.parametric)
        self.btn_enterd.config(font=("Gadugi", 12))
        self.txt_lowest = tk.Label(window, text="Lowest:")
        self.txt_lowest.config(font=("Gadugi", 12))
        self.ent_lowest = tk.Entry(window, width=3, font="Gadugi", justify="left")
        self.txt_highest = tk.Label(window, text="Highest:")
        self.txt_highest.config(font=("Gadugi", 12))
        self.ent_highest = tk.Entry(window, width=3, font="Gadugi", justify="left")
        self.frm_hidex = tk.Frame(window, width=1000, height=160)
        ### polynomial
        self.txt_pareqx = tk.Label(window, text="x =")
        self.txt_pareqx.config(font=("Gadugi", 13))
        self.txt_pareqxt4 = tk.Label(window, text="t")
        self.txt_pareqxt4.config(font=("Gadugi", 13))
        self.txt_pareqxt3 = tk.Label(window, text="t")
        self.txt_pareqxt3.config(font=("Gadugi", 13))
        self.txt_pareqxt2 = tk.Label(window, text="t")
        self.txt_pareqxt2.config(font=("Gadugi", 13))
        self.txt_pareqxt1 = tk.Label(window, text="t")
        self.txt_pareqxt1.config(font=("Gadugi", 13))
        ### algebraic fraction
        self.txt_parafeqxt4 = tk.Label(window, text="t")
        self.txt_parafeqxt4.config(font=("Gadugi", 13))
        self.txt_parafeqxt3 = tk.Label(window, text="t")
        self.txt_parafeqxt3.config(font=("Gadugi", 13))
        self.txt_parafeqxt2 = tk.Label(window, text="t")
        self.txt_parafeqxt2.config(font=("Gadugi", 13))
        self.txt_parafeqxt1 = tk.Label(window, text="t")
        self.txt_parafeqxt1.config(font=("Gadugi", 13))
        ### exponential
        self.ax = False
        self.txt_xat = tk.Label(window, text="t")
        self.txt_xat.config(font=("Gadugi", 13))
        self.txt_axt = tk.Label(window, text="t")
        self.txt_axt.config(font=("Gadugi", 10))
        ## table of values widgets
        self.btn_import = tk.Button(window, text="Import data", width=10, height=1, command=self.importData)
        self.btn_import.config(font=("Gadugi", 12))
        self.txt_xval = tk.Label(window, text="x-values:")
        self.txt_xval.config(font=("Gadugi", 12))
        self.txt_yval = tk.Label(window, text="y-values:")
        self.txt_yval.config(font=("Gadugi", 12))
        self.place = 0
        self.btn_next = tk.Button(window, text="Next point", width=10, height=1, command=self.getValues)
        self.btn_next.config(font=("Gadugi", 12))
        self.X = 0
        self.Y = 0
        self.txt_xpoint = tk.Label(window, text=str(self.X))
        self.txt_xpoint.config(font=("Gadugi", 12))
        self.txt_ypoint = tk.Label(window, text=str(self.Y))
        self.txt_ypoint.config(font=("Gadugi", 12))
        self.count = 1
        # create buttons
        self.btn_createpol = tk.Button(window, text="Create graph", width=10, height=1, command=self.createPolynomial)
        self.btn_createpol.config(font=("Gadugi", 12))
        self.btn_createaf = tk.Button(window, text="Create graph", width=10, height=1, command=self.createAlgebraicFraction)
        self.btn_createaf.config(font=("Gadugi", 12))
        self.btn_createrec = tk.Button(window, text="Create graph", width=10, height=1, command=self.createReciprocal)
        self.btn_createrec.config(font=("Gadugi", 12))
        self.btn_createcir = tk.Button(window, text="Create graph", width=10, height=1, command=self.createCircular)
        self.btn_createcir.config(font=("Gadugi", 12))
        self.btn_createexp = tk.Button(window, text="Create graph", width=10, height=1, command=self.createExponential)
        self.btn_createexp.config(font=("Gadugi", 12))
        self.btn_createlog = tk.Button(window, text="Create graph", width=10, height=1, command=self.createLogarithmic)
        self.btn_createlog.config(font=("Gadugi", 12))
        self.btn_createtrig = tk.Button(window, text="Create graph", width=10, height=1, command=self.createTrigonometric)
        self.btn_createtrig.config(font=("Gadugi", 12))
        self.btn_createpar = tk.Button(window, text="Create graph", width=10, height=1, command=self.createYPlots)
        self.btn_createpar.config(font=("Gadugi", 12))
        self.btn_createbin = tk.Button(window, text="Create graph", width=10, height=1, command=self.createBinomial)
        self.btn_createbin.config(font=("Gadugi", 12))
        self.btn_createnor = tk.Button(window, text="Create graph", width=10, height=1, command=self.createNormal)
        self.btn_createnor.config(font=("Gadugi", 12))
        self.btn_createuni = tk.Button(window, text="Create graph", width=10, height=1, command=self.createUniform)
        self.btn_createuni.config(font=("Gadugi", 12))
        self.btn_createtov = tk.Button(window, text="Create", width=6, height=1, command=self.createScatterGraph)
        self.btn_createtov.config(font=("Gadugi", 12))
        # draw example buttons
        self.btn_exampleaf = tk.Button(window, text="Plot\nexample", width=8, height=2, bg="#f5f5f0", command=self.createExampleAf)
        self.btn_exampleaf.config(font=("Gadugi", 12))
        self.btn_examplecir = tk.Button(window, text="Plot\nexample", width=8, height=2, bg="#f5f5f0", command=self.createExampleCir)
        self.btn_examplecir.config(font=("Gadugi", 12))
        self.btn_exampleex = tk.Button(window, text="Plot\nexample", width=8, height=2, bg="#f5f5f0", command=self.createExampleEx)
        self.btn_exampleex.config(font=("Gadugi", 12))
        self.btn_examplelog = tk.Button(window, text="Plot\nexample", width=8, height=2, bg="#f5f5f0", command=self.createExampleLog)
        self.btn_examplelog.config(font=("Gadugi", 12))
        self.btn_examplepol = tk.Button(window, text="Plot\nexample", width=8, height=2, bg="#f5f5f0", command=self.createExamplePol)
        self.btn_examplepol.config(font=("Gadugi", 12))
        self.btn_examplerec = tk.Button(window, text="Plot\nexample", width=8, height=2, bg="#f5f5f0", command=self.createExampleRec)
        self.btn_examplerec.config(font=("Gadugi", 12))
        self.btn_exampletrig = tk.Button(window, text="Plot\nexample", width=8, height=2, bg="#f5f5f0", command=self.createExampleTrig)
        self.btn_exampletrig.config(font=("Gadugi", 12))
        self.btn_examplepar = tk.Button(window, text="Plot\nexample", width=8, height=2, bg="#f5f5f0", command=self.createExamplePar)
        self.btn_examplepar.config(font=("Gadugi", 12))
        self.btn_examplebin = tk.Button(window, text="Plot\nexample", width=8, height=2, bg="#f5f5f0", command=self.createExampleBin)
        self.btn_examplebin.config(font=("Gadugi", 12))
        self.btn_examplenor = tk.Button(window, text="Plot\nexample", width=8, height=2, bg="#f5f5f0", command=self.createExampleNor)
        self.btn_examplenor.config(font=("Gadugi", 12))
        self.btn_exampleuni = tk.Button(window, text="Plot\nexample", width=8, height=2, bg="#f5f5f0", command=self.createExampleUni)
        self.btn_exampleuni.config(font=("Gadugi", 12))
        
    def create3D(self):
        root3D = tk.Tk()
        root3D.state("zoomed")
        app3D = ThreeDimensional(root3D)
        
    def createExampleAf(self):
        global functions, coefficients
        functions[graph_num] = "Algebraic fraction"
        coefficients[graph_num].extend([0, 0, 0, 1, 0, 0, 0, 0, 2, 5])
        fx = []
        self.curve.algebraicFraction(False, False, fx, 0, 0, 0, 1, 0, 0, 0, 0, 2, 5)
    
    def createExampleCir(self):
        global functions, coefficients
        functions[graph_num] = "Circular"
        coefficients[graph_num].extend([0, 0, 9])
        self.curve.circular(0, 0, 9)
        
    def createExampleEx(self):
        global functions, coefficients
        functions[graph_num] = "a^x"
        coefficients[graph_num].extend([2, 1, 0])
        fx = []
        self.curve.ax(False, False, fx, 2, 1, 0)

    def createExampleLog(self):
        global functions, coefficients
        functions[graph_num] = "Logarithmic"
        coefficients[graph_num].extend([1, 10, 1, 0])
        fx = []
        self.curve.logarithmic(False, False, fx, 1, 10, 1, 0)

    def createExamplePol(self):
        global functions, coefficients
        functions[graph_num] = "Polynomial"
        coefficients[graph_num].extend([0, 0, 1, 2, 1])
        fx = []
        self.curve.polynomial(False, False, fx, 0, 0, 1, 2, 1)

    def createExampleRec(self):
        global functions, coefficients
        functions[graph_num] = "Reciprocal"
        coefficients[graph_num].extend([1, 0, 0, 0, 1, 0])
        fx = []
        self.curve.reciprocal(False, False, fx, 1, 0, 0, 0, 1, 0)

    def createExampleTrig(self):
        global functions, coefficients
        functions[graph_num] = "Sin"
        coefficients[graph_num].extend([1, 2, 0])
        fx = []
        self.curve.sin(False, False, fx, 1, 2, 0)

    def createExamplePar(self):
        global pt_functions, pt_coefficients, qt_functions, qt_coefficients
        pt_functions[graph_num] = "Sin"
        pt_coefficients[graph_num].extend([1, 1, 0])
        fx = []
        points = self.pt.sin(True, False, fx, 1, 1, 0)
        qt_functions[graph_num] = "Cos"
        qt_coefficients[graph_num].extend([1, 1, 0])
        self.qt.cos(True, True, fx, 1, 1, 0)

    def createExampleBin(self):
        global distributions, dist_parameters, graph_num
        distributions[graph_num] = "Binomial"
        dist_parameters[graph_num].extend([20, 0.15])
        dist = Create(0, 0)
        dist.binomial(20, 0.15)

    def createExampleNor(self):
        global distributions, dist_parameters, graph_num
        distributions[graph_num] = "Normal"
        dist_parameters[graph_num].extend([30, 16])
        dist = Create(0, 0)
        dist.normal(30, 16)

    def createExampleUni(self):
        global distributions, dist_parameters, graph_num
        distributions[graph_num] = "Uniform"
        dist_parameters[graph_num].extend([2, 6])
        dist = Create(0, 0)
        dist.uniform(2, 6)

    def chooseFunction(self):
        self.txt_fun.place(x=190, y=0)
        self.rbtn_one.place(x=190, y=20)
        self.rbtn_two.place(x=190, y=40)
        self.rbtn_three.place(x=190, y=60)
        self.rbtn_four.place(x=190, y=80)

    def cartesian(self):
        self.txt_car.place(x=340, y=0)
        self.om_car.place(x=340, y=25)
        self.btn_enter.place(x=342, y=65)
        if self.pary == True:
            self.frm_hidex.place(x=400, y=0)
            self.frm_hidex.lift()
            self.txt_car.place(x=340, y=170)
            self.om_car.place(x=340, y=195)
            self.btn_enter.place(x=342, y=235)                

    def selectEquation(self):
        item = self.e.get()
        if item == "Algebraic fraction":
            self.drawLine()
        elif item == "Circular":
            self.circular()
        elif item == "Exponential":
            self.exponential()
        elif item == "Logarithmic":
            self.logarithmic()
        elif item == "Polynomial":
            self.polynomial()
        elif item == "Reciprocal":
            self.reciprocal()
        elif item == "Trigonometric":
            self.trigonometric()

    def drawLine(self):
        if self.pary == True:
            self.line.place(x=570, y=225)
        else:
            self.line.place(x=570, y=55)
        self.polynomial()
        self.algebraicFraction()
        
    def algebraicFraction(self):
        self.txt_afeqx.place(x=600, y=80)   # writes 'x'
        self.txt_affour.place(x=610, y=77)  # power of 4
        self.ent_afx4.place(x=580, y=82)    # user enters coefficient of x^4
        self.txt_afthree.place(x=680, y=77) # power of 3
        self.ent_afx3.place(x=650, y=82)    # user enters coefficient of x^3
        self.txt_aftwo.place(x=750, y=77)   # power of 2
        self.ent_afx2.place(x=720, y=82)    # user enters coefficient of x^2
        self.ent_afx1.place(x=790, y=82)    # user enters coefficient of x
        self.ent_afx0.place(x=860, y=82)    # user enters constant
        if self.par == True:
            self.pxaf = True
            self.txt_pareqx.place(x=540, y=57)
            self.txt_parafeqxt4.place(x=600, y=82)
            self.txt_parafeqxt3.place(x=670, y=82)
            self.txt_parafeqxt2.place(x=740, y=82)
            self.txt_parafeqxt1.place(x=810, y=82)
            if self.pary == True:
                self.pyaf = True
                self.txt_eqy.place(x=540, y=225)
                self.txt_parafeqxt4.place(x=600, y=250)
                self.txt_parafeqxt3.place(x=670, y=250)
                self.txt_parafeqxt2.place(x=740, y=250)
                self.txt_parafeqxt1.place(x=810, y=250)
                self.txt_afeqx.place(x=600, y=250)
                self.txt_affour.place(x=610, y=245)
                self.ent_afx4.place(x=580, y=250)
                self.txt_afthree.place(x=680, y=245)
                self.ent_afx3.place(x=650, y=250)
                self.txt_aftwo.place(x=750, y=245)
                self.ent_afx2.place(x=720, y=250)
                self.ent_afx1.place(x=790, y=250)
                self.ent_afx0.place(x=860, y=250)
                self.btn_createaf.place(x=540, y=300)
                self.btn_createaf.lift()
        else:
            self.btn_exampleaf.place(x=342, y=105)
            self.btn_exampleaf.lift()
            self.btn_createaf.place(x=540, y=120)
            self.btn_createaf.lift()

    def circular(self):
        self.btn_examplecir.place(x=342, y=105)
        self.txt_eq.place(x=540, y=0)
        self.txt_ceq.place(x=540, y=30)
        self.ent_x.place(x=575, y=32)
        self.txt_twox.place(x=608, y=25)
        self.ent_y.place(x=672, y=32)
        self.txt_twoy.place(x=700, y=25)
        self.ent_r.place(x=742, y=32)
        self.btn_createcir.place(x=540, y=70)
        
    def exponential(self):
        self.txt_exp.place(x=500, y=0)    # "Select form of equation:"
        self.rbtn_five.place(x=500, y=20) # "a"
        self.txt_ax.place(x=532, y=20)    # power of x
        self.rbtn_six.place(x=500, y=40)  # "x"
        self.txt_xa.place(x=532, y=40)    # power of a
        if self.pary == True:
            self.txt_exp.place(x=500, y=170)
            self.rbtn_five.place(x=500, y=190)
            self.txt_ax.place(x=532, y=190)
            self.rbtn_six.place(x=500, y=210)
            self.txt_xa.place(x=532, y=210)
        else:
            if self.par == False:
                self.btn_exampleex.place(x=342, y=105)

    def ax(self):
        self.ax = True
        self.txt_eq.place(x=700, y=0)
        self.ent_x1.place(x=730, y=42)
        self.ent_power.place(x=753, y=33)
        self.txt_axx.place(x=765, y=33)
        self.txt_plus.place(x=780, y=40)
        self.ent_x0.place(x=800, y=42)
        if self.par == True:
            self.pxax = True
            self.txt_eqforx.place(x=700, y=0)
            self.txt_axt.place(x=765, y=33)
            if self.pary == False:
                self.txt_pareqx.place(x=700, y=40)
                self.btn_enterpary.place(x=700, y=80)
            else:
                self.pyax = True
                self.txt_eqfory.place(x=700, y=170)
                self.ent_x1.place(x=730, y=222)
                self.ent_power.place(x=753, y=213)
                self.txt_axt.place(x=765, y=213)
                self.txt_plus.place(x=780, y=220)
                self.ent_x0.place(x=800, y=222)
                self.txt_eqy.place(x=700, y=220)
                self.btn_createexp.place(x=700, y=260)
        else:
            self.txt_eqy.place(x=700, y=40)
            self.btn_createexp.place(x=700, y=80)

    def xa(self):
        self.xa = True
        self.txt_eq.place(x=700, y=0)
        self.ent_x1.place(x=730, y=42)
        self.txt_xax.place(x=750, y=40)
        self.ent_power.place(x=763, y=33)
        self.txt_plus.place(x=780, y=40)
        self.ent_x0.place(x=800, y=42)
        if self.par == True:
            self.pxxa = True
            self.txt_xat.place(x=750, y=40)
            if self.pary == False:
                self.txt_pareqx.place(x=700, y=40)
                self.btn_enterpary.place(x=700, y=80)
            else:
                self.pyxa = True
                self.txt_eqfory.place(x=700, y=170)
                self.txt_eqy.place(x=700, y=220)
                self.ent_x1.place(x=730, y=224)
                self.txt_xat.place(x=750, y=222)
                self.ent_power.place(x=763, y=215)
                self.txt_plus.place(x=780, y=222)
                self.ent_x0.place(x=800, y=224)
                self.btn_createexp.place(x=700, y=260)
        else:
            self.txt_eqy.place(x=700, y=40)
            self.btn_createexp.place(x=700, y=80)
        
    def logarithmic(self):
        self.txt_eq.place(x=540, y=0)
        self.txt_eqy.place(x=540, y=30)
        self.ent_x2.place(x=575, y=32)
        self.txt_log.place(x=595, y=30)
        self.ent_power.place(x=625, y=40)
        self.txt_obracket.place(x=640, y=30)
        self.ent_x1.place(x=645, y=32)
        self.txt_xax.place(x=665, y=30)
        self.txt_cbracket.place(x=677, y=30)
        self.txt_plus.place(x=690, y=30)
        self.ent_x0.place(x=700, y=32)
        if self.par == True:
            self.pxlog = True
            self.txt_xat.place(x=665, y=30)
            self.txt_eqforx.place(x=540, y=0)
            if self.pary == False:
                self.txt_pareqx.place(x=540, y=30)
                self.btn_enterpary.place(x=540, y=70)
            else:
                self.pylog = True
                self.txt_eqfory.place(x=540, y=170)
                self.txt_eqy.place(x=540, y=200)
                self.ent_x2.place(x=575, y=202)
                self.txt_log.place(x=595, y=200)
                self.ent_power.place(x=625, y=210)
                self.txt_obracket.place(x=640, y=200)
                self.ent_x1.place(x=645, y=202)
                self.txt_xat.place(x=665, y=200)
                self.txt_cbracket.place(x=677, y=200)
                self.txt_plus.place(x=690, y=200)
                self.ent_x0.place(x=700, y=202)
                self.btn_createlog.place(x=540, y=240)
        else:
            self.btn_examplelog.place(x=342, y=105)
            self.btn_createlog.place(x=540, y=70)
        
    def polynomial(self):
        self.txt_eq.place(x=540, y=0)     # "Enter equation:"
        self.txt_eqx.place(x=600, y=30)   # string that writes 'x' where needed
        self.txt_four.place(x=610, y=27)  # power of 4
        self.ent_x4.place(x=580, y=32)    # user enters coefficient of x^4
        self.txt_three.place(x=680, y=27) # power of 3
        self.ent_x3.place(x=650, y=32)    # user enters coefficient of x^3
        self.txt_two.place(x=750, y=27)   # power of 2
        self.ent_x2.place(x=720, y=32)    # user enters coefficient of x^2
        self.ent_x1.place(x=790, y=32)    # user enters coefficient of x
        self.ent_x0.place(x=860, y=32)    # user enters constant
        if self.par == True:
            self.pxpol = True
            self.txt_eqforx.place(x=540, y=0)
            self.txt_pareqxt4.place(x=600, y=30)
            self.txt_pareqxt3.place(x=670, y=30)
            self.txt_pareqxt2.place(x=740, y=30)
            self.txt_pareqxt1.place(x=810, y=30)
            if self.pary == False:
                self.btn_enterpary.place(x=540, y=120)
                self.btn_enterpary.lift()
                self.txt_pareqx.place(x=540, y=30)            
            else:
                self.pypol = True
                self.txt_eqfory.place(x=540, y=170)
                self.txt_eqy.place(x=540, y=200)
                self.txt_eqx.place(x=600, y=200)
                self.txt_pareqxt4.place(x=600, y=200)
                self.txt_pareqxt3.place(x=670, y=200)
                self.txt_pareqxt2.place(x=740, y=200)
                self.txt_pareqxt1.place(x=810, y=200)
                self.txt_four.place(x=610, y=195)
                self.ent_x4.place(x=580, y=200)
                self.txt_three.place(x=680, y=195)
                self.ent_x3.place(x=650, y=200)
                self.txt_two.place(x=750, y=195)
                self.ent_x2.place(x=720, y=200)
                self.ent_x1.place(x=790, y=200)
                self.ent_x0.place(x=860, y=200)
                self.btn_createpol.place(x=540, y=300)
        else:
            self.btn_examplepol.place(x=342, y=105)
            self.txt_eqy.place(x=540, y=30)
            self.btn_createpol.place(x=540, y=120)
        
    def reciprocal(self):
        self.txt_eq.place(x=540, y=0)  # "Enter equation:"
        self.ent_x0.place(x=720, y=32) # user enters numerator constant
        self.line.place(x=570, y=55)   # fraction's dividing line
        self.algebraicFraction()       # creates denominator
        if self.par == True:                           # parametric equation
            self.pxrec = True
            self.txt_eqforx.place(x=540, y=0)          # "Enter equation for x:"
            if self.pary == False:
                self.btn_enterpary.place(x=540, y=120) # button to move on to
            else:                                      ## entering y-equation
                self.pyrec = True
                self.txt_eqfory.place(x=540, y=170)    # "Enter equation for y:"
                self.ent_x0.place(x=720, y=200)        # moves the positions of 
                self.line.place(x=570, y=225)          ## the widgets
                self.txt_eqy.place(x=540, y=200)
                self.btn_createrec.place(x=540, y=300)
                self.btn_createrec.lift()
        else:
            self.btn_examplerec.place(x=342, y=105)
            self.btn_examplerec.lift()
            self.txt_eqy.place(x=540, y=57)
            self.btn_createrec.place(x=540, y=120)
            self.btn_createrec.lift()
        
    def trigonometric(self):
        if self.pary == True:
            self.txt_entertf.place(x=500, y=170)
            self.om_trig.place(x=500, y=195)
            self.btn_entertrig.place(x=502, y=235)              
        else:
            self.txt_entertf.place(x=500, y=0)
            self.om_trig.place(x=500, y=25)
            self.btn_entertrig.place(x=502, y=65)
        if self.par == False: self.btn_exampletrig.place(x=342, y=105)
    '''
    def trigonometric(self):
        self.txt_entertf.place(x=500, y=0)    # "Enter trigonometric function:"
        self.om_trig.place(x=500, y=25)       # option menu
        self.btn_entertrig.place(x=502, y=65) # enter button

    def selectTrigEquation(self):              
        self.trig = self.t.get()              # retrieves entry
        if self.trig == "Sin":                # places the text of the 
            self.txt_sin.place(x=785, y=30)   ## trigonometric function
        elif self.trig == "Cos":              ## selected, then creates 
            self.txt_cos.place(x=785, y=30)   ## the equation template
        elif self.trig == "Tan":
            self.txt_tan.place(x=785, y=30)
        elif self.trig == "Sec":
            self.txt_sec.place(x=785, y=30)
        elif self.trig == "Cosec":
            self.txt_csc.place(x=785, y=30)
        elif self.trig == "Cot":
            self.txt_cot.place(x=785, y=30)
        self.placeTrigEquation()
    '''
    
    def selectTrigEquation(self):
        self.trig = self.t.get()
        if self.pary == True:
            self.pytrig = True
            if self.trig == "Sin":
                self.txt_sin.place(x=785, y=200)
            elif self.trig == "Cos":
                self.txt_cos.place(x=785, y=200)
            elif self.trig == "Tan":
                self.txt_tan.place(x=785, y=200)
            elif self.trig == "Sec":
                self.txt_sec.place(x=785, y=200)
            elif self.trig == "Cosec":
                self.txt_csc.place(x=785, y=200)
            elif self.trig == "Cot":
                self.txt_cot.place(x=785, y=200)
        else:
            if self.par == True:
                self.pxtrig = True
            if self.trig == "Sin":
                self.txt_sin.place(x=785, y=30)
            elif self.trig == "Cos":
                self.txt_cos.place(x=785, y=30)
            elif self.trig == "Tan":
                self.txt_tan.place(x=785, y=30)
            elif self.trig == "Sec":
                self.txt_sec.place(x=785, y=30)
            elif self.trig == "Cosec":
                self.txt_csc.place(x=785, y=30)
            elif self.trig == "Cot":
                self.txt_cot.place(x=785, y=30)
        self.placeTrigEquation()
            
    def placeTrigEquation(self):
        self.txt_eq.place(x=730, y=0)
        self.txt_eqy.place(x=730, y=30)
        self.ent_x2.place(x=765, y=32)
        self.txt_obracket.place(x=815, y=30)
        self.ent_x1.place(x=820, y=32)
        self.txt_xax.place(x=840, y=30)
        self.txt_cbracket.place(x=852, y=30)
        self.txt_plus.place(x=865, y=30)
        self.ent_x0.place(x=890, y=32)      
        if self.par == True:
            self.txt_eqforx.place(x=730, y=0)
            self.txt_xat.place(x=840, y=30)
            if self.pary == False:
                self.txt_pareqx.place(x=730, y=30)
                self.btn_enterpary.place(x=732, y=70)
            else:
                self.txt_eqfory.place(x=730, y=170)
                self.txt_eqy.place(x=730, y=200)
                self.ent_x2.place(x=765, y=202)
                self.txt_obracket.place(x=815, y=200)
                self.ent_x1.place(x=820, y=202)
                self.txt_xat.place(x=840, y=200)
                self.txt_cbracket.place(x=852, y=200)
                self.txt_plus.place(x=865, y=200)
                self.ent_x0.place(x=890, y=202)    
                self.btn_createtrig.place(x=732, y=240)
        else:
            self.txt_eqy.place(x=730, y=30)
            self.btn_createtrig.place(x=732, y=70)

    def distribution(self):
        self.txt_dist.place(x=340, y=0)        # "Select distribution:"
        self.rbtn_seven.place(x=340, y=20)     # binomial
        self.rbtn_eight.place(x=340, y=40)     # normal
        self.rbtn_nine.place(x=340, y=60)      # distribution

    def enterBinomial(self):
        self.txt_bdn.place(x=500, y=0)         # "Enter no. of trials:"
        self.ent_x.place(x=660, y=2)           # user enters n
        self.txt_bdp.place(x=500, y=30)        # "Enter probability:"
        self.ent_y.place(x=620, y=32)          # user enters p
        self.btn_createbin.place(x=500, y=65)

    def enterNormal(self):
        self.txt_ndm.place(x=500, y=0)         # "Enter mean:"
        self.ent_x.place(x=590, y=2)           # user enters mu
        self.txt_ndv.place(x=500, y=30)        # "Enter variance:"
        self.ent_y.place(x=610, y=32)          # user enters sigma^2
        self.btn_createnor.place(x=500, y=65)

    def enterUniform(self):
        self.txt_uda.place(x=500, y=0)         # "Enter lower x:"
        self.ent_x.place(x=660, y=2)           # user enters a
        self.txt_udb.place(x=500, y=30)        # "Enter upper x:"
        self.ent_y.place(x=662, y=32)          # user enters b
        self.btn_createuni.place(x=500, y=65)

    def parametric(self):
        global lower_p, upper_p, graph_num
        try:
            start = float(self.eOrPi(self.ent_lowest.get()))
            stop = float(self.eOrPi(self.ent_highest.get()))
            if start >= stop:
                raise ArithmeticError
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        except ArithmeticError:
            tkMessageBox.showerror("Invalid domain", "Start value must be less than end value.") 
        else:
            if self.ent_lowest.get() == "":
                start = -5
            if self.ent_highest.get() == "":
                stop = 5
            self.pt = Create(start, stop)
            start_pt.append(start)
            stop_pt.append(stop)
            self.qt = Create(start, stop)
            start_qt.append(start)
            stop_qt.append(stop)
            lower_p.append(start)
            upper_p.append(stop)
            self.par = True
            self.opt_car.remove("Circular")
            self.om_car = tk.OptionMenu(self.window, self.e, *self.opt_car)
            self.om_car.config(font=("Gadugi", 12))
            self.btn_examplepar.place(x=190, y=240)
            self.cartesian()

    def enterCartesianDomain(self):
        self.txt_xdomain.place(x=190, y=110)
        self.txt_lowest.place(x=190, y=140)
        self.ent_lowest.place(x=255, y=140)
        self.txt_highest.place(x=190, y=170)
        self.ent_highest.place(x=255, y=170)
        self.btn_xdomain.place(x=190, y=200)

    def cartesianDomain(self):
        global lower_c, upper_c, start_fx, stop_fx
        try:
            start = float(self.eOrPi(self.ent_lowest.get()))
            stop = float(self.eOrPi(self.ent_highest.get()))
            if start >= stop:
                raise ArithmeticError
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        except ArithmeticError:
            tkMessageBox.showerror("Invalid domain", "Start value must be less than end value.") 
        else:
            if self.ent_lowest.get() == "":
                start = -5
            if self.ent_highest.get() == "":
                stop = 5
            lower_c.append(start)
            upper_c.append(stop)
            self.curve = Create(start, stop)
            start_fx.append(start)
            stop_fx.append(stop)
            self.cartesian()
            
    def enterDomain(self):
        self.txt_enterd.place(x=190, y=110)
        self.txt_lowest.place(x=190, y=140)
        self.ent_lowest.place(x=255, y=140)
        self.txt_highest.place(x=190, y=170)
        self.ent_highest.place(x=255, y=170)
        self.btn_enterd.place(x=190, y=200)

    def table(self):
        self.btn_import.place(x=200, y=120)
        self.txt_xval.place(x=342, y=20)             # "Enter x-values:"
        self.txt_yval.place(x=437, y=20)             # "Enter y-values:"
        self.ent_x.place(x=340, y=50+self.place)     # user enters one x-value
        self.ent_y.place(x=435, y=50+self.place)     # user enters one y-value
        self.btn_next.place(x=510, y=45+self.place)

    def importData(self):
        global scatterx, scattery, scatter_num
        filepath = askopenfilename(filetypes=[("CSV files", "*.csv"),])
        if not filepath:                                                                    # so that the plot is only made
            return                                                                          # if the user provides the data
        else:
            try:
                file = open(filepath, "r")                                                  # opens csv file in read mode
                data = file.read()
                values = data.split("\n")                                                   # splits data by cell
                values.pop()                                                                # gets rid of empty cells 
                for i in range(1, len(values)):
                    record = values[i].split(",")                                           # splits data by comma
                    scatterx[scatter_num].append(float(record[0]))                          # appends x-coordinates
                    scattery[scatter_num].append(float(record[1]))                          # appends y-coordinates
            except ValueError:
                tkMessageBox.showerror("Invalid input", "Check format of table.")
            else:  
                self.createScatterGraph()                                                   # plot is created as normal

    def getValues(self):
        try:
            x = float(self.eOrPi(self.ent_x.get()))
            y = float(self.eOrPi(self.ent_y.get()))
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            if self.ent_x.get() == "":                            # if nothing is input,
                x = 0.0                                           ## the value will be
            if self.ent_y.get() == "":                            ## be whatever the 
                y = 0.0                                           ## user enters
            scatterx[scatter_num].append(x)                       # values added to their  
            scattery[scatter_num].append(y)                       ## appropriate arrays
            if self.count >= 3:
                self.btn_createtov.place(x=510, y=30+self.place)  # displays 'Create'
            self.displayValues()                                  ## button
            self.table()

    def displayValues(self):
        self.ent_x.delete(0, "end")
        self.ent_y.delete(0, "end")
        for i in range(len(scatterx[scatter_num])):                                      # displays the inputs
            txt = format(scatterx[scatter_num][i], ".2f") + "    "
            labelx = tk.Label(self.window, text=txt)  ## in their
            labelx.config(font=("Gadugi", 12))                                           ## appropriate places
            labelx.place(x=340, y=50+self.place)                
        for i in range(len(scattery[scatter_num])):
            txt = format(scattery[scatter_num][i], ".2f") + "    "
            labely = tk.Label(self.window, text=txt)
            labely.config(font=("Gadugi", 12))
            labely.place(x=435, y=50+self.place)
        self.place = self.place + 30                                                     # increments place
        self.count = self.count + 1                                                      # increments count
        
    def createAlgebraicFraction(self):
        try:
            a = float(self.eOrPi(self.ent_x4.get()))
            b = float(self.eOrPi(self.ent_x3.get()))
            c = float(self.eOrPi(self.ent_x2.get()))
            d = float(self.eOrPi(self.ent_x1.get()))
            e = float(self.eOrPi(self.ent_x0.get()))
            f = float(self.eOrPi(self.ent_afx4.get()))
            g = float(self.eOrPi(self.ent_afx3.get()))
            h = float(self.eOrPi(self.ent_afx2.get()))
            i = float(self.eOrPi(self.ent_afx1.get()))
            j = float(self.eOrPi(self.ent_afx0.get()))
            if f == g == h == i == j == 0:
                raise ZeroDivisionError
        except ZeroDivisionError:
            tkMessageBox.showerror("Invalid input", "Denominator cannot equal 0.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            self.ent_x4.delete(0, "end")
            self.ent_x3.delete(0, "end")
            self.ent_x2.delete(0, "end")
            self.ent_x1.delete(0, "end")
            self.ent_x0.delete(0, "end")
            self.ent_afx4.delete(0, "end")
            self.ent_afx3.delete(0, "end")
            self.ent_afx2.delete(0, "end")
            self.ent_afx1.delete(0, "end")
            self.ent_afx0.delete(0, "end")
            fx = []
            self.addFunctionDetails("Algebraic fraction", a, b, c, d, e, f, g, h, i, j)
            if self.pyaf == True:
                self.qt.algebraicFraction(self.par, self.pary, self.points, a, b, c, d, e, f, g, h, i, j)
            elif self.pxaf == True:
                self.points = self.pt.algebraicFraction(self.par, self.pary, fx, a, b, c, d, e, f, g, h, i, j) 
            else:
                self.curve.algebraicFraction(self.par, self.pary, fx, a, b, c, d, e, f, g, h, i, j)
            if self.par == True:
                self.pary = True
                self.cartesian()

    def createCircular(self):
        try:
            a = float(self.eOrPi(self.ent_x.get()))
            b = float(self.eOrPi(self.ent_y.get()))
            c = float(self.eOrPi(self.ent_r.get()))
            if c <= 0:
                raise ArithmeticError
        except ArithmeticError:
            tkMessageBox.showerror("Invalid radius", "Radius cannot be less than or equal to 0.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            self.addFunctionDetails("Circular", a, b, c)
            self.curve.circular(a, b, c)

    def createExponential(self):
        try:
            a = float(self.eOrPi(self.ent_x1.get()))
            b = float(self.eOrPi(self.ent_power.get()))
            c = float(self.eOrPi(self.ent_x0.get()))
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            self.ent_x1.delete(0, "end")
            self.ent_power.delete(0, "end")
            self.ent_x0.delete(0, "end")
            fx = []
            if self.ax == True:
                self.addFunctionDetails("a^x", a, b, c)
                if self.pyax == True:
                    self.qt.ax(self.par, self.pary, self.points, a, b, c)
                elif self.pxax == True:
                    self.points = self.pt.ax(self.par, self.pary, fx, a, b, c)
                else:
                    self.curve.ax(self.par, self.pary, fx, a, b, c)
            else:
                self.addFunctionDetails("x^a", a, b, c)
                if self.pyxa == True:
                    self.qt.xa(self.par, self.pary, self.points, a, b, c)
                elif self.pxxa == True:
                    self.points = self.pt.xa(self.par, self.pary, fx, a, b, c)
                else:
                    self.curve.xa(self.par, self.pary, fx, a, b, c)
            if self.par == True:
                self.pary = True
                self.cartesian()

    def createLogarithmic(self):
        try:
            a = float(self.eOrPi(self.ent_x2.get()))
            b = float(self.eOrPi(self.ent_power.get()))
            c = float(self.eOrPi(self.ent_x1.get()))
            d = float(self.eOrPi(self.ent_x0.get()))
            if b <= 1 or c <= 0:
                raise ArithmeticError
        except ArithmeticError:
            tkMessageBox.showerror("Invalid base/argument", "Base cannot be less than 2.\nArgument cannot be less than 1.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            self.ent_x2.delete(0, "end")
            self.ent_power.delete(0, "end")
            self.ent_x1.delete(0, "end")
            self.ent_x0.delete(0, "end")
            fx = []
            self.addFunctionDetails("Logarithmic", a, b, c, d)
            if self.pylog == True:
                self.qt.logarithmic(self.par, self.pary, self.points, a, b, c, d)
            elif self.pxlog == True:
                self.points = self.pt.logarithmic(self.par, self.pary, fx, a, b, c, d) 
            else:
                self.curve.logarithmic(self.par, self.pary, fx, a, b, c, d)
            if self.par == True:
                self.pary = True
                self.cartesian()

    def createPolynomial(self):
        try:
            a = float(self.eOrPi(self.ent_x4.get()))
            b = float(self.eOrPi(self.ent_x3.get()))
            c = float(self.eOrPi(self.ent_x2.get()))
            d = float(self.eOrPi(self.ent_x1.get()))
            e = float(self.eOrPi(self.ent_x0.get()))
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            self.ent_x4.delete(0, "end")
            self.ent_x3.delete(0, "end")
            self.ent_x2.delete(0, "end")
            self.ent_x1.delete(0, "end")
            self.ent_x0.delete(0, "end")
            fx = []
            self.addFunctionDetails("Polynomial", a, b, c, d, e)
            if self.pypol == True:
                self.qt.polynomial(self.par, self.pary, self.points, a, b, c, d, e)
            elif self.pxpol == True:
                self.points = self.pt.polynomial(self.par, self.pary, fx, a, b, c, d, e)
            else:
                self.curve.polynomial(self.par, self.pary, fx, a, b, c, d, e)

            if self.par == True:
                self.pary = True
                self.cartesian()

    def createReciprocal(self):
        try:
            a = float(self.eOrPi(self.ent_x0.get()))
            b = float(self.eOrPi(self.ent_afx4.get()))
            c = float(self.eOrPi(self.ent_afx3.get()))
            d = float(self.eOrPi(self.ent_afx2.get()))
            e = float(self.eOrPi(self.ent_afx1.get()))
            f = float(self.eOrPi(self.ent_afx0.get()))
            if b == c == d == e == f == 0:
                raise ZeroDivisionError
        except ZeroDivisionError:
            tkMessageBox.showerror("Invalid input", "Denominator cannot equal 0.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            self.ent_x0.delete(0, "end")
            self.ent_afx4.delete(0, "end")
            self.ent_afx3.delete(0, "end")
            self.ent_afx2.delete(0, "end")
            self.ent_afx1.delete(0, "end")
            self.ent_afx0.delete(0, "end")
            fx = []
            self.addFunctionDetails("Reciprocal", a, b, c, d, e, f)
            if self.pyrec == True:
                self.qt.reciprocal(self.par, self.pary, self.points, a, b, c, d, e, f)
            elif self.pxrec == True:
                self.points = self.pt.reciprocal(self.par, self.pary, fx, a, b, c, d, e, f) 
            else:
                self.curve.reciprocal(self.par, self.pary, fx, a, b, c, d, e, f)
            if self.par == True:
                self.pary = True
                self.cartesian()

    def createTrigonometric(self):
        try:
            a = float(self.eOrPi(self.ent_x2.get()))
            b = float(self.eOrPi(self.ent_x1.get()))
            c = float(self.eOrPi(self.ent_x0.get()))
        except TypeError:
            tkMessageBox.showerror("Error", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Error", "Only real values, e and π/p can be entered.")
        else:
            self.ent_x2.delete(0, "end")
            self.ent_x1.delete(0, "end")
            self.ent_x0.delete(0, "end")
            fx = []
            if self.trig == "Sin":
                self.addFunctionDetails("Sin", a, b, c)
                if self.pytrig == True:
                    self.qt.sin(self.par, self.pary, self.points, a, b, c)
                elif self.pxtrig == True:
                    self.points = self.pt.sin(self.par, self.pary, fx, a, b, c)
                else:
                    self.curve.sin(self.par, self.pary, fx, a, b, c)
            elif self.trig == "Cos":
                self.addFunctionDetails("Cos", a, b, c)
                if self.pytrig == True:
                    self.qt.cos(self.par, self.pary, self.points, a, b, c)
                elif self.pxtrig == True:
                    self.points = self.pt.cos(self.par, self.pary, fx, a, b, c)
                else:
                    self.curve.cos(self.par, self.pary, fx, a, b, c)
            elif self.trig == "Tan":
                self.addFunctionDetails("Tan", a, b, c)
                if self.pytrig == True:
                    self.qt.tan(self.par, self.pary, self.points, a, b, c)
                elif self.pxtrig == True:
                    self.points = self.pt.tan(self.par, self.pary, fx, a, b, c)
                else:
                    self.curve.tan(self.par, self.pary, fx, a, b, c)
            elif self.trig == "Sec":
                self.addFunctionDetails("Sec", a, b, c)
                if self.pytrig == True:
                    self.qt.sec(self.par, self.pary, self.points, a, b, c)
                elif self.pxtrig == True:
                    self.points = self.pt.sec(self.par, self.pary, fx, a, b, c)
                else:
                    self.curve.sec(self.par, self.pary, fx, a, b, c)
            elif self.trig == "Cosec":
                self.addFunctionDetails("Cosec", a, b, c)
                if self.pytrig == True:
                    self.qt.cosec(self.par, self.pary, self.points, a, b, c)
                elif self.pxtrig == True:
                    self.points = self.pt.cosec(self.par, self.pary, fx, a, b, c)
                else:
                    self.curve.cosec(self.par, self.pary, fx, a, b, c)
            elif self.trig == "Cot":
                self.addFunctionDetails("Cot", a, b, c)
                if self.pytrig == True:
                    self.qt.cot(self.par, self.pary, self.points, a, b, c)
                elif self.pxtrig == True:
                    self.points = self.pt.cot(self.par, self.pary, fx, a, b, c)
                else:
                    self.curve.cot(self.par, self.pary, fx, a, b, c)
            if self.par == True:
                self.pary = True
                self.cartesian()

    def addFunctionDetails(self, f, *args):
        global qt_coefficients, pt_coefficients, qt_functions, pt_functions, functions
        if self.pary == True:
            qt_functions[graph_num] = f
        elif self.par == True:
            pt_functions[graph_num] = f
        else:
            functions[graph_num] = f
          
        for argument in args:
            if self.pary == True:
                qt_coefficients[graph_num].append(argument)
            elif self.par == True:
                pt_coefficients[graph_num].append(argument)
            else:
                coefficients[graph_num].append(argument)
            
    def eOrPi(self, value):
        if value == "": return 1
        elif value == "-" : return -1
        elif value == "e": return math.e
        elif value == "-e": return -math.e
        elif value == "p" or value == "π": return math.pi
        elif value == "-p" or value == "-π": return -math.pi
        else:
            letter_pos = 0
            # checks to see if a multiple of e has been entered
            for digit in value:
                if digit == "e":
                    # separates digits before e from the letter
                    new_value = value[0:letter_pos]
                    try:
                        # attempts multiplication of separated digits with e
                        new_value = float(new_value) * math.e
                    except TypeError:
                        # raised if digits before e are not of type float
                        return TypeError
                    else:
                        # raised if there are characters after the e
                        if letter_pos < (len(value)-1):
                            return ValueError
                        else:
                            return new_value
                else:
                    letter_pos = letter_pos + 1

            # same process for p and π
            letter_pos = 0
            for digit in value:
                if digit == "p" or digit == "π":
                    new_value = value[0:letter_pos]
                    try:
                        new_value = float(new_value) * math.pi
                    except TypeError:
                        return TypeError
                    else:
                        if letter_pos < (len(value)-1):
                            return ValueError
                        else:
                            return new_value
                else:
                    letter_pos = letter_pos + 1
            # if nothing else applies, value should be a float other than 1 or -1
            return value

    def createBinomial(self):
        try:
            a = int(self.eOrPi(self.ent_x.get()))
            b = float(self.eOrPi(self.ent_y.get()))
            if a <= 0 or b <= 0:
                raise ArithmeticError
        except ArithmeticError:
            tkMessageBox.showerror("Invalid input", "Number of trials/probability cannot be less than 0.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            self.addDistributionDetails("Binomial", a, b)
            dist = Create(0, 0)
            dist.binomial(a, b)
            
    def createNormal(self):
        try:
            a = float(self.eOrPi(self.ent_x.get()))
            b = float(self.eOrPi(self.ent_y.get()))
            if b <= 0:
                raise ArithmeticError
            else:
                b = math.sqrt(b)
        except ArithmeticError:
            tkMessageBox.showerror("Invalid input", "Variance cannot be 0 or less.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            self.addDistributionDetails("Normal", a, b)
            dist = Create(0, 0)
            dist.normal(a, b)
        
    def createUniform(self):
        try:
            a = float(self.eOrPi(self.ent_x.get()))
            b = float(self.eOrPi(self.ent_y.get()))
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            self.addDistributionDetails("Uniform", a, b)
            dist = Create(0, 0)
            dist.uniform(a, b)

    def addDistributionDetails(self, fx, a, b):
        distributions[graph_num] = fx
        dist_parameters[graph_num].extend([a, b])
        
    def createXPlots(self):
        if self.pxrec == True:
            self.createReciprocal()
        elif self.pxaf == True:
            self.createAlgebraicFraction()
        elif self.pxax == True or self.pxxa == True:
            self.createExponential()
        elif self.pxlog == True:
            self.createLogarithmic()
        elif self.pxpol == True:
            self.createPolynomial()
        elif self.pxtrig == True:
            self.createTrigonometric()
            
    def createYPlots(self):
        if self.pyrec == True:
            self.createReciprocal()
        elif self.pyaf == True:
            self.createAlgebraicFraction()
        elif self.pyax == True or self.pyxa == True:
            self.createExponential()
        elif self.pylog == True:
            self.createLogarithmic()
        elif self.pypol == True:
            self.createPolynomial()
        elif self.pytrig == True:
            self.createTrigonometric()

    def createScatterGraph(self):
        global scatterx, scattery, scatter_num
        graph = Create(0, 0)
        graph.tableOfValues(scatterx[scatter_num], scattery[scatter_num])

class Create:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
        self.x = np.linspace(start, stop, 9000)
        self.y = np.linspace(start, stop, 9000)
        self.fx = []
        self.fy = [] 
        
    def algebraicFraction(self, parametric, parametricy, fx, a, b, c, d, e, f, g, h, i, j):
        if parametric == False or parametric == True and parametricy == False:
            for val in range(len(self.x)):
                point = (a*(self.x[val]**4) + b*(self.x[val]**3) + c*(self.x[val]**2) + d*(self.x[val]) + e)/(f*(self.x[val]**4)+ g*(self.x[val]**3) + h*(self.x[val]**2) + i*(self.x[val]) + j)
                if point > 1000 or point < -1000:
                        point = np.inf
                if parametric == False:
                    self.fx.append(point)
                else:
                    fx.append(point)
            if parametric == False:
                self.plotCartesian()
            else:
                return fx
        else:
            for val in range(len(self.y)):
                point = (a*(self.y[val]**4) + b*(self.y[val]**3) + c*(self.y[val]**2) + d*(self.y[val]) + e)/(f*(self.y[val]**4)+ g*(self.y[val]**3) + h*(self.y[val]**2) + i*(self.y[val]) + j)
                if point > 1000 or point < -1000:
                    point = np.inf
                self.fy.append(point)       
            self.plotParametric(fx)

    def circular(self, a, b, c):
        global canvas, graph_num
        graph_num = graph_num + 1
        self.createWindow()
        self.x = np.linspace(-10, 10, 100)
        self.y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(self.x, self.y)
        Z = (X - a)**2 + (Y - b)**2 - c
        diagram.contour(X, Y, Z, 0)
        canvas.draw()
        diagram.axvline(color="black", linewidth=1.25)
        diagram.axhline(color="black", linewidth=1.25)
        root.mainloop()
               
    def ax(self, parametric, parametricy, fx, a, b, c):
        if parametric == False or parametric == True and parametricy == False:
            for i in range(len(self.x)):
                point = a**(b*self.x[i]) + c
                if parametric == False:
                    self.fx.append(point)
                else:
                    fx.append(point)
            if parametric == False:
                self.plotCartesian()
            else:
                return fx
        else:
            for i in range(len(self.y)):
                self.fy.append(a**(b*self.y[i]) + c)
            self.plotParametric(fx)
    
    def xa(self, parametric, parametricy, fx, a, b, c):
        if parametric == False or parametric == True and parametricy == False:
            for i in range(len(self.x)):
                if a*(self.x[i]**b) == 0:
                    point = c
                else:
                    point = a*(self.x[i]**b) + c
                if parametric == False:
                    self.fx.append(point)
                else:
                    fx.append(point)
            if parametric == False:
                self.plotCartesian()
            else:
                return fx
        else:
            for i in range(len(self.y)):
                if a*(self.y[i]**b) == 0:
                    point = c
                else:
                    point = a*(self.y[i]**b) + c
                self.fy.append(point)
            self.plotParametric(fx)
    
    def logarithmic(self, parametric, parametricy, fx, a, b, c, d):
        self.x = np.linspace(0, self.stop, 9000)
        if parametric == False or parametric == True and parametricy == False:
            for i in range(len(self.x)):
                z = c*self.x[i]
                if self.x[i] == 0:
                    point = np.inf
                else:
                    point = a*(math.log(z, b)) + d
                if parametric == False:
                    self.fx.append(point)
                else:
                    fx.append(point)
            if parametric == False:
                self.plotCartesian()
            else:
                return fx
        else:
            self.y = np.linspace(0, self.stop, 9000)
            for i in range(len(self.y)):
                z = c*self.y[i]
                if self.y[i] == 0:
                    self.fy.append(np.inf)
                else:
                    self.fy.append(a*(math.log(z, b)) + d)
            self.plotParametric(fx)
        
    def polynomial(self, parametric, parametricy, fx, a, b, c, d, e):
        if parametric == False or parametric == True and parametricy == False:
            for i in range(len(self.x)):
                point = a*(self.x[i]**4) + b*(self.x[i]**3) + c*(self.x[i]**2)+ d*(self.x[i]) + e
                if parametric == False:
                    self.fx.append(point)
                else:
                    fx.append(point)
            if parametric == False:
                self.plotCartesian()
            else:
                return fx
        else:
            for i in range(len(self.y)):
                self.fy.append(a*(self.y[i]**4) + b*(self.y[i]**3) + c*(self.y[i]**2)+ d*(self.y[i]) + e)
            self.plotParametric(fx)

    def reciprocal(self, parametric, parametricy, fx, a, b, c, d, e, f):
        if parametric == False or parametric == True and parametricy == False:
            for i in range(len(self.x)):
                point = a/(b*(self.x[i]**4) + c*(self.x[i]**3) + d*(self.x[i]**2)+ e*(self.x[i]) + f)
                if point > 100 or point < -100:
                    point = np.inf
                if parametric == False:
                    self.fx.append(point)
                else:
                    fx.append(point)
            if parametric == False:
                    self.plotCartesian()
            else:
                return fx
        else:
            for i in range(len(self.y)):
                point = a/(b*(self.y[i]**4) + c*(self.y[i]**3) + d*(self.y[i]**2)+ e*(self.y[i]) + f)
                if point > 100 or point < -100:
                    point = np.inf
                self.fy.append(point)
            self.plotParametric(fx)

    def sin(self, parametric, parametricy, fx, a, b, c):
        if parametric == False or parametric == True and parametricy == False:
            for i in range(len(self.x)):
                point = a*math.sin(b*self.x[i])+c
                if parametric == False:
                    self.fx.append(point)
                else:
                    fx.append(point)
            if parametric == False:
                self.plotCartesian()
            else:
                return fx
        else:
            for i in range(len(self.y)):
                self.fy.append(a*math.sin(b*self.y[i])+c)
            self.plotParametric(fx)

    def cos(self, parametric, parametricy, fx, a, b, c):
        if parametric == False or parametric == True and parametricy == False:
            for i in range(len(self.x)):
                point = a*math.cos(b*self.x[i])+c
                if parametric == False:
                    self.fx.append(point)
                else:
                    fx.append(point)
            if parametric == False:
                self.plotCartesian()
            else:
                return fx
        else:
            for i in range(len(self.y)):
                self.fy.append(a*math.cos(b*self.y[i])+c)
            self.plotParametric(fx)

    def tan(self, parametric, parametricy, fx, a, b, c):
        if parametric == False or parametric == True and parametricy == False:
            for i in range(len(self.x)):
                point = a*math.tan(b*self.x[i])+c
                if point > 1000 or point < -1000:
                    point = np.inf
                if parametric == False:
                    self.fx.append(point)
                else:
                    fx.append(point)
            if parametric == False:
                self.plotCartesian()
            else:
                return fx
        else:
            for i in range(len(self.y)):
                point = a*math.tan(b*self.y[i])+c
                if point > 1000 or point < -1000:
                    point = np.inf
                self.fy.append(point)
            self.plotParametric(fx)

    def sec(self, parametric, parametricy, fx, a, b, c):
        if parametric == False or parametric == True and parametricy == False:
            for i in range(len(self.x)):
                point = a*sec(b*self.x[i])+c
                if point > 1000 or point < -1000:
                    point = np.inf
                if parametric == False:
                    self.fx.append(point)
                else:
                    fx.append(point)
            if parametric == False:
                self.plotCartesian()
            else:
                return fx
        else:
            for i in range(len(self.y)):
                point = a*sec(b*self.y[i])+c
                if point > 1000 or point < -1000:
                    point = np.inf
                self.fy.append(point)
            self.plotParametric(fx)
    
    def cosec(self, parametric, parametricy, fx, a, b, c):
        if parametric == False or parametric == True and parametricy == False:
            for i in range(len(self.x)):
                point = a*csc(b*self.x[i])+c
                if point > 1000 or point < -1000:
                    point = np.inf
                if parametric == False:
                    self.fx.append(point)
                else:
                    fx.append(point)
            if parametric == False:
                self.plotCartesian()
            else:
                return fx
        else:
            for i in range(len(self.y)):
                point = a*csc(b*self.y[i])+c
                if point > 1000 or point < -1000:
                    point = np.inf
                self.fy.append(point)
            self.plotParametric(fx)

    def cot(self, parametric, parametricy, fx, a, b, c):
        if parametric == False or parametric == True and parametricy == False:
            for i in range(len(self.x)):
                try:
                    point = float(a*cot(b*self.x[i])+c)
                except:
                    point = np.inf
                else:
                    if point > 1000 or point < -1000:
                        point = np.inf
                if parametric == False:
                    self.fx.append(point)
                else:
                    fx.append(point)
            if parametric == False:
                self.plotCartesian()
            else:
                return fx
        else:
            for i in range(len(self.y)):
                try:
                    point = float(a*cot(b*self.y[i])+c)
                except:
                    point = np.inf
                else:
                    if point > 1000 or point < -1000:
                       point = np.inf
                self.fy.append(point)
            self.plotParametric(fx)

    def createWindow(self):
        global is_window_made, root, app, canvas, toolbar, graph_num
        if is_window_made == False:
            root = tk.Tk()
            root.state("zoomed")
            app2D = Interpret(root)
            canvas = FigureCanvasTkAgg(figure, master=root)
            canvas.get_tk_widget().place(x=560, y=45)
            toolbar = NavigationToolbar2Tk(canvas, root)
            toolbar.place(x=1113, y=0)
            frame = tk.Frame(root, width=520, height=265, background="white")
            frame.place(x=20, y=430)
            is_window_made = True
        self.writeEquation()
        self.drawEquationButtons()

    def changeToInt(self, num):
        if num == 0.0:
            num = 0
        elif num == int(num):
            num = int(num)
        else:
            num = round(num, 2)
        return num

    def writeEquation(self):
        global functions, distributions, pt_functions, qt_functions, graph_num
        if functions[graph_num-1] != "":
            self.writeCartesian()
        elif distributions[graph_num-1] != "":
            self.writeDistribution()
        elif pt_functions[graph_num-1] != "":
            self.writeParametric()
        else:
            self.writeTableOfValues()

    def writeCartesian(self):
        global coefficients, functions, graph_num
        fx = functions[graph_num-1]
        if fx == "Algebraic fraction": e = self.writeAlgebraicFraction("fx")
        elif fx == "Circular": e = self.writeCircular()
        elif fx == "a^x": e = self.writeAx("fx")
        elif fx == "x^a": e = self.writeXa("fx")
        elif fx == "Logarithmic": e = self.writeLogarithmic("fx")
        elif fx == "Polynomial": e = self.writePolynomial("fx")
        elif fx == "Reciprocal": e = self.writeReciprocal("fx")
        elif fx == "Sin": e = self.writeTrigonometric("fx", "sin")
        elif fx == "Cos": e = self.writeTrigonometric("fx", "cos")
        elif fx == "Tan": e = self.writeTrigonometric("fx", "tan")
        elif fx == "Sec": e = self.writeTrigonometric("fx", "sec")
        elif fx == "Cosec": e = self.writeTrigonometric("fx", "csc")
        elif fx == "Cot": e = self.writeTrigonometric("fx", "cot")
        if type(e) == str:
            txt = "y = " + e
            txt_equation = tk.Label(root, text=txt, bg="white")
            txt_equation.config(font=("Gadugi", 12))
            if graph_num == 1: txt_equation.place(x=70, y=438)
            if graph_num == 2: txt_equation.place(x=70, y=488)
            if graph_num == 3: txt_equation.place(x=70, y=538)
            if graph_num == 4: txt_equation.place(x=70, y=588)
            if graph_num == 5: txt_equation.place(x=70, y=638)
    
    def writeDistribution(self):
        a = str(self.changeToInt(dist_parameters[graph_num-1][0]))
        if distributions[user_graph] == "Binomial" or distributions[graph_num-1] == "Uniform":
            b = str(self.changeToInt(dist_parameters[graph_num-1][1]))
            txt = a + ", " + b
            l = "B" if distributions[graph_num-1] == "Binomial" else "U"
        elif distributions[user_graph] == "Normal":
            b = str(self.changeToInt(dist_parameters[graph_num-1][1]**2))
            txt = a + ", " + b
            l = "N"
        full_txt = "X ~ " + l + "(" + txt + ")"
        txt_equation = tk.Label(root, text=full_txt, bg="white")
        txt_equation.config(font=("Gadugi", 12))
        if graph_num == 1: txt_equation.place(x=70, y=438)
        if graph_num == 2: txt_equation.place(x=70, y=488)
        if graph_num == 3: txt_equation.place(x=70, y=538)
        if graph_num == 4: txt_equation.place(x=70, y=588)
        if graph_num == 5: txt_equation.place(x=70, y=638)

    def writeParametric(self):
        equations = []
        f = "pt"
        fx = pt_functions[graph_num-1]
        for i in range(2):
            if fx == "Algebraic fraction": e = self.writeAlgebraicFraction(f)
            elif fx == "a^x": e = self.writeAx(f)
            elif fx == "x^a": e = self.writeXa(f)
            elif fx == "Logarithmic": e = self.writeLogarithmic(f)
            elif fx == "Polynomial": e = self.writePolynomial(f)
            elif fx == "Reciprocal": e = self.writeReciprocal(f)
            elif fx == "Sin": e = self.writeTrigonometric(f, "sin")
            elif fx == "Cos": e = self.writeTrigonometric(f, "cos")
            elif fx == "Tan": e = self.writeTrigonometric(f, "tan")
            elif fx == "Sec": e = self.writeTrigonometric(f, "sec")
            elif fx == "Cosec": e = self.writeTrigonometric(f, "csc")
            elif fx == "Cot": e = self.writeTrigonometric(f, "cot")
            equations.append(e)
            f = "qt"
            fx = qt_functions[graph_num-1]
        txt = "x = " + equations[0] + ",\ny = " + equations[1]
        txt_equation = tk.Label(root, text=txt, bg="white")
        txt_equation.config(font=("Gadugi", 12))
        if graph_num == 1: txt_equation.place(x=70, y=430)
        if graph_num == 2: txt_equation.place(x=70, y=480)
        if graph_num == 3: txt_equation.place(x=70, y=530)
        if graph_num == 4: txt_equation.place(x=70, y=580)
        if graph_num == 5: txt_equation.place(x=70, y=630)

    def writeTableOfValues(self):
        if scatter_num == 1:
            txt = "Blue scatter"
            txt_equation = tk.Label(root, text=txt, bg="white")
            txt_equation.config(font=("Gadugi", 12))
            txt_equation.place(x=70, y=438)
        elif scatter_num == 2:
            txt = "Orange scatter"
            txt_equation = tk.Label(root, text=txt, bg="white")
            txt_equation.config(font=("Gadugi", 12))
            txt_equation.place(x=70, y=488)
        elif scatter_num == 3:
            txt = "Green scatter"
            txt_equation = tk.Label(root, text=txt, bg="white")
            txt_equation.config(font=("Gadugi", 12))
            txt_equation.place(x=75, y=538)
        elif scatter_num == 4:
            txt = "Red scatter"
            txt_equation = tk.Label(root, text=txt, bg="white")
            txt_equation.config(font=("Gadugi", 12))
            txt_equation.place(x=75, y=588)
        elif scatter_num == 5:
            txt = "Purple scatter"
            txt_equation = tk.Label(root, text=txt, bg="white")
            txt_equation.config(font=("Gadugi", 12))
            txt_equation.place(x=75, y=638)

    def writeAlgebraicFraction(self, co):
        if co == "fx": a, b, c, d, e, f, g, h, i, j = coefficients[graph_num-1]
        if co == "pt": a, b, c, d, e, f, g, h, i, j = pt_coefficients[graph_num-1]
        if co == "qt": a, b, c, d, e, f, g, h, i, j = qt_coefficients[graph_num-1]
        l = "x" if functions[graph_num-1] != "" else "t"
        ax4 = str(self.makeIntOrBlank(a)) + l + "^4" 
        bx3 = str(self.makeIntOrBlank(b)) + l + "^3" 
        cx2 = str(self.makeIntOrBlank(c)) + l + "^2" 
        dx = str(self.makeIntOrBlank(d)) + l
        e = " + " + str(self.makeIntOrBlank(e)) 
        fx4 = str(self.makeIntOrBlank(f)) + l + "^4" 
        gx3 = str(self.makeIntOrBlank(g)) + l + "^3" 
        hx2 = str(self.makeIntOrBlank(h)) + l + "^2" 
        ix = str(self.makeIntOrBlank(i)) + l 
        j = " + " + str(self.makeIntOrBlank(j))
        equation = "(" + ax4 + " + " + bx3 + " + " + cx2 + " + " + dx + e + ")/(" + fx4 + " + " + gx3 + " + " + hx2 + " + " + ix + j + ")"
        return equation

    def writeCircular(self):
        global graph_num
        a, b, r = coefficients[graph_num-1]
        if a == int(a): a = int(a)
        if b == int(b): b = int(b)
        if r == int(r): r = int(r)
        xa = "(x - " + str(a) + ")"
        yb = "(y - " + str(b) + ")"
        equation = xa + " + " + yb + " = " + str(r)
        txt_equation = tk.Label(root, text=equation, bg="white")
        txt_equation.config(font=("Gadugi", 12))
        if graph_num == 1: txt_equation.place(x=70, y=438)
        if graph_num == 2: txt_equation.place(x=70, y=488)
        if graph_num == 3: txt_equation.place(x=70, y=538)
        if graph_num == 4: txt_equation.place(x=70, y=588)
        if graph_num == 5: txt_equation.place(x=70, y=638)

    def writeAx(self, co):
        if co == "fx": a, b, c = coefficients[graph_num-1]
        if co == "pt": a, b, c = pt_coefficients[graph_num-1]
        if co == "qt": a, b, c = qt_coefficients[graph_num-1]
        l = "x" if functions[graph_num-1] != "" else "t"
        a = str(self.makeIntOrBlank(a)) + "^"
        bx = str(self.makeIntOrBlank(b)) + l
        c = " + " + str(self.makeIntOrBlank(c))
        equation = a + bx + c
        return equation

    def writeXa(self, co):
        if co == "fx": a, b, c = coefficients[graph_num-1]
        if co == "pt": a, b, c = pt_coefficients[graph_num-1]
        if co == "qt": a, b, c = qt_coefficients[graph_num-1]
        l = "x" if functions[graph_num-1] != "" else "t"
        a = str(self.makeIntOrBlank(a))
        bx = l + "^" + str(self.makeIntOrBlank(b))
        c = " + " + str(self.makeIntOrBlank(c))
        equation = a + bx + c
        return equation

    def writeLogarithmic(self, co):
        if co == "fx": a, b, c, d = coefficients[graph_num-1]
        if co == "pt": a, b, c, d = pt_coefficients[graph_num-1]
        if co == "qt": a, b, c, d = qt_coefficients[graph_num-1]
        l = "x" if functions[graph_num-1] != "" else "t"
        a = str(self.makeIntOrBlank(a)) + "log_"
        logb = str(b) + "_("
        cx = str(self.makeIntOrBlank(c)) + l + ")"
        d = " + " + str(self.makeIntOrBlank(d))
        equation = a + logb + cx + d
        return equation

    def writePolynomial(self, co):
        if co == "fx": a, b, c, d, e = coefficients[graph_num-1]
        if co == "pt": a, b, c, d, e = pt_coefficients[graph_num-1]
        if co == "qt": a, b, c, d, e = qt_coefficients[graph_num-1]
        l = "x" if functions[graph_num-1] != "" else "t"
        ax4 = str(self.makeIntOrBlank(a)) + l + "^4 + "# if a != 0 else ""
        bx3 = str(self.makeIntOrBlank(b)) + l + "^3 + "# if b != 0 else ""
        cx2 = str(self.makeIntOrBlank(c)) + l + "^2 + "# if c != 0 else ""
        dx = str(self.makeIntOrBlank(d)) + l#  if d != 0 else ""
        e = " + " + str(self.changeToInt(e)) if e != 0 else ""
        equation = ax4 + bx3 + cx2 + dx + e
        return equation

    def writeReciprocal(self, co):
        if co == "fx": a, b, c, d, e, f = coefficients[graph_num-1]
        if co == "pt": a, b, c, d, e, f = pt_coefficients[graph_num-1]
        if co == "qt": a, b, c, d, e, f = qt_coefficients[graph_num-1]
        l = "x" if functions[graph_num-1] != "" else "t"
        a = str(self.changeToInt(a))
        bx4 = str(self.makeIntOrBlank(b)) + l + "^4 + "# if b != 0 else "_"
        cx3 = str(self.makeIntOrBlank(c)) + l + "^3 + "# if c != 0 else "_"
        dx2 = str(self.makeIntOrBlank(d)) + l + "^2 + "# if d != 0 else "_"
        ex = str(self.makeIntOrBlank(e)) + l#  if e != 0 else ""
        f = " + " + str(self.changeToInt(f)) if f != 0 else ""
        equation = a + "/(" + bx4 + cx3 + dx2 + ex + f + ")"
        return equation

    def writeTrigonometric(self, co, trig):
        if co == "fx": a, b, c = coefficients[graph_num-1]
        if co == "pt": a, b, c = pt_coefficients[graph_num-1]
        if co == "qt": a, b, c = qt_coefficients[graph_num-1]
        l = "x" if functions[graph_num-1] != "" else "t"
        a = str(self.makeIntOrBlank(a))
        trigb = trig + "(" + str(self.makeIntOrBlank(b)) + l + ")"
        c = " + " + str(self.makeIntOrBlank(c))
        equation = a + trigb + c
        return equation

    def makeIntOrBlank(self, num):
        num = self.changeToInt(num)
        if num == 1: num = ""
        return num
    
    def drawEquationButtons(self):
        btn_one = tk.Button(root, text="1", width=2, height=1, command=self.setUserGraphToZero)
        btn_two = tk.Button(root, text="2", width=2, height=1, command=self.setUserGraphToOne)
        btn_three = tk.Button(root, text="3", width=2, height=1, command=self.setUserGraphToTwo)
        btn_four = tk.Button(root, text="4", width=2, height=1, command=self.setUserGraphToThree)
        btn_five = tk.Button(root, text="5", width=2, height=1, command=self.setUserGraphToFour)
        if (graph_num or scatter_num) == 1: btn_one.place(x=30, y=438)
        if (graph_num or scatter_num) == 2: btn_two.place(x=30, y=488)
        if (graph_num or scatter_num) == 3: btn_three.place(x=30, y=538)
        if (graph_num or scatter_num) == 4: btn_four.place(x=30, y=588)
        if (graph_num or scatter_num) == 5: btn_five.place(x=30, y=638)
        
    def setUserGraphToZero(self):
        global user_graph
        user_graph = 0
        
    def setUserGraphToOne(self):
        global user_graph
        user_graph = 1

    def setUserGraphToTwo(self):
        global user_graph
        user_graph = 2

    def setUserGraphToThree(self):
        global user_graph
        user_graph = 3

    def setUserGraphToFour(self):
        global user_graph
        user_graph = 4

    def plotCartesian(self):
        global diagram, graph_num
        graph_num = graph_num + 1
        self.createWindow()
        diagram.plot(self.x, self.fx)
        canvas.draw()
        diagram.axvline(color="black", linewidth=1.25)
        diagram.axhline(color="black", linewidth=1.25)
        root.mainloop()

    def binomial(self, n, p):
        global graph_num, diagram
        graph_num = graph_num + 1
        self.createWindow()
        low = binom.ppf(0, n, p)
        high = binom.ppf(1, n, p)
        points = np.arange(low, high)
        canvas.draw()
        diagram.vlines(points, 0, binom.pmf(points, n, p), color=next(diagram._get_lines.prop_cycler)["color"], linewidth=5)
        root.mainloop()
        
    def normal(self, mu, sigma):
        global graph_num, diagram
        graph_num = graph_num + 1
        self.createWindow()
        low = math.ceil(mu) - 4*math.ceil(sigma)
        high = math.ceil(mu) + 4*math.ceil(sigma)
        points = np.linspace(low, high, 100)
        graph = norm.pdf(points, mu, sigma)
        diagram.plot(points, graph)     
        canvas.draw()
        diagram.axvline(x=mu,color="black", linestyle="--", linewidth=0.5)
        root.mainloop()

    def uniform(self, a, b):
        global graph_num, diagram
        graph_num = graph_num + 1
        self.createWindow()
        low = math.floor(a) - 2
        high = math.ceil(b) + 2
        points = np.linspace(low, high, 100)
        graph = uniform.pdf(points, a, b-a)
        diagram.plot(points, graph)     
        canvas.get_tk_widget().place(x=560, y=45)
        root.mainloop()
        
    def plotParametric(self, fx):
        global graph_num
        graph_num = graph_num + 1
        self.createWindow()
        diagram.plot(fx, self.fy)     
        diagram.axvline(color="black", linewidth=1.25)
        diagram.axhline(color="black", linewidth=1.25)
        canvas.draw()
        root.mainloop()

    def tableOfValues(self, x, y):
        global canvas, scatter_num
        scatter_num = scatter_num + 1
        self.createWindow()
        diagram.scatter(x, y, marker="x")     
        canvas = FigureCanvasTkAgg(figure, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=560, y=45)
        diagram.axvline(color="black", linewidth=1.25)
        diagram.axhline(color="black", linewidth=1.25)
        root.mainloop()

class Interpret:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Plotter")
        # where the axes will go (temporary frame)
        self.frame = tk.Frame(root, width=650, height=650, bg="white", borderwidth=5)
        ## points
        self.txt_pnts = tk.Label(root, text="Points")
        self.txt_pnts.config(font=("Gadugi", 14))
        self.btn_turn = tk.Button(root, text="Locate\nturning points", width=12, height=2, command=self.whichCurveForTP)
        self.btn_turn.config(font=("Gadugi", 11))
        self.btn_pnt = tk.Button(root, text="Coordinates\nof point", width=12, height=2, command=self.coordinate)
        self.btn_pnt.config(font=("Gadugi", 11))
        self.btn_rts = tk.Button(root, text="Locate\nroots", width=12, height=2, command=self.locateRoots)
        self.btn_rts.config(font=("Gadugi", 11))
        self.btn_mid = tk.Button(root, text="Find\nmidpoint", width=12, height=2, command=self.midpoint)
        self.btn_mid.config(font=("Gadugi", 11))
        self.btn_poi = tk.Button(root, text="Points of\nintersection", width=12, height=2, command=self.poiWindowNeeded)
        self.btn_poi.config(font=("Gadugi", 11))
        ##lines
        self.txt_line = tk.Label(root, text="Lines")
        self.txt_line.config(font=("Gadugi", 14))
        self.btn_seg = tk.Button(root, text="Segment\nlength", width=12, height=2, command=self.segmentLength)
        self.btn_seg.config(font=("Gadugi", 11))
        self.btn_bestfit = tk.Button(root, text="Line of\nbest fit", width=12, height=2, command=self.lineOfBestFit)
        self.btn_bestfit.config(font=("Gadugi", 11))
        self.btn_nor = tk.Button(root, text="Draw a\nnormal", width=12, height=2, command=self.normal)
        self.btn_nor.config(font=("Gadugi", 11))
        self.btn_tan = tk.Button(root, text="Draw a\ntangent", width=12, height=2, command=self.tangent)
        self.btn_tan.config(font=("Gadugi", 11))
        ##axes
        self.txt_axes = tk.Label(root, text="Axes")
        self.txt_axes.config(font=("Gadugi", 14))
        self.btn_axnames = tk.Button(root,text="Change axes\nnames", width=12, height=2, command=self.axesNames)
        self.btn_axnames.config(font=("Gadugi", 11))
        self.btn_axscalepi = tk.Button(root, text="Change\nscale to π", width=12, height=2, command=self.changeScaleToPi)
        self.btn_axscalepi.config(font=("Gadugi", 11))
        self.btn_axscalelin = tk.Button(root, text="Change\nscale back", width=12, height=2, command=self.changeScaleToLinear)
        self.btn_axscalelin.config(font=("Gadugi", 11))
        # others
##        self.btn_undo = tk.Button(root, text="Undo", width=12, height=2, command=self.undo)
##        self.btn_undo.config(font=("Gadugi", 11))
##        self.btn_rst = tk.Button(root, text="Reset", width=12, height=2)
##        self.btn_rst.config(font=("Gadugi", 11))
        #####self.txt_zoom = tk.Label(root, text="Zoom")
        #####self.txt_zoom.config(font=("Gadugi", 12))
        #####self.s_zoom = tk.Scale(root, orient="horizontal", length=200, from_=1.0, to=8.0)
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Add graph title", command=self.graphTitle)
        self.filemenu.add_command(label="Save image", command=self.saveFigure)
        self.filemenu.add_command(label="Add new graph", command=self.addNewGraph)
        self.filemenu.add_command(label="Restart", command=self.restartProgram)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quitProgram)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.pointsmenu = tk.Menu(self.menubar, tearoff=0)
        self.pointsmenu.add_command(label="Locate turning points", command=self.whichCurveForTP)
        self.pointsmenu.add_command(label="Coordinates of point", command=self.coordinate)
        self.pointsmenu.add_command(label="Locate roots", command=self.locateRoots)
        self.pointsmenu.add_command(label="Find midpoint", command=self.midpoint)
        self.pointsmenu.add_command(label="Points of intersection", command=self.poiWindowNeeded)
        self.menubar.add_cascade(label="Points", menu=self.pointsmenu)
        self.linemenu = tk.Menu(self.menubar, tearoff=0)
        self.linemenu.add_command(label="Segment length", command=self.segmentLength)
        self.linemenu.add_command(label="Line of best fit", command=self.lineOfBestFit)
        self.linemenu.add_command(label="Draw a normal", command=self.normal)
        self.linemenu.add_command(label="Draw a tangent", command=self.tangent)
        self.menubar.add_cascade(label="Lines", menu=self.linemenu)
        self.axesmenu = tk.Menu(self.menubar, tearoff=0)
        self.axesmenu.add_command(label="Change axes names", command=self.axesNames)
        self.axesmenu.add_command(label="Change scale to π", command=self.changeScaleToPi)
        self.menubar.add_cascade(label="Axes", menu=self.axesmenu)
        self.distmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Distributions", menu=self.distmenu)        
        self.distmenu.add_command(label="Binomial", command=self.binomialDist)
        self.distmenu.add_command(label="Normal", command=self.normalDist)

        self.copWindow = ""
        self.mpWindow = ""
        self.anWindow = ""
        self.gtWindow = ""
        self.bWindow = ""
        self.nWindow = ""
        self.poiWindow = ""

        self.ent_x = ""
        self.ent_y = ""
        self.ent_t = ""
        self.t = False

        self.tan = False
        self.nor = False

        self.ent_newxname = ""
        self.ent_newyname = ""

        self.ent_point1x = ""
        self.ent_point1y = ""
        self.ent_point2x = ""
        self.ent_point2y = ""

        self.findx = False
        self.pt = False
        self.qt = False

        self.ent_title = ""

        self.ent_binx = ""
        self.ent_biny = ""
        self.b = ""
        self.opt_bin = ["P(X=x)", "P(X<x)", "P(X>x)", "P(X≤x)", "P(X≥x)", "P(x≤X≤y)"]
        self.om_bin = ""
        self.b = ""
        self.opt_nor = ["P(X<x)", "P(X>x)", "P(X≤x)", "P(X≥x)", "P(x<X<y)"]
        self.om_nor = ""

        self.poiVar1 = ""
        self.poiVar2 = ""

        self.draw()
        
    def draw(self):
        self.frame.place(x=550, y=45)
        self.txt_pnts.place(x=20, y=45)
        self.btn_turn.place(x=20, y=75)
        self.btn_pnt.place(x=140, y=75)
        self.btn_rts.place(x=260, y=75)
        self.btn_mid.place(x=380, y=75)
        self.txt_line.place(x=20, y=220)
        self.btn_seg.place(x=20, y=250)
        self.txt_axes.place(x=20, y=325)
        #self.btn_undo.place(x=20, y=640)
        #self.btn_rst.place(x=140, y=640)
        self.btn_poi.place(x=20, y=140)
        self.btn_axnames.place(x=20, y=355)
        self.btn_axscalepi.place(x=140, y=355)
        self.btn_bestfit.place(x=140, y=250)
        self.btn_nor.place(x=260, y=250)
        self.btn_tan.place(x=380, y=250)
        #####self.txt_zoom.place(x=340, y=351)
        #####self.s_zoom.place(x=260, y=369)
        self.root.config(menu=self.menubar)

    def eOrPi(self, value):
        if value == "": return 1
        elif value == "-" : return -1
        elif value == "e": return math.e
        elif value == "-e": return -math.e
        elif value == "p" or value == "π": return math.pi
        elif value == "-p" or value == "-π": return -math.pi
        else:
            letter_pos = 0
            # checks to see if a multiple of e has been entered
            for digit in value:
                if digit == "e":
                    # separates digits before e from the letter
                    new_value = value[0:letter_pos]
                    try:
                        # attempts multiplication of separated digits with e
                        new_value = float(new_value) * math.e
                    except TypeError:
                        # raised if digits before e are not of type float
                        return TypeError
                    else:
                        # raised if there are characters after the e
                        if letter_pos < (len(value)-1):
                            return ValueError
                        else:
                            return new_value
                else:
                    letter_pos = letter_pos + 1

            # same process for p and π
            letter_pos = 0
            for digit in value:
                if digit == "p" or digit == "π":
                    new_value = value[0:letter_pos]
                    try:
                        new_value = float(new_value) * math.pi
                    except TypeError:
                        return TypeError
                    else:
                        if letter_pos < (len(value)-1):
                            return ValueError
                        else:
                            return new_value
                else:
                    letter_pos = letter_pos + 1
            # if nothing else applies, value should be a float other than 1 or -1
            return value

    def changeToInt(self, num):
        if num == 0.0:
            num = 0
        elif num == int(num):
            num = int(num)
        return num
    
    def addNewGraph(self):
        global window, graph_num
        if graph_num == 5:
            tkMessageBox.showerror("Maximum reached", "The maximum number of graphs has been drawn.") 
        else:
            window.destroy()
            main()

    def whichCurveForTP(self):
        if distributions[user_graph] != "" or len(scatterx[user_graph]) > 0:
            tkMessageBox.showerror("Invalid graph", "Turning points cannot be calculated for this graph style.")
        else:
            global coefficients
            # if the coefficients array is filled up,
            # a Cartesian equation must have been drawn
            if len(coefficients[user_graph]) >= 3: 
                self.turningPointsC()
            else:
                # if it does not contain 3 or more items,
                # the array must be empty,
                # indicating the parametric arrays are full
                self.turningPointsP()

    def turningPointsC(self):
        x = self.findFunctionAndTP()
        if len(x) == 0:
            tkMessageBox.showinfo("No turning points", "This graph has no turning points.")
        else:
            y = self.findYOfTP(x)
            diagram.scatter(x, y, marker="x", s=100, c="#7bd4f5", zorder=3)
            for coordinate in range(len(x)):
                text = "(" + format(float(x[coordinate]), ".2f") + ", " + format(float(y[coordinate]), ".2f") + ")"   
                diagram.annotate(text, xy=(x[coordinate], y[coordinate]), xytext=(x[coordinate]-0.3, y[coordinate]+0.1), fontsize=12)
            canvas.draw()

    def findYOfTP(self, x):
        # holds the corresponding y-coordinate for each x-coordinate
        Y = [] 
        for coordinate in range(len(x)):
            Y.append(self.setValues(x[coordinate]))
        return Y

    def findFunctionAndTP(self):
        fx = functions[user_graph]
        if fx == "Circular" or fx == "a^x" or fx == "Logarithmic" or fx == "Tan" or fx == "Cot" :
            tkMessageBox.showinfo("No turning points", "This graph has no turning points.")
        else:
            # xpoints = array that will hold all of the x-coordinates
            # of the turning points
            if fx == "Algebraic fraction":
                a, b, c, d, e, f, g, h, i, j = coefficients[user_graph]
                xpoints = self.afTurningPoints(a, b, c, d, e, f, g, h, i, j)
            elif fx == "x^a":
                xpoints = [0]
            elif fx == "Polynomial":
                a, b, c, d, = [coefficients[user_graph][i] for i in range(4)]
                xpoints = self.polTurningPoints(a, b, c, d)
            elif fx == "Reciprocal":
                a, b, c, d, e, f = coefficients[user_graph]
                xpoints = self.recTurningPoints(a, b, c, d, e, f)
            else:
                b = coefficients[user_graph][1]
                if fx == "Sin" or fx == "Cosec":
                    xpoints = self.sinCscTurningPoints(b)
                elif fx == "Cos" or fx == "Sec":
                    xpoints = self.cosSecTurningPoints(b)
            return xpoints

    def turningPointsP(self):
        tvalues = self.findQtAndTValues()
        tvalues = list(dict.fromkeys(tvalues))
        tvalues = self.removeInvalidT(tvalues)
        if len(tvalues) == 0:
            tkMessageBox.showinfo("No turning points", "This graph has no turning points.")
        else:
            x = []
            y = []
            for t in range(len(tvalues)):
                # sets coefficients using pt_coefficients
                # uses these and t-value to work out x-value
                self.pt = True
                xpoint = self.setPtValues(tvalues[t])
                x.append(xpoint)
                self.pt = False
                # sets coefficients using qt_coefficients
                # uses these and t-value to work out y-values
                self.qt = True
                ypoint = self.setQtValues(tvalues[t])
                y.append(ypoint)
                self.qt = False
            try:
                diagram.scatter(x, y, marker="x", s=100, c="#7bd4f5", zorder=3)
            except:
                tkMessageBox.showinfo("No turning points", "Turning points could not be calculated.")  
            else:
                for coordinate in range(len(x)):
                    space = 0.1 if coordinate%2 == 0 else -0.4
                    text = "(" + format(float(x[coordinate]), ".2f") + ", " + format(float(y[coordinate]), ".2f") + ")\nt=" + format(float(tvalues[coordinate]), ".2f")   
                    diagram.annotate(text, xy=(x[coordinate], y[coordinate]), xytext=(x[coordinate]-0.3, y[coordinate]+space), fontsize=12)
                canvas.draw()

    def removeInvalidT(self, tvalues):
        global upper_p, lower_p
        values_to_remove = []
        for t in range(len(tvalues)):
            print(t)
            print(tvalues[t])
            print(":)")
            if tvalues[t] > upper_p[user_graph] or tvalues[t] < lower_p[user_graph]:
                values_to_remove.append(tvalues[t])
        for i in range(len(values_to_remove)):
            tvalues.remove(values_to_remove[i])
        return tvalues
    
    def findQtAndTValues(self):
        fx = qt_functions[user_graph]
        if fx == "Algebraic fraction":
            a, b, c, d, e, f, g, h, i, j = qt_coefficients[user_graph]
            t = self.afTurningPoints(a, b, c, d, e, f, g, h, i, j)
        elif fx == "x^a":
            t = [0]
        elif fx == "Polynomial":
            a, b, c, d, = [qt_coefficients[user_graph][i] for i in range(4)]
            t = self.polTurningPoints(a, b, c, d)
        elif fx == "Reciprocal":
            a, b, c, d, e, f = qt_coefficients[user_graph]
            t = self.recTurningPoints(a, b, c, d, e, f)
        else:
            b = qt_coefficients[user_graph][1]
            if fx == "Sin" or fx == "Cosec":
                t = self.sinCscTurningPoints(b)
            elif fx == "Cos" or fx == "Sec":
                t = self.cosSecTurningPoints(b)
            else:
                return []
        return t

    def setPtValues(self, coordinate):
        if len(pt_coefficients[user_graph]) == 3:
            a, b, c = pt_coefficients[user_graph]
            x = self.selectPtFunction(coordinate, a, b, c)
        elif len(pt_coefficients[user_graph]) == 4:
            a, b, c, d = pt_coefficients[user_graph]
            x = self.logCoordinates(coordinate, a, b, c, d)
        elif len(pt_coefficients[user_graph]) == 5:
            a, b, c, d, e = pt_coefficients[user_graph]
            x = self.polCoordinates(coordinate, a, b, c, d, e)
        elif len(pt_coefficients[user_graph]) == 6:
            a, b, c, d, e, f = pt_coefficients[user_graph]
            x = self.recCoordinates(coordinate, a, b, c, d, e, f)
        elif len(pt_coefficients[user_graph]) == 10:
            a, b, c, d, e, f, g, h, i, j = pt_coefficients[user_graph]
            x = self.afCoordinates(coordinate, a, b, c, d, e, f, g, h, i, j)
        return x

    def selectPtFunction(self, coordinate, *args):
        fx = pt_functions[user_graph]
        if fx == "a^x":
            xcoordinate = self.axCoordinates(coordinate, *args)
        elif fx == "x^a":
            xcoordinate = self.xaCoordinates(coordinate, *args)
        elif fx == "Sin" or fx == "Cosec":
            xcoordinate = self.sinCscCoordinates(coordinate, *args)
        elif fx == "Cos" or fx == "Sec":
            xcoordinate = self.cosSecCoordinates(coordinate, *args)
        elif fx == "Tan" or fx == "Cot":
            xcoordinate = self.tanCotCoordinates(coordinate, *args)
        return xcoordinate

    def setQtValues(self, coordinate):
        if len(qt_coefficients[user_graph]) == 3:
            a, b, c = qt_coefficients[user_graph]
            y = self.selectQtFunction(coordinate, a, b, c)
        elif len(qt_coefficients[user_graph]) == 4:
            a, b, c, d = qt_coefficients[user_graph]
            y = self.logCoordinates(coordinate, a, b, c, d)
        elif len(qt_coefficients[user_graph]) == 5:
            a, b, c, d, e = qt_coefficients[user_graph]
            y = self.polCoordinates(coordinate, a, b, c, d, e)
        elif len(qt_coefficients[user_graph]) == 6:
            a, b, c, d, e, f = qt_coefficients[user_graph]
            y = self.recCoordinates(coordinate, a, b, c, d, e, f)
        elif len(qt_coefficients[user_graph]) == 10:
            a, b, c, d, e, f, g, h, i, j = qt_coefficients[user_graph]
            y = self.afCoordinates(coordinate, a, b, c, d, e, f, g, h, i, j)
        return y

    def selectQtFunction(self, coordinate, *args):
        fx = qt_functions[user_graph]
        if fx == "a^x":
            ycoordinate = self.axCoordinates(coordinate, *args)
        elif fx == "x^a":
            ycoordinate = self.xaCoordinates(coordinate, *args)
        elif fx == "Sin" or fx == "Cosec":
            ycoordinate = self.sinCscCoordinates(coordinate, *args)
        elif fx == "Cos" or fx == "Sec":
            ycoordinate = self.cosSecCoordinates(coordinate, *args)
        elif fx == "Tan" or fx == "Cot":	
            ycoordinate = self.tanCotCoordinates(coordinate, *args)
        return ycoordinate

    def afTurningPoints(self, a, b, c, d, e, f, g, h, i, j):
        a, b, c, d, e, f, g, h, i, j = self.changeToInt(a), self.changeToInt(b), self.changeToInt(c), self.changeToInt(d), self.changeToInt(e), self.changeToInt(f), self.changeToInt(g), self.changeToInt(h), self.changeToInt(i), self.changeToInt(j)
        try:
            solveset(diff((a*x**4 + b*x**3 + c*x**2 + d*x + e)/(f*x**4 + g*x**3 + h*x**2 + i*x + j), x), x, domain=S.Reals)
        except TypeError:
            tkMessageBox.showerror("Error", "The turning points could not be calculated for this graph.")
        else:
            X = []
            for point in solveset(diff((a*x**4 + b*x**3 + c*x**2 + d*x + e)/(f*x**4 + g*x**3 + h*x**2 + i*x + j), x), x, domain=S.Reals):
                X.append(point)
            return X

    def polTurningPoints(self, a, b, c, d):
        a, b, c, d = self.changeToInt(a), self.changeToInt(b), self.changeToInt(c), self.changeToInt(d)
        try:
            solveset(4*a*x**3 + 3*b*x**2 + 2*c*x + d, x, domain=S.Reals)
        except TypeError:
            tkMessageBox.showerror("Error", "The turning points could not be calculated for this graph.")
        else:
            X = []
            for point in solveset(4*a*x**3 + 3*b*x**2 + 2*c*x + d, x, domain=S.Reals):
                X.append(point)
            return X

    def recTurningPoints(self, a, b, c, d, e, f):
        a, b, c, d, e, f = self.changeToInt(a), self.changeToInt(b), self.changeToInt(c), self.changeToInt(d), self.changeToInt(e), self.changeToInt(f)
        try:
            solveset(diff(a/(b*x**4 + c*x**3 + d*x**2 + e*x + f), x), x, domain=S.Reals)
        except TypeError:
            tkMessageBox.showerror("Error", "The turning points could not be calculated for this graph.")
        else:
            X = []
            for point in solveset(diff(a/(b*x**4 + c*x**3 + d*x**2 + e*x + f), x), x, domain=S.Reals):
                X.append(point)
            return X

    def sinCscTurningPoints(self, b):
        X = []
        pv = math.acos(0)/b #(acos(y))/b
        X.extend((round(pv, 2), round(-pv, 2))) # if val is in the domain
        count = 2
        val = pv
        subtract = True
        while val <= 2*math.pi: # while val does not exceed the upmost positive limit
            if val != pv: # and val is in the domain
                X.append(round(val, 2))
            if subtract == True:
                val = (count*math.pi)/b - pv #(count*math.pi - b*pv)/b
                subtract = False
            else:
                val = (count*math.pi)/b + pv #(-count*math.pi - b*pv)/b
                subtract = True
                count = count + 2

        val = pv
        count = 2
        subtract = True
        while val >= -2*math.pi: # while val does not exceed the lowest negative limit
            if val != pv: # and val is in the domain
                X.append(round(val, 2))
            if subtract == True:
                val = -((count*math.pi)/b - pv) #(-count*math.pi - b*pv)/b
                subtract = False
            else:
                val = -((count*math.pi)/b + pv) #(-count*math.pi + b*pv)/b
                subtract = True
                count = count + 2
        return X

    def cosSecTurningPoints(self, b):
        X = []
        pv = -math.asin(0)/b
        X.append(round(pv, 2)) # if val is in the domain
        count = 1 
        val = pv
        while val < 2*math.pi: # while val does not exceed the upmost positive limit
            if val != pv: # and val is in the domain
                X.append(val)
            if count%2 == 1:
                val = (count*math.pi)/b - pv #(count*math.pi - b*pv)/b
            else:
                val = (count*math.pi)/b + pv #(-count*math.pi - b*pv)/b
            count = count + 1

        val = pv
        count = 1
        while val > -2*math.pi: # while val does not exceed the lowest negative limit
            if val != pv: # and val is in the domain
                X.append(round(val, 2))
            if count%2 == 1:
                val = (-count*math.pi)/b - pv #(-count*math.pi - b*pv)/b 
            else:
                val = (-count*math.pi)/b + pv #(-count*math.pi + b*pv)/b
            count = count + 1
            
        return X

    def coordinate(self):
        # condition 1 implies a distribution has been made as the function at that index is filled
        # condition 2 implied a scatter plot has been made as that index contains x-coordinates
        if distributions[user_graph] != "" or len(scatterx[user_graph]) > 0:
            tkMessageBox.showerror("Invalid graph", "Coordinates cannot be calculated for this graph style.")
        else:
            # parametric or Cartesian graph has been selected so program can go ahead as normal
            self.copWindow = tk.Tk()
            self.copWindow.title("Coordinates of point")
            self.copWindow.geometry("350x80")
            txt_xory = tk.Label(self.copWindow, text="Which coordinate?")
            txt_xory.config(font=("Gadugi", 12))
            txt_xory.place(x=5, y=5)
            var = tk.IntVar()
            rbtn_x = tk.Radiobutton(self.copWindow, text="x", variable=var, value=1, tristatevalue=0, command=self.enterY)
            rbtn_x.config(font=("Gadugi", 12))
            rbtn_x.place(x=140, y=5)
            rbtn_y = tk.Radiobutton(self.copWindow, text="y", variable=var, value=2, tristatevalue=0, command=self.enterX)
            rbtn_y.config(font=("Gadugi", 12))
            rbtn_y.place(x=180, y=5)
            if len(coefficients[user_graph]) < 3:
                self.copWindow.geometry("390x80")
                rbtn_t = tk.Radiobutton(self.copWindow, text="t", variable=var, value=3, tristatevalue=0, command=self.enterT)
                rbtn_t.config(font=("Gadugi", 12))
                rbtn_t.place(x=220, y=5)

    def enterX(self):
        txt_entery = tk.Label(self.copWindow, text="Enter x-coordinate:")
        txt_entery.config(font=("Gadugi", 12))
        txt_entery.place(x=5, y=30)
        self.ent_enterxy = tk.Entry(self.copWindow, width=2, font="Gadugi", justify="left")
        self.ent_enterxy.place(x=145, y=32)
        if len(coefficients[user_graph]) >= 3:
            btn_calculatey = tk.Button(self.copWindow, text="Calculate\ny-coordinate", width=11, height=2, command=self.plotOtherCoordinate)
            btn_calculatey.config(font=("Gadugi", 11))
            btn_calculatey.place(x=230, y=10)
        else:
            self.pt = True
            btn_calculatey = tk.Button(self.copWindow, text="Calculate\ny-coordinate", width=11, height=2, command=self.findT) 
            btn_calculatey.config(font=("Gadugi", 11))
            btn_calculatey.place(x=270, y=10)
        btn_calculatey.lift()

    def enterY(self):
        txt_enterx = tk.Label(self.copWindow, text="Enter y-coordinate:")
        txt_enterx.config(font=("Gadugi", 12))
        txt_enterx.place(x=5, y=30)
        self.ent_enterxy = tk.Entry(self.copWindow, width=2, font="Gadugi", justify="left")
        self.ent_enterxy.place(x=145, y=32)
        if len(coefficients[user_graph]) >= 3:
            btn_calculatex = tk.Button(self.copWindow, text="Calculate\nx-coordinate", width=11, height=2, command=self.makeFindxTrue)
            btn_calculatex.config(font=("Gadugi", 11))
            btn_calculatex.place(x=230, y=10)
        else:
            btn_calculatex = tk.Button(self.copWindow, text="Calculate\nx-coordinate", width=11, height=2, command=self.findT)
            btn_calculatex.config(font=("Gadugi", 11))
            btn_calculatex.place(x=270, y=10)
        btn_calculatex.lift()

    def enterT(self):
        txt_entert = tk.Label(self.copWindow, text="Enter value of t:")
        txt_entert.config(font=("Gadugi", 12))
        txt_entert.place(x=5, y=30)
        self.ent_enterxy = tk.Entry(self.copWindow, width=2, font="Gadugi", justify="left")
        self.ent_enterxy.place(x=125, y=32)
        btn_calculatexy = tk.Button(self.copWindow, text="Calculate\ncoordinates", width=11, height=2, command=self.findXandY)
        btn_calculatexy.config(font=("Gadugi", 11))
        btn_calculatexy.place(x=270, y=10)
        btn_calculatexy.lift()

    def findXandY(self):
        global lower_p, upper_p, user_graph
        try:
            t = float(self.eOrPi(self.ent_enterxy.get()))
            if t < lower_p[user_graph] or t > upper_p[user_graph]:
                raise ArithmeticError
        except ArithmeticError:
            tkMessageBox.showerror("Invalid input", "This value of t is not in the entered domain.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            X = []
            self.pt = True
            x = self.setValues(t)
            self.pt = False
            X.append(x)
            if len(X) == 0:
                tkMessageBox.showinfo("No coordinates", "This value has no corresponding coordinates in the domain.")
            else:
                Y = []
                y = self.setValues(t)
                Y.append(y)
                diagram.scatter(x, y, marker="x", s=100, c="#964b01", zorder=3)
                for coordinate in range(len(X)):
                    text = "(" + format(float(X[coordinate]), ".2f") + ", " + format(float(Y[coordinate]), ".2f") + ")\nt=" + str(t)   
                    space = 0.1 if coordinate%2 == 0 else -0.4
                    diagram.annotate(text, xy=(X[coordinate], Y[coordinate]), xytext=(X[coordinate]-0.3, Y[coordinate]+space), fontsize=12)
                canvas.draw()
        
    def findT(self):
        try:
            x = float(self.eOrPi(self.ent_enterxy.get()))
        except TypeError:
            tkMessageBox.showerror("Error!", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Error!", "Only real values, e and π/p can be entered.")
        else:
            self.findx = True
            T = self.setValues(x)
            print(T)
            if type(T) != float:
                T = list(dict.fromkeys(T))
                T = self.removeInvalidT(T)
            self.findx = False
            if len(T) == 0:
                tkMessageBox.showinfo("No coordinates", "This value has no corresponding coordinates in the domain.")
            else:
                changed = False
                if self.pt == False:
                    self.pt = True
                    changed = True
                else:
                    self.pt = False
                Y = []
                for t in range(len(T)):
                    y = self.setValues(T[t])
                    Y.append(y)
                print(T)
                print(Y)
                if changed == False: # this means the x-coordinate was given
                    ####otherC = list(dict.fromkeys(otherC))
                    for coordinate in range(len(T)):
                        diagram.scatter(x, Y[coordinate], marker="x", s=100, c="#964b01", zorder=3)
                        space = 0.1 if coordinate%2 == 0 else -0.4
                        text = "(" + format(float(x), ".2f") + ", " + format(float(Y[coordinate]), ".2f") + ")\nt=" + format(float(T[coordinate]), ".2f")   
                        diagram.annotate(text, xy=(x, Y[coordinate]), xytext=(x-0.3, Y[coordinate]+space), fontsize=12)
                    self.pt = False
                else:
                    for coordinate in range(len(T)):
                        diagram.scatter(Y[coordinate], x, marker="x", s=100, c="#964b01", zorder=3)
                        text = "(" + format(float(Y[coordinate]), ".2f") + ", " + format(float(x), ".2f") + ")\nt=" + format(float(T[coordinate]), ".2f")  
                        space = 0.1 if coordinate%2 == 0 else -0.4
                        diagram.annotate(text, xy=(Y[coordinate], x), xytext=(Y[coordinate]-0.3, x+space), fontsize=12)
                canvas.draw()
    
    def makeFindxTrue(self):
        try:
            coordinate = float(self.eOrPi(self.ent_enterxy.get()))
        except TypeError:
            tkMessageBox.showerror("Error!", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Error!", "Only real values, e and π/p can be entered.")
        else:
            self.findx = True
            self.plotOtherCoordinate("#964b01", coordinate)

    def locateRoots(self):
        if distributions[user_graph] != "" or len(scatterx[user_graph]) > 0:
            tkMessageBox.showerror("Invalid graph", "Roots cannot be calculated for this graph style.")
        else:
            if len(coefficients[user_graph]) >= 3:
                self.locateCartesianRoots()
            else:
                self.locateParametricRoots()

    def locateCartesianRoots(self):
        self.findx = True
        self.plotOtherCoordinate("#f545ec", 0)

    def locateParametricRoots(self):
        self.findx = True
        T = self.setValues(0)
        self.findx = False
        X = []
        self.pt = True
        values_to_remove = []
        for t in range(len(T)):
            # condition 1 = lower than the start of the domain of t
            # condition 2 = higher than the end of the domain of t
            # a value of t only needs to satisfy one condition to be removed
            if T[t] < lower_p[user_graph] or T[t] > upper_p[user_graph]:
                values_to_remove.append(T[t])
        for i in range(len(values_to_remove)):
            T.remove(values_to_remove[i])
        if len(T) == 0:
            tkMessageBox.showinfo("No roots", "This graph has no roots in the domain.")
        else:
            for t in range(len(T)):
                x = self.setValues(T[t])
                X.append(x)
            self.pt = False
            for coordinate in range(len(X)):
                diagram.scatter(X[coordinate], 0, marker="x", s=100, c="#f545ec", zorder=3)
                space = 0.1 if coordinate%2 == 0 else -0.4
                text = "(" + format(float(X[coordinate]), ".2f") + ", " + str(0) + ")\nt=" + format(float(T[coordinate]), ".2f")
                diagram.annotate(text, xy=(X[coordinate], 0), xytext=(X[coordinate]-0.3, space), fontsize=12)
            canvas.draw()
    
    def plotOtherCoordinate(self, *args):
        continu = False
        if self.findx == False:
            try:
                givenC = float(self.eOrPi(self.ent_enterxy.get()))
            except TypeError:
                tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
            except ValueError:
                tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
            else:
                continu = True
                color = "#964b01"
        else:
            continu = True
            color = args[0]
            givenC = args[1]
        if continu == True:
            otherC = self.setValues(givenC)
            try:
                otherC = float(otherC)
            except:
                pass
            finally:
                if type(otherC) == float or type(otherC) == int:
                    if self.findx == True:
                        text = "(" + format(float(otherC), ".2f") + ", " + format(float(givenC), ".2f") + ")"
                        diagram.scatter(otherC, givenC, marker="x", s=100, c=color, zorder=3)
                        diagram.annotate(text, xy=(otherC, givenC), xytext=(otherC-0.3, givenC+0.1), fontsize=12)
                    else:
                        text = "(" + format(float(givenC), ".2f") + ", " + format(float(otherC), ".2f") + ")"
                        diagram.scatter(givenC, otherC, marker="x", s=100, c=color, zorder=3)
                        diagram.annotate(text, xy=(givenC, otherC), xytext=(givenC-0.3, otherC+0.1), fontsize=12)
                elif otherC == "Empty" or len(otherC) == 0:
                    tkMessageBox.showinfo("No coordinates/roots", "The value has no corresponding coordinates or the graph has no roots in the domain.")
                else:
                    otherC = list(dict.fromkeys(otherC)) # gets rid of duplicate values
                    if self.findx == True:
                        for solution in range(len(otherC)):
                            text = "(" + format(float(otherC[solution]), ".2f") + ", " + format(float(givenC), ".2f") + ")"
                            diagram.scatter(otherC[solution], givenC, marker="x", s=100, c=color, zorder=3)
                            diagram.annotate(text, xy=(otherC[solution], givenC), xytext=(otherC[solution]-0.3, givenC+0.1), fontsize=12)
                    else:
                        for solution in range(len(otherC)):
                            text = "(" + format(float(givenC), ".2f") + ", " + format(float(otherC[solution]), ".2f") + ")"
                            diagram.scatter(givenC, otherC[solution], marker="x", s=100, c=color, zorder=3)
                            diagram.annotate(text, xy=(givenC, otherC[solution]), xytext=(givenC-0.3, otherC[solution]+0.1), fontsize=12)
                self.findx = False
                canvas.draw()

    def setValues(self, coordinate):
        if len(coefficients[user_graph]) >= 3:
            co = coefficients
        elif self.pt == True:
            co = pt_coefficients
        else:
            co = qt_coefficients
        if len(co[user_graph]) == 3:
            a, b, c = co[user_graph]
            otherValue = self.selectFunction(coordinate, a, b, c)
        elif len(co[user_graph]) == 4:
            a, b, c, d = co[user_graph]
            otherValue = self.logCoordinates(coordinate, a, b, c, d)
        elif len(co[user_graph]) == 5:
            a, b, c, d, e = co[user_graph]
            otherValue = self.polCoordinates(coordinate, a, b, c, d, e)
        elif len(co[user_graph]) == 6:
            a, b, c, d, e, f = co[user_graph]
            otherValue = self.recCoordinates(coordinate, a, b, c, d, e, f)
        elif len(co[user_graph]) == 10:
            a, b, c, d, e, f, g, h, i, j = co[user_graph]
            otherValue = self.afCoordinates(coordinate, a, b, c, d, e, f, g, h, i, j)
        return otherValue

    def selectFunction(self, coordinate, *args):
        if len(coefficients[user_graph]) >= 3:
            fx = functions[user_graph]
        elif self.pt == True:
            fx = pt_functions[user_graph]
        else:
            fx = qt_functions[user_graph]
        if fx == "Circular":
            otherV = self.cirCoordinates(coordinate, *args)
        elif fx == "a^x":
            otherV = self.axCoordinates(coordinate, *args)
        elif fx == "x^a":
            otherV = self.xaCoordinates(coordinate, *args)
        elif fx == "Sin" or fx == "Cosec":
            otherV = self.sinCscCoordinates(coordinate, *args)
        elif fx == "Cos" or fx == "Sec":
            otherV = self.cosSecCoordinates(coordinate, *args)
        elif fx == "Tan" or fx == "Cot":
            otherV = self.tanCotCoordinates(coordinate, *args)
        return otherV
    
    def afCoordinates(self, givenVal, a, b, c, d, e, f, g, h, i, j):
        gv = givenVal
        a, b, c, d, e, f, g, h, i, j = self.changeToInt(a), self.changeToInt(b), self.changeToInt(c), self.changeToInt(d), self.changeToInt(e), self.changeToInt(f), self.changeToInt(g), self.changeToInt(h), self.changeToInt(i), self.changeToInt(j)
        if self.findx == True:
            try:
                solveset((a*x**4 + b*x**3 + c*x**2 + d*x + e)/(f*x**4 + g*x**3 + h*x**2 + i*x + j) - gv, x, domain=S.Reals)
            except TypeError:
                tkMessageBox.showerror("Error", "The required coordinates could not be calculated for this graph.")
            else:
                s = []
                for sol in solveset((a*x**4 + b*x**3 + c*x**2 + d*x + e)/(f*x**4 + g*x**3 + h*x**2 + i*x + j) - gv, x, domain=S.Reals):
                    s.append(sol)
                return s
        else:
            Y = (a*gv**4 + b*gv**3 + c*gv**2 + d*gv + e)/(f*gv**4 + g*gv**3 + h*gv**2 + i*gv + j)
            return Y
    
    def cirCoordinates(self, givenVal, a, b, r):
        if self.findx == True:
            if a + math.sqrt(r-(givenVal-b)**2) == a - math.sqrt(r-(givenVal-b)**2):
                X = [a + math.sqrt(r-(givenVal-b)**2)]
            else:
                X = [a + math.sqrt(r-(givenVal-b)**2), a - math.sqrt(r-(givenVal-b)**2)]
            return X
        else:
            if b + math.sqrt(r-(givenVal-a)**2) == b - math.sqrt(r-(givenVal-a)**2):
                Y = math.sqrt(r-(givenVal-a)**2) + b
            else:
                Y = [b + math.sqrt(r-(givenVal-a)**2), b - math.sqrt(r-(givenVal-a)**2)]
            return Y
    
    def axCoordinates(self, givenVal, a, b, c):
        # if calculating x
        if self.findx == True:
            try:
                X = (math.log(givenVal - c, 10))/(b*math.log(a, 10))
            except ValueError:
                return []
            else:
                s = []
                s.append(X)
                return s
        # if calculating y
        else:
            Y = a**(b*givenVal) + c
            return Y

    def xaCoordinates(self, givenVal, a, b, c):
        # if calculating x
        if self.findx == True:
            X = []
            radicand = (givenVal-c)/a
            if radicand >= 0:
                if b%2 == 0:
                    X.extend([radicand**(1/b), -radicand**(1/b)])
                else:
                    X.append(radicand**(1/b))
            else:
                radicand = -radicand
                if b%2 == 0:
                    X.extend([-(radicand**(1/b)), -(-radicand**(1/b))])
                else:
                    X.append(-(radicand**(1/b)))
            return X
        # if calculating y
        else:
            Y = a*(givenVal**b) + c
            return Y
    
    def logCoordinates(self, givenVal, a, b, c, d):
        if self.findx == True:
            X = [(b**((givenVal-d)/a))/c]
            return X
        else:
            if c*givenVal < 0:
                pass
            elif c*givenVal != 0:
                Y = a*math.log(c*givenVal, b) + d
                return Y
            else:
                return np.inf
    
    def polCoordinates(self, givenVal, a, b, c, d, e):
        gv = self.changeToInt(givenVal)
        a, b, c, d, e = self.changeToInt(a), self.changeToInt(b), self.changeToInt(c), self.changeToInt(d), self.changeToInt(e)
        if self.findx == True:
            try:
                solveset((a*x**4 + b*x**3 + c*x**2 + d*x + e) - gv, x, domain=S.Reals)
            except TypeError:
                tkMessageBox.showerror("Error", "The required coordinates could not be calculated for this graph.")
            else:
                s = []
                for sol in solveset((a*x**4 + b*x**3 + c*x**2 + d*x + e) - gv, x, domain=S.Reals):
                    s.append(sol)
                return s
        else:
            Y = a*gv**4 + b*gv**3 + c*gv**2 + d*gv + e
            return Y
    
    def recCoordinates(self, givenVal, a, b, c, d, e, f):
        gv = self.changeToInt(givenVal)
        a, b, c, d, e, f = self.changeToInt(a), self.changeToInt(b), self.changeToInt(c), self.changeToInt(d), self.changeToInt(e), self.changeToInt(f)
        if self.findx == True:
            try:
                solveset((a/(b*x**4 + c*x**3 + d*x**2 + e*x + f)) - gv, x, domain=S.Reals)
            except TypeError:
                tkMessageBox.showerror("Error", "The required coordinates could not be calculated for this graph.")
            else:
                s = []
                for sol in solveset((a/(b*x**4 + c*x**3 + d*x**2 + e*x + f)) - gv, x, domain=S.Reals):
                    s.append(sol)
                return s
        else:
            denominator = b*gv**4 + c*gv**3 + d*gv**2 + e*gv + f
            if denominator == 0:
                Y = np.inf
            else:
                Y = a/(b*gv**4 + c*gv**3 + d*gv**2 + e*gv + f)
            return Y

    def areRootsPossible(self, fx, a, c):
        if fx == "Sin" or fx == "Cos":
            if abs(c) > abs(a):
                return False
            else:
                return True
        elif fx == "Sec" or fx == "Cosec":
            if abs(c) >= abs(a):
                return True
            else:
                return False
            pass
        
    def sinCscCoordinates(self, givenVal, a, b, c):
        if len(coefficients[user_graph]) >= 3:
            function = functions[user_graph]
            lower, upper = lower_c[user_graph], upper_c[user_graph]
        elif self.pt == True:
            function = pt_functions[user_graph]
            lower, upper = lower_p[user_graph], upper_p[user_graph]
        else:
            function = qt_functions[user_graph]
            lower, upper = lower_p[user_graph], upper_p[user_graph]

        if self.findx == True:
            if givenVal == 0:
                continu = self.areRootsPossible(function, a, c)
            else:
                continu = True
            if continu == True:
                if function == "Sin":
                    pv = math.asin(givenVal-c)/b if a==1 else math.asin((givenVal-c)/a)/b
                elif function == "Cosec":
                    pv = acsc(givenVal-c)/b if a==1 else acsc((givenVal-c)/a)/b
                s = []
                s.append(pv) # if val is in the domain
                count = 1 
                val = pv
                while val >= 0 and val <= upper: # while val does not exceed the upmost positive limit
                    if val != pv: # and val is in the domain
                        s.append(val)
                    if count%2 == 1:
                        val = (count*math.pi)/b - pv #(count*math.pi - b*pv)/b
                    else:
                        val = (count*math.pi)/b + pv #(-count*math.pi - b*pv)/b
                    count = count + 1

                val = pv
                count = 1
                while val >= lower: # while val does not exceed the lowest negative limit
                    if val != pv: # and val is in the domain
                        s.append(val)
                    if count%2 == 1:
                        val = (-count*math.pi)/b - pv #(-count*math.pi - b*pv)/b 
                    else:
                        val = (-count*math.pi)/b + pv #(-count*math.pi + b*pv)/b
                    count = count + 1
                return s
            else:
                return "Empty"

        else:
            if function == "Sin" or (self.pt == True and pt_functions[user_graph] == "Sin") or (self.qt == True and qt_functions[user_graph] == "Sin"):
                Y = a*math.sin(b*givenVal) + c
            elif function == "Cosec" or (self.pt == True and pt_functions[user_graph] == "Cosec") or (self.qt == True and qt_functions[user_graph] == "Cosec"):
                Y = a*csc(b*givenVal) + c
            return Y
            
        
    def cosSecCoordinates(self, givenVal, a, b, c):
        if len(coefficients[user_graph]) >= 3:
            function = functions[user_graph]
            lower, upper = lower_c[user_graph], upper_c[user_graph]
        elif self.pt == True:
            function = pt_functions[user_graph]
            lower, upper = lower_p[user_graph], upper_p[user_graph]
        else:
            function = qt_functions[user_graph]
            lower, upper = lower_p[user_graph], upper_p[user_graph]

        if self.findx == True:
            if givenVal == 0:
                continu = self.areRootsPossible(function, a, c)
            else:
                continu = True
            if continu == True:
                if function == "Cos":
                    pv = math.acos(givenVal-c)/b if a==1 else math.acos((givenVal-c)/a)/b #(math.acos(y))/b
                elif function == "Sec":
                    pv = asec(givenVal-c)/b if a==1 else asec((givenVal-c)/a)/b
                s = []
                s.extend([pv, -pv]) # if val is in the domain
                count = 2
                val = pv
                subtract = True
                while val >= 0 and val <= upper: # while val does not exceed the upmost positive limit
                    if val != pv: # and val is in the domain
                        s.append(val)
                    if subtract == True:
                        val = (count*math.pi)/b - pv #(count*math.pi - b*pv)/b
                        subtract = False
                    else:
                        val = (count*math.pi)/b + pv #(-count*math.pi - b*pv)/b
                        subtract = True
                        count = count + 2

                val = pv
                count = 2
                subtract = True
                while val >= lower: # while val does not exceed the lowest negative limit
                    if val != pv: # and val is in the domain
                        s.append(val)
                    if subtract == True:
                        val = -((count*math.pi)/b - pv) #(-count*math.pi - b*pv)/b
                        subtract = False
                    else:
                        val = -((count*math.pi)/b + pv) #(-count*math.pi + b*pv)/b
                        subtract = True
                        count = count + 2
                return s
            else:
                return "Empty"
        else:
            if function == "Cos" or (self.pt == True and pt_functions[user_graph] == "Cos") or (self.qt == True and qt_functions[user_graph] == "Cos"):
                Y = a*math.cos(b*givenVal) + c
            elif function == "Sec" or (self.pt == True and pt_functions[user_graph] == "Sec") or (self.qt == True and qt_functions[user_graph] == "Sec"):
                Y = a*sec(b*givenVal) + c
            return Y
    
    def tanCotCoordinates(self, givenVal, a, b, c):
        if len(coefficients[user_graph]) >= 3:
            function = functions[user_graph]
            lower, upper = lower_c[user_graph], upper_c[user_graph]
        elif self.pt == True:
            function = pt_functions[user_graph]
            lower, upper = lower_p[user_graph], upper_p[user_graph]
        else:
            function = qt_functions[user_graph]
            lower, upper = lower_p[user_graph], upper_p[user_graph]

        if self.findx == True:
            if function == "Tan":
                pv = math.atan((givenVal-c)/a)/b
            elif function == "Cot":
                pv = acot((givenVal-c)/a)/b
                
            s = []
            s.append(pv)

            val = pv
            while val >= 0 and val <= upper: # while val does not exceed the upmost positive limit
                if val != pv: # and val is in the domain
                    s.append(round(val, 2))
                val = val + math.pi/b

            val = pv
            while val >= lower: # while val does not exceed the lowest negative limit
                if val != pv: # and val is in the domain
                    s.append(round(val, 2))
                val = val - math.pi/b

            return s 
        else:
            if function == "Tan" or (self.pt == True and pt_functions[user_graph] == "Tan"):
                Y = a*math.tan(b*givenVal) + c
            elif function == "Cot" or (self.pt == True and pt_functions[user_graph] == "Cot"):
                Y = a*cot(b*givenVal) + c
                Y = round(Y, 7)
            return Y

    def midpoint(self):
        self.mpWindow = tk.Tk()
        self.mpWindow.title("Midpoint")
        self.mpWindow.geometry("380x95")
        txt_coords = tk.Label(self.mpWindow, text="Enter the coordinates of the first and second points:")
        txt_coords.config(font=("Gadugi", 12))
        txt_coords.place(x=5, y=5)
        txt_point1 = tk.Label(self.mpWindow, text="Point 1: (         ,         )")
        txt_point1.config(font=("Gadugi", 12))
        txt_point1.place(x=5, y=30)
        self.ent_point1x = tk.Entry(self.mpWindow, width=2, font="Gadugi", justify="center")
        self.ent_point1x.place(x=75, y=32)
        self.ent_point1y = tk.Entry(self.mpWindow, width=2, font="Gadugi", justify="center")
        self.ent_point1y.place(x=115, y=32)
        txt_point2 = tk.Label(self.mpWindow, text="Point 2: (         ,         )")
        txt_point2.config(font=("Gadugi", 12))
        txt_point2.place(x=5, y=60)
        self.ent_point2x = tk.Entry(self.mpWindow, width=2, font="Gadugi", justify="center")
        self.ent_point2x.place(x=75, y=62)
        self.ent_point2y = tk.Entry(self.mpWindow, width=2, font="Gadugi", justify="center")
        self.ent_point2y.place(x=115, y=62)
        btn_midpoint = tk.Button(self.mpWindow, text="Calculate\nmidpoint", width=10, height=2, command=self.calculateMidpoint)
        btn_midpoint.config(font=("Gadugi", 12))
        btn_midpoint.place(x=160, y=32)

    def calculateMidpoint(self):
        try:
            x1 = float(self.eOrPi(self.ent_point1x.get()))
            y1 = float(self.eOrPi(self.ent_point1y.get()))
            x2 = float(self.eOrPi(self.ent_point2x.get()))
            y2 = float(self.eOrPi(self.ent_point2y.get()))
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")  
        else:
            if x1 == x2 and y1 == y2:
                tkMessageBox.showinfo("Same point", "Midpoint equals points 1 and 2")
            else:
                x = [x2, x1]
                y = [y2, y1]
                diagram.plot(x, y)
                x.append((x2+x1)/2)
                y.append((y2+y1)/2)
                diagram.scatter(x, y, marker="+", s=100, c="#f52020", zorder=3)
                text = "(" + format(float((x2+x1)/2), ".2f") + ", " + format(float((y2+y1)/2), ".2f") + ")"
                diagram.annotate(text, xy=((x2+x1)/2, (y2+y1)/2), xytext=((x2+x1)/2-0.3, (y2+y1)/2+0.1), fontsize=12)        
                canvas.draw()

    def poiWindowNeeded(self):
        global graph_num
        if graph_num == 1:
            tkMessageBox.showerror("No intersection", "Two graphs are needed for finding points of intersection.")
        elif graph_num == 2:
            if functions[0] != "" and functions[1] != "":
                if (functions[0] or functions[1]) == "Logarithmic":
                    tkMessageBox.showerror("Error", "Points of intersection cannot be calculated when one curve is logarithmic.")
                else:
                    self.pointsOfIntersection(0, 1)
            else:
                tkMessageBox.showerror("Error", "Two Cartesian graphs must be drawn to find points of intersection.")
        elif graph_num > 2:
            self.pointsOfIntersectionWindow()
            
    def pointsOfIntersectionWindow(self):
        global graph_num
        self.poiWindow = tk.Tk()
        self.poiWindow.title("Points of intersection")
        self.poiWindow.geometry("550x300")
        txt_intersect = tk.Label(self.poiWindow, text="Pick the numbers of the graphs you would like to find the intersection points of:")
        txt_intersect.config(font=("Gadugi, 12"))
        txt_intersect.place(x=5, y=5)
        txt_graph1 = tk.Label(self.poiWindow, text="Select first graph:")
        txt_graph1.config(font=("Gadugi, 12"))
        txt_graph1.place(x=5, y=40)
        txt_graph2 = tk.Label(self.poiWindow, text="Select second graph:")
        txt_graph2.config(font=("Gadugi, 12"))
        txt_graph2.place(x=270, y=40)
        btn_enter = tk.Button(self.poiWindow, text="Calculate\nintersection", width=11, height=2, command=self.findValuesSelected)
        btn_enter.config(font=("Gadugi, 12"))
        btn_enter.place(x=200, y=100)
            
        self.poiVar1 = tk.StringVar(self.poiWindow)
        self.poiVar2 = tk.StringVar(self.poiWindow)
        
        if graph_num >= 3:
            rbtn_graph11 = tk.Radiobutton(self.poiWindow, text="1", variable=self.poiVar1, value=1, tristatevalue=0)
            rbtn_graph11.config(font=("Gadugi", 12))
            rbtn_graph11.place(x=5, y=65)
            rbtn_graph21 = tk.Radiobutton(self.poiWindow, text="1", variable=self.poiVar2, value=1, tristatevalue=0)
            rbtn_graph21.config(font=("Gadugi", 12))
            rbtn_graph21.place(x=270, y=65)
            rbtn_graph12 = tk.Radiobutton(self.poiWindow, text="2", variable=self.poiVar1, value=2, tristatevalue=0)
            rbtn_graph12.config(font=("Gadugi", 12))
            rbtn_graph12.place(x=50, y=65)
            rbtn_graph22 = tk.Radiobutton(self.poiWindow, text="2", variable=self.poiVar2, value=2, tristatevalue=0)
            rbtn_graph22.config(font=("Gadugi", 12))
            rbtn_graph22.place(x=315, y=65)
            rbtn_graph13 = tk.Radiobutton(self.poiWindow, text="3", variable=self.poiVar1, value=3, tristatevalue=0)
            rbtn_graph13.config(font=("Gadugi", 12))
            rbtn_graph13.place(x=95, y=65)
            rbtn_graph23 = tk.Radiobutton(self.poiWindow, text="3", variable=self.poiVar2, value=3, tristatevalue=0)
            rbtn_graph23.config(font=("Gadugi", 12))
            rbtn_graph23.place(x=360, y=65)
        if graph_num >= 4:
            rbtn_graph14 = tk.Radiobutton(self.poiWindow, text="4", variable=self.poiVar1, value=4, tristatevalue=0)
            rbtn_graph14.config(font=("Gadugi", 12))
            rbtn_graph14.place(x=140, y=65)
            rbtn_graph24 = tk.Radiobutton(self.poiWindow, text="4", variable=self.poiVar2, value=4, tristatevalue=0)
            rbtn_graph24.config(font=("Gadugi", 12))
            rbtn_graph24.place(x=405, y=65)
        if graph_num == 5:
            rbtn_graph15 = tk.Radiobutton(self.poiWindow, text="5", variable=self.poiVar1, value=5, tristatevalue=0)
            rbtn_graph15.config(font=("Gadugi", 12))
            rbtn_graph15.place(x=185, y=65)
            rbtn_graph25 = tk.Radiobutton(self.poiWindow, text="5", variable=self.poiVar2, value=5, tristatevalue=0)
            rbtn_graph25.config(font=("Gadugi", 12))
            rbtn_graph25.place(x=450, y=65)

    def findValuesSelected(self):
        if self.poiVar1.get() == "" or self.poiVar2.get() == "":
            tkMessageBox.showerror("Error", "Select two Cartesian graphs.")
        else:
            graph1 = int(self.poiVar1.get())
            graph2 = int(self.poiVar2.get())
            if functions[graph1-1] != "" and functions[graph2-1] != "":
                if (functions[graph1-1] or functions[graph2-1]) == "Logarithmic":
                    tkMessageBox.showerror("Error", "Points of intersection cannot be calculated when one curve is logarithmic.")
                else:
                    self.pointsOfIntersection(graph1, graph2)
            else:
                tkMessageBox.showerror("Error", "Select two Cartesian graphs.")
        
    def pointsOfIntersection(self, graph1, graph2):
        global user_graph
        # the actual value of user_graph is temporarily held in a local variable;
        # all subroutines use values from arrays with the index 'user_graph', so
        # instead of using different variables in its place, the indices of the
        # graphs that will have intersection points calculated are substituted
        # in its place; once this subroutine is over, the original value of
        # user_graph is restored
        temp_user_graph = user_graph
        Y1 = []
        # the coordinates of the first graph are returned and stored in Y1
        user_graph = graph1
        X1 = np.arange(lower_c[user_graph], upper_c[user_graph], 0.001)  
        for i in range(len(X1)):      
            y = self.setValues(X1[i]) 
            Y1.append(y)              
        Y2 = []
        # the coordinates of the second graph are returned and stored in Y2
        user_graph = graph2
        X2 = np.arange(lower_c[user_graph], upper_c[user_graph], 0.001)  
        for i in range(len(X2)):      
            y = self.setValues(X2[i]) 
            Y2.append(y)              
        # restoration of the original user_graph value
        user_graph = temp_user_graph
        # changes Y1 and Y2 into two 2D arrays using x- and y-values
        C1 = np.column_stack((X1, Y1))
        C2 = np.column_stack((X2, Y2))
        # each curve is made as an instance of LineString
        # LineString uses each 2D array to form a 'tuple' of coordinates
        # each item in the tuple holds the x-coordinate, then the y-coordinate
        curve1 = LineString(C1)
        curve2 = LineString(C2)
        # returns coordinates of the points where the first curve intersects with
        # the second curve
        # also returned in the same 'tuple' form as the instances of LineString
        try:
            intersects = curve1.intersection(curve2)        # returns the coordinates of the points of intersection in two arrays
        except:                                             # x-coordinates stored in array 'x', y-coordinates stored in array 'y'
            tkMessageBox.showerror("Error", "The points of intersection were not able to be calculated for these graphs.")
        else:
            if intersects.geom_type == "MultiPoint":
                x, y = LineString(intersects).xy
                for coordinate in range(len(x)):
                    space = 0.1 if coordinate%2 == 0 else -0.4
                    text = "(" + format(float(x[coordinate]), ".2f") + ", " + format(float(y[coordinate]), ".2f") + ")"   
                    diagram.annotate(text, xy=(x[coordinate], y[coordinate]), xytext=(x[coordinate]-0.3, y[coordinate]+space), fontsize=12)
                    diagram.scatter(x[coordinate], y[coordinate], marker="+", s=100, c="#777777", zorder=3)
            elif intersects.geom_type == "Point":
                x, y = intersects.xy
                text = "(" + format(x[0], ".2f") + ", " + format(y[0], ".2f") + ")"   
                diagram.annotate(text, xy=(x[0], y[0]), xytext=(x[0]-0.3, y[0]+0.1), fontsize=12)
                diagram.scatter(x[0], y[0], marker="+", s=100, c="#777777", zorder=3)
            else:
                tkMessageBox.showinfo("No intersection", "The selected graphs do not intersect.")
            canvas.draw()
       
    def segmentLength(self):
        self.midpoint()
        self.mpWindow.title("Length of segment")
        btn_midpoint = tk.Button(self.mpWindow, text="Calculate\nlength", width=10, height=2, command=self.calculateSegmentLength)
        btn_midpoint.config(font=("Gadugi", 12))
        btn_midpoint.place(x=160, y=32)

    def calculateSegmentLength(self):
        try:
            x1 = float(self.eOrPi(self.ent_point1x.get()))
            y1 = float(self.eOrPi(self.ent_point1y.get()))
            x2 = float(self.eOrPi(self.ent_point2x.get()))
            y2 = float(self.eOrPi(self.ent_point2y.get()))
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            length = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            if type(length) == float: length = round(length, 1)
            diagram.annotate(str(length), xy=((x2+x1)/2,(y2+y1)/2), xytext=((x2+x1)/2, (y2+y1)/2+0.1), color="#f4583e")
            diagram.annotate("", xy=(x1, y1), xytext=(x2, y2), arrowprops=(dict(arrowstyle="<->", color="#f4583e", lw=2)))
            canvas.draw()

    def lineOfBestFit(self):
        global scatterx, scattery, scatter_num
        if len(scatterx[user_graph]) > 0:
            m, c = np.polyfit(scatterx[scatter_num-1], scattery[scatter_num-1], 1)
            y = []
            for i in range(len(scatterx[scatter_num-1])):
                y.append(m*scatterx[scatter_num-1][i] + c)
            diagram.plot(scatterx[scatter_num-1], y)#, color="#7ddb35")
            canvas.draw()
        else:
            tkMessageBox.showerror("Invalid graph", "Lines of best fit can only be drawn for scatter plots.")

    def normal(self):
        if (pt_functions[user_graph] or distributions[user_graph]) != "" or len(scatterx[user_graph]) > 0:
            tkMessageBox.showerror("Invalid graph", "Normals/tangents cannot be drawn for this graph style.")
            return False
        else:
            self.nor = True
            self.ntWindow = tk.Tk()
            self.ntWindow.title("Draw a normal")
            self.ntWindow.geometry("380x65")
            txt_coords = tk.Label(self.ntWindow, text="Coordinates where the normal")
            txt_coords.config(font=("Gadugi", 12))
            txt_coords.place(x=5, y=5)
            txt_drawn = tk.Label(self.ntWindow, text="should be drawn: (       ,       )") 
            txt_drawn.config(font=("Gadugi", 12))
            txt_drawn.place(x=5, y=28)
            self.ent_x = tk.Entry(self.ntWindow, width=2, font="Gadugi", justify="center")
            self.ent_x.place(x=140, y=30)
            self.ent_y = tk.Entry(self.ntWindow, width=2, font="Gadugi", justify="center")
            self.ent_y.place(x=170, y=30)
            btn_normal = tk.Button(self.ntWindow, text="Draw\nnormal", width=10, height=2, command=self.drawTangentNormal)
            btn_normal.config(font=("Gadugi", 12))
            btn_normal.place(x=250, y=5)

    def tangent(self):
        valid_graph = self.normal()
        if valid_graph != False:
            self.nor = False
            self.tan = True
            self.ntWindow.title("Draw a tangent")
            txt_coords = tk.Label(self.ntWindow, text="Coordinates where the tangent")
            txt_coords.config(font=("Gadugi", 12))
            txt_coords.place(x=5, y=5)
            btn_tangent = tk.Button(self.ntWindow, text="Draw\ntangent", width=10, height=2, command=self.drawTangentNormal)
            btn_tangent.config(font=("Gadugi", 12))
            btn_tangent.place(x=250, y=5)

    def drawTangentNormal(self):
        global graph_num, last_action, points_list
        try:
            x = float(self.eOrPi(self.ent_x.get()))
            y = float(self.eOrPi(self.ent_y.get()))
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            try:
                test_Y = self.checkCoordinate(x)
                y = round(y, 7)
                match = False
                for Y in range(len(test_Y)):
                    if test_Y[Y] == y:
                        match = True
                if match == False:
                    raise ArithmeticError
            except ArithmeticError:
                tkMessageBox.showerror("Invalid coordinates", "These coordinates are not on the curve")   
            else:
                line = self.setddxValues(x, y)
                if line == "undefined":
                    diagram.axvline(x=x, color="#9a53f1")
                else:
                    X = np.linspace(lower_c[user_graph], upper_c[user_graph], 100)
                    fx = []
                    for i in range(len(X)):
                        fx.append(line[0]*X[i] + line[1])
                    diagram.plot(X, fx)
                diagram.scatter(x, y, marker="+", s=100, c="#f52020", zorder=3)
                canvas.draw()
                self.tan = False
                self.nor = False

    def checkCoordinate(self, x):
        Y = []
        self.findx = False
        if functions[user_graph] != "":
            y = self.setValues(x)
            Y.append(y)
        else:
            self.findx = True
            self.pt = True
            T = self.setValues(x)
            for t in range(len(T)):
                if T[t] < lower_p[user_graph] or T[t] > upper_p[user_graph]:
                    T.remove(T[t])
            self.findx = False
            self.pt = False
            for t in range(len(T)):
                y = self.setValues(t)
                Y.append(y)
        return Y

    def setddxValues(self, x, y):
        if len(coefficients[user_graph]) == 3:
            a, b = [coefficients[user_graph][i] for i in range(2)]
            line = self.selectDerivative(x, y, a, b)
        elif len(coefficients[user_graph]) == 4:
            a, b = [coefficients[user_graph][i] for i in range(2)]
            line = self.ddxLogarithmic(x, y, a, b)
        elif len(coefficients[user_graph]) == 5:
            a, b, c, d = [coefficients[user_graph][i] for i in range(4)]
            line = self.selectDerivative(x, y, a, b, c, d)
        elif len(coefficients[user_graph]) == 6:
            a, b, c, d, e, f = coefficients[user_graph]
            line = self.ddxReciprocal(x, y, a, b, c, d, e, f)
        elif len(coefficients[user_graph]) == 10:
            a, b, c, d, e, f, g, h, i, j = coefficients[user_graph]
            line = self.ddxAlgebraicFraction(x, y, a, b, c, d, e, f, g, h, i, j)
        return line
        
    def selectDerivative(self, x, y, *args):
        global function
        fx = functions[user_graph]
        if fx == "Algebraic function":
            equation = self.ddxAlgebraicFraction(x, y, *args)
        elif fx == "Circular":
            equation = self.ddxCircular(x, y, *args)
        elif fx == "a^x":
            equation = self.ddxAx(x, y, *args)
        elif fx == "x^a":
            equation = self.ddxXa(x, y, *args)
        elif fx == "Polynomial":
            equation = self.ddxPolynomial(x, y, *args)
        elif fx == "Sin":
            equation = self.ddxSin(x, y, *args)
        elif fx == "Cos":
            equation = self.ddxCos(x, y, *args)
        elif fx == "Sec":
            equation = self.ddxSec(x, y, *args)
        elif fx == "Cosec":
            equation = self.ddxCosec(x, y, *args)
        elif fx == "Cot":
            equation = self.ddxCot(x, y, *args)
        return equation

    def ddxAlgebraicFraction(self, x, y, a, b, c, d, e, f, g, h, i, j):
        u = a*x**4 + b*x**3 + c*x**2 + d*x + e
        dudx = a*4*x**3 + b*3*x**2 + c*2*x + d
        v = f*x**4 + g*x**3 + h*x**2 + i*x + j
        dvdx = f*4*x**3 + g*3*x**2 + h*2*x + i
        der = (v*dudx - u*dvdx)/(v**2)
        gori = self.gradientOrIntercept(x, y, der)
        return gori
    
    def ddxCircular(self, x, y, a, b):
        if (y-b == 0 and self.tan == True) or (-a-x == 0 and self.nor == True):
            return "undefined"
        elif (y-b == 0 and self.nor == True) or (-a-x == 0 and self.tan == True):
            i = self.intercept(y, 0, x)
            return 0, i
        else:
            der = (-a-x)/(y-b)
            gori = self.gradientOrIntercept(x, y, der)
            return gori

    def ddxAx(self, x, y, a, b):
        if a == math.e:
            der = b*math.e**(b*x)
        else:
            der = (a**(b*x))*b*math.log(a)
        gori = self.gradientOrIntercept(x, y, der)
        return gori

    def ddxXa(self, x, y, a, b):
        der = a*b*x**(b-1)
        gori = self.gradientOrIntercept(x, y, der)
        return gori

    def ddxLogarithmic(self, x, y, a, b):
        if (x == 0 and self.tan == True) or (a*math.log(math.e, b) == 0 and self.nor == True):
            return "undefined"
        elif (x == 0 and self.nor == True) or (a*math.log(math.e, b) == 0 and self.tan == True):
            i = self.intercept(y, 0, x)
            return 0, i
        else:
            if b == math.e:
                der = a/x
            else:
                der = (a*math.log(math.e, b))/x
            gori = self.gradientOrIntercept(x, y, der)
        return gori
    
    def ddxPolynomial(self, x, y, a, b, c, d):
        der = a*4*x**3 + b*3*x**2 + c*2*x + d
        gori = self.gradientOrIntercept(x, y, der)
        return gori

    def ddxReciprocal(self, x, y, a, b, c, d, e, f):
        der = -a*(4*b*x**3 + 3*c*x**2 + 2*d*x + e)/(b*x**4 + c*x**3 + d*x**2 + e*x + f)**2
        gori = self.gradientOrIntercept(x, y, der)
        return gori

    def ddxSin(self, x, y, a, b):
        der = a*b*math.cos(b*x)
        der = round(der, 7)
        gori = self.gradientOrIntercept(x, y, der)
        return gori
    
    def ddxCos(self, x, y, a, b):
        der = -a*b*math.sin(b*x)
        der = round(der, 7) # addition
        gori = self.gradientOrIntercept(x, y, der)
        return gori
    
    def ddxSec(self, x, y, a, b):
        der = a*b*sec(b*x)*math.tan(b*x)
        der = round(der, 7)
        gori = self.gradientOrIntercept(x, y, der)
        return gori
    
    def ddxCosec(self, x, y, a, b):
        der = -a*b*csc(b*x)*cot(b*x)
        der = round(der, 7)
        gori = self.gradientOrIntercept(x, y, der)
        return gori

    def ddxCot(self, x, y, a, b):
        der = -a*b*(csc(b*x)**2)
        der = round(der, 7)
        gori = self.gradientOrIntercept(x, y, der)
        return gori

    def gradientOrIntercept(self, x, y, d):
        if self.nor == True:
            g = self.gradient(d, x, y)
            self.nor = False
            return g
        elif self.tan == True:
            i = self.intercept(y, d, x)
            self.tan = False
            return i

    def gradient(self, d, x, y):
        if d == 0:
            return "undefined"
        else:
            g = -1/d
            i = self.intercept(y, g, x)
        return i

    def intercept(self, y, m, x):
        c = y - m*x
        return m, c
    
    def axesNames(self):
        self.anWindow = tk.Tk()
        self.anWindow.title("Change axes names")
        self.anWindow.geometry("450x65")
        txt_newxname = tk.Label(self.anWindow, text="New x-axis name:")
        txt_newxname.config(font=("Gadugi", 12))
        txt_newxname.place(x=5, y=5)
        self.ent_newxname = tk.Entry(self.anWindow, width=20, font="Gadugi")
        self.ent_newxname.place(x=135, y=7)
        txt_newyname = tk.Label(self.anWindow, text="New y-axis name:")
        txt_newyname.config(font=("Gadugi", 12))
        txt_newyname.place(x=5, y=30)
        self.ent_newyname = tk.Entry(self.anWindow, width=20, font="Gadugi")
        self.ent_newyname.place(x=135, y=32)
        btn_axnames = tk.Button(self.anWindow, text="Change\naxes names", width=10, height=2, command=self.changeNames)
        btn_axnames.config(font=("Gadugi", 12))
        btn_axnames.place(x=330, y=5)

    def changeNames(self):
        x = self.ent_newxname.get()
        y = self.ent_newyname.get()
        diagram.set_xlabel(x, fontsize = 15)
        diagram.set_ylabel(y, fontsize = 15)
        canvas.draw()

    def graphTitle(self):
        self.gtWindow = tk.Tk()
        self.gtWindow.title("Add graph title")
        self.gtWindow.geometry("305x65")
        txt_title = tk.Label(self.gtWindow,
                             text="Title of graph:")
        txt_title.config(font=("Gadugi", 12))
        txt_title.place(x=5, y=5)
        self.ent_title = tk.Entry(self.gtWindow, width=20,
                                  font="Gadugi")
        self.ent_title.place(x=5, y=32)
        btn_title = tk.Button(self.gtWindow, text="Add title",
                              width=10, height=2,
                              command=self.addGraphTitle)
        btn_title.config(font=("Gadugi", 12))
        btn_title.place(x=200, y=5)

    def addGraphTitle(self):
        new_title = self.ent_title.get()
        diagram.set_title(new_title, fontsize=17)
        canvas.draw()
        
    def changeScaleToPi(self):
        diagram.xaxis.set_major_locator(ticker.MultipleLocator(base=math.pi))
        canvas.draw()
        ticktext = [tick.get_text() for tick in diagram.get_xticklabels()]
        for i in range(len(ticktext)):
            if ticktext[i][0] == "−":
                ticktext[i] = ticktext[i].replace("−", "")
                ticktext[i] = -float(ticktext[i])
            new_text = round(float(ticktext[i])/math.pi)
            ticktext[i] = str(new_text) + "π"
        diagram.set_xticklabels(ticktext)
        self.btn_axscalelin.place(x=140, y=355)
        self.btn_axscalelin.lift()
        self.axesmenu.delete("Change scale to π")
        self.axesmenu.add_command(label="Change scale back", command=self.changeScaleToLinear)
        canvas.draw()

    def changeScaleToLinear(self):
        diagram.xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=True))
        diagram.xaxis.set_major_locator(ticker.MultipleLocator(base=2))
        self.btn_axscalepi.place(x=140, y=355)
        self.btn_axscalepi.lift()
        self.axesmenu.delete("Change scale back")
        self.axesmenu.add_command(label="Change scale to π", command=self.changeScaleToPi)
        canvas.draw()

    def saveFigure(self):
        global figure
        image = tk.filedialog.asksaveasfilename(title="Save graph", defaultextension=".png", filetypes=(("PNG Image", "*.png"), ("All Files", "*.*")))
        if image:
            figure.savefig(image, bbox_inches="tight")

    def restartProgram(self):
        restart = tkMessageBox.askquestion("Restart", "Are you sure you wish to restart?")
        if restart == "yes":
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    def quitProgram(self):
        sys.exit()

    def binomialDist(self):
        if distributions[user_graph] != "Binomial":
            tkMessageBox.showerror("Invalid graph", "Select a binomial distribution.")
        else:
            self.bWindow = tk.Tk()
            self.bWindow.title("Binomial distribution")
            self.bWindow.geometry("270x150")
            txt_select = tk.Label(self.bWindow, text="Select value to find:")
            txt_select.config(font=("Gadugi", 12))
            txt_select.place(x=5, y=0)
            self.b = tk.StringVar(self.bWindow)
            self.b.set("Find")
            self.om_bin = tk.OptionMenu(self.bWindow, self.b, *self.opt_bin)
            self.om_bin.config(font=("Gadugi", 12))
            self.om_bin.place(x=5, y=25)
            btn_enter = tk.Button(self.bWindow, text="Enter", width=5, height=1, command=self.selectBinomialOption)
            btn_enter.config(font=("Gadugi", 12))
            btn_enter.place(x=5, y=65)

    def selectBinomialOption(self):
        txt_enter = tk.Label(self.bWindow, text="Enter values:")
        txt_enter.config(font=("Gadugi", 12))
        txt_enter.place(x=160, y=0)
        option = self.b.get()
        self.ent_binx = tk.Entry(self.bWindow, width=2, font="Gadugi", justify="center")
        if option == "P(X=x)":
            txt_xex = tk.Label(self.bWindow,text="P(X=     )")
            txt_xex.config(font=("Gadugi", 13))
            txt_xex.place(x=160, y=25)
            self.ent_binx.place(x=200, y=27)
            self.ent_binx.lift()
            btn_bin = tk.Button(self.bWindow, text="Calculate", width=8, height=1, command=self.calculateBinxex)
        elif option == "P(X<x)":
            txt_xlx = tk.Label(self.bWindow,text="P(X<     )")
            txt_xlx.config(font=("Gadugi", 13))
            txt_xlx.place(x=160, y=25)
            self.ent_binx.place(x=200, y=27)
            self.ent_binx.lift()
            btn_bin = tk.Button(self.bWindow, text="Calculate", width=8, height=1, command=self.calculateBinxlx)
        elif option == "P(X>x)":
            txt_xgx = tk.Label(self.bWindow,text="P(X>     )")
            txt_xgx.config(font=("Gadugi", 13))
            txt_xgx.place(x=160, y=25)
            self.ent_binx.place(x=200, y=27)
            self.ent_binx.lift()
            btn_bin = tk.Button(self.bWindow, text="Calculate", width=8, height=1, command=self.calculateBinxgx)
        elif option == "P(X≤x)":
            txt_xlex = tk.Label(self.bWindow,text="P(X≤     )")
            txt_xlex.config(font=("Gadugi", 13))
            txt_xlex.place(x=160, y=25)
            self.ent_binx.place(x=200, y=27)
            self.ent_binx.lift()
            btn_bin = tk.Button(self.bWindow, text="Calculate", width=8, height=1, command=self.calculateBinxlex)
        elif option == "P(X≥x)":
            txt_xgex = tk.Label(self.bWindow,text="P(X≥     )")
            txt_xgex.config(font=("Gadugi", 13))
            txt_xgex.place(x=160, y=25)
            self.ent_binx.place(x=200, y=27)
            self.ent_binx.lift()
            btn_bin = tk.Button(self.bWindow, text="Calculate", width=8, height=1, command=self.calculateBinxgex)
        else:
            self.ent_biny = tk.Entry(self.bWindow, width=2, font="Gadugi", justify="center")
            txt_xlexley = tk.Label(self.bWindow,text="P(     ≤X≤     )")
            txt_xlexley.config(font=("Gadugi", 13))
            txt_xlexley.place(x=160, y=25)
            self.ent_binx.place(x=180, y=27)
            self.ent_binx.lift()
            self.ent_biny.place(x=237, y=27)
            self.ent_biny.lift()
            btn_bin = tk.Button(self.bWindow, text="Calculate", width=8, height=1, command=self.calculateBinxlexley)
        btn_bin.config(font=("Gadugi", 12))
        btn_bin.place(x=160, y=65)

    def nCr(self, n, r):
        nchooser = math.factorial(n)/(math.factorial(r)*math.factorial(n-r))
        return nchooser

    def calculateBinxex(self):
        try:
            x = int(self.eOrPi(self.ent_binx.get()))
            if x < 0 or x > dist_parameters[user_graph][0]:
                raise ArithmeticError
        except ArithmeticError:
            tkMessageBox.showerror("Invalid input", "This value is not a possible trial number.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            n = dist_parameters[user_graph][0]
            p = dist_parameters[user_graph][1]
            choose = self.nCr(n, x)
            P = choose * (p**x) * (1-p)**(n-x)
            txt = "P(X=" + str(x) + ") = " + format(P, ".4f")
            txt_answer = tk.Label(self.bWindow, text=txt, width=23)
            txt_answer.config(font=("Gadugi", 15), bg="white", anchor="center")
            txt_answer.place(x=5, y=105)
        
    def calculateBinxlx(self):
        try:
            x = int(self.eOrPi(self.ent_binx.get())) # x in P(X<x)
            if x < 0 or x > dist_parameters[user_graph][0]:
                raise ArithmeticError
        except ArithmeticError:
            tkMessageBox.showerror("Invalid input", "This value is not a possible trial number.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            P = 0 
            n = dist_parameters[user_graph][0] # n in X~B(n, p)
            p = dist_parameters[user_graph][1] # p in X~B(n, p)
            for i in range(x):
                choose = self.nCr(n, i) # calculates binomial coefficient
                add = choose * (p**i) * (1-p)**(n-i) # binomial formula
                P = P + add 
            txt = "P(X<" + str(x) + ") = " + format(P, ".4f")
            txt_answer = tk.Label(self.bWindow, text=txt, width=23)
            txt_answer.config(font=("Gadugi", 15), bg="white", anchor="center")
            txt_answer.place(x=5, y=105)
        
    def calculateBinxgx(self):
        try:
            x = int(self.eOrPi(self.ent_binx.get())) # x in P(X<x)
            if x < 0 or x > dist_parameters[user_graph][0]:
                raise ArithmeticError
        except ArithmeticError:
            tkMessageBox.showerror("Invalid input", "This value is not a possible trial number.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            P = 1
            n = dist_parameters[user_graph][0]
            p = dist_parameters[user_graph][1]
            for i in range(x+1):
                choose = self.nCr(n, i)
                subtract = choose * (p**i) * (1-p)**(n-i)
                P = P - subtract
            txt = "P(X>" + str(x) + ") = " + format(P, ".4f")
            txt_answer = tk.Label(self.bWindow, text=txt, width=23)
            txt_answer.config(font=("Gadugi", 15), bg="white", anchor="center")
            txt_answer.place(x=5, y=105)
        
    def calculateBinxlex(self):
        try:
            x = int(self.eOrPi(self.ent_binx.get())) # x in P(X<x)
            if x < 0 or x > dist_parameters[user_graph][0]:
                raise ArithmeticError
        except ArithmeticError:
            tkMessageBox.showerror("Invalid input", "This value is not a possible trial number.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            P = 0 
            n = dist_parameters[user_graph][0]
            p = dist_parameters[user_graph][1]
            for i in range(x+1):
                choose = self.nCr(n, i)
                add = choose * (p**i) * (1-p)**(n-i)
                P = P + add
            txt = "P(X≤" + str(x) + ") = " + format(P, ".4f")
            txt_answer = tk.Label(self.bWindow, text=txt, width=23)
            txt_answer.config(font=("Gadugi", 15), bg="white", anchor="center")
            txt_answer.place(x=5, y=105)

    def calculateBinxgex(self):
        try:
            x = int(self.eOrPi(self.ent_binx.get())) # x in P(X<x)
            if x < 0 or x > dist_parameters[user_graph][0]:
                raise ArithmeticError
        except ArithmeticError:
            tkMessageBox.showerror("Invalid input", "This value is not a possible trial number.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            P = 1
            n = dist_parameters[user_graph][0]
            p = dist_parameters[user_graph][1]
            for i in range(x):
                choose = self.nCr(n, i)
                subtract = choose * (p**i) * (1-p)**(n-i)
                P = P - subtract
            txt = "P(X≥" + str(x) + ") = " + format(P, ".4f")
            txt_answer = tk.Label(self.bWindow, text=txt, width=23)
            txt_answer.config(font=("Gadugi", 15), bg="white", anchor="center")
            txt_answer.place(x=5, y=105)

    def calculateBinxlexley(self):
        try:
            x = int(self.eOrPi(self.ent_binx.get())) # x in P(X<x)
            y = int(self.eOrPi(self.ent_biny.get()))
            if x < 0 or x > dist_parameters[user_graph][0] or y < 0 or y > dist_parameters[user_graph][0] or x > y:
                raise ArithmeticError
        except ArithmeticError:
            tkMessageBox.showerror("Invalid input", "This range is invalid.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            P = 0
            n = dist_parameters[user_graph][0]
            p = dist_parameters[user_graph][1]
            for i in range(x, y+1):
                choose = self.nCr(n, i)
                add = choose * (p**i) * (1-p)**(n-i)
                P = P + add
            txt = "P(" + str(x) +"≤X≤" + str(y) + ") = " + format(P, ".4f")
            txt_answer = tk.Label(self.bWindow, text=txt, width=23)
            txt_answer.config(font=("Gadugi", 15), bg="white", anchor="center")
            txt_answer.place(x=5, y=105)

    def normalDist(self):
        if distributions[user_graph] != "Normal":
            tkMessageBox.showerror("Invalid graph", "Select a normal distribution.")
        else:
            self.nWindow = tk.Tk()
            self.nWindow.title("Normal distribution")
            self.nWindow.geometry("270x150")
            txt_select = tk.Label(self.nWindow, text="Select value to find:")
            txt_select.config(font=("Gadugi", 12))
            txt_select.place(x=5, y=0)
            self.n = tk.StringVar(self.nWindow)
            self.n.set("Find")
            self.om_nor = tk.OptionMenu(self.nWindow, self.n, *self.opt_nor)
            self.om_nor.config(font=("Gadugi", 12))
            self.om_nor.place(x=5, y=25)
            self.om_nor.lift()
            btn_enter = tk.Button(self.nWindow, text="Enter", width=5, height=1, command=self.selectNormalOption)
            btn_enter.config(font=("Gadugi", 12))
            btn_enter.place(x=5, y=65)
            btn_enter.lift()

    def selectNormalOption(self):
        txt_enter = tk.Label(self.nWindow, text="Enter values:")
        txt_enter.config(font=("Gadugi", 12))
        txt_enter.place(x=160, y=0)
        option = self.n.get()
        self.ent_binx = tk.Entry(self.nWindow, width=2, font="Gadugi", justify="center")
        if option == "P(X<x)" or option == "P(X≤x)":
            txt = "P(X<     )" if option == "P(X<x)" else "P(X≤     )"
            txt_xlx = tk.Label(self.nWindow,text=txt)
            txt_xlx.config(font=("Gadugi", 13))
            txt_xlx.place(x=160, y=25)
            self.ent_binx.place(x=200, y=27)
            self.ent_binx.lift()
            btn_nor = tk.Button(self.nWindow, text="Calculate", width=8, height=1, command=self.calculateNorxlx)            
        elif option == "P(X>x)" or option == "P(X≥x)":
            txt = "P(X>     )" if option == "P(X>x)" else "P(X≥     )"
            txt_xgx = tk.Label(self.nWindow,text=txt)
            txt_xgx.config(font=("Gadugi", 13))
            txt_xgx.place(x=160, y=25)
            self.ent_binx.place(x=200, y=27)
            self.ent_binx.lift()
            btn_nor = tk.Button(self.nWindow, text="Calculate", width=8, height=1, command=self.calculateNorxgx)
        else:
            self.ent_biny = tk.Entry(self.nWindow, width=2, font="Gadugi", justify="center")
            txt_xlexley = tk.Label(self.nWindow,text="P(     <X<     )")
            txt_xlexley.config(font=("Gadugi", 13))
            txt_xlexley.place(x=160, y=25)
            self.ent_binx.place(x=180, y=27)
            self.ent_binx.lift()
            self.ent_biny.place(x=237, y=27)
            self.ent_biny.lift()
            btn_nor = tk.Button(self.nWindow, text="Calculate", width=8, height=1, command=self.calculateNorxlxly)
        btn_nor.config(font=("Gadugi", 12))
        btn_nor.place(x=160, y=65)
        btn_nor.lift()

    def calculateNorxlx(self):
        mu = dist_parameters[user_graph][0]
        sigma = dist_parameters[user_graph][1]
        try:
            x = float(self.eOrPi(self.ent_binx.get()))
            if x < math.ceil(mu) - 4*math.ceil(sigma) or x > math.ceil(mu) + 4*math.ceil(sigma):
                raise ArithmeticError
        except ArithmeticError:
            tkMessageBox.showerror("Invalid input", "This value is out of range.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            P = norm.cdf(x, mu, sigma)
            if self.n.get() == "P(X<x)":
                txt = "P(X<" + str(x) + ") = " + format(P, ".4f")
            else:
                txt = "P(X≤" + str(x) + ") = " + format(P, ".4f")
            txt_answer = tk.Label(self.nWindow, text=txt, width=23)
            txt_answer.config(font=("Gadugi", 15), bg="white", anchor="center")
            txt_answer.place(x=5, y=105)
            low = math.ceil(mu) - 4*math.ceil(sigma)
            color_range = np.arange(low, x, 0.001)
            stop = norm(mu, sigma)
            diagram.fill_between(color_range, stop.pdf(color_range), alpha=0.2)
            canvas.draw()

    def calculateNorxgx(self):
        mu = dist_parameters[user_graph][0]
        sigma = dist_parameters[user_graph][1]
        try:
            x = float(self.eOrPi(self.ent_binx.get()))
            if x < math.ceil(mu) - 4*math.ceil(sigma) or x > math.ceil(mu) + 4*math.ceil(sigma):
                raise ArithmeticError
        except ArithmeticError:
            tkMessageBox.showerror("Invalid input", "This value is out of range.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            P = 1 - norm.cdf(x, mu, sigma)
            if self.n.get() == "P(X>x)":
                txt = "P(X>" + str(x) + ") = " + format(P, ".4f")
            else:
                txt = "P(X≥" + str(x) + ") = " + format(P, ".4f")
            txt_answer = tk.Label(self.nWindow, text=txt, width=23)
            txt_answer.config(font=("Gadugi", 15), bg="white", anchor="center")
            txt_answer.place(x=5, y=105)
            high = math.ceil(mu) + 4*math.ceil(sigma)
            color_range = np.arange(x, high, 0.001)
            stop = norm(mu, sigma)
            diagram.fill_between(color_range, stop.pdf(color_range), alpha=0.2)
            canvas.draw()

    def calculateNorxlxly(self):
        mu = dist_parameters[user_graph][0]
        sigma = dist_parameters[user_graph][1]
        try:
            x = float(self.eOrPi(self.ent_binx.get()))
            y = float(self.eOrPi(self.ent_biny.get()))
            low = math.ceil(mu) - 4*math.ceil(sigma)
            high = math.ceil(mu) + 4*math.ceil(sigma)
            if x < low or x > high or y < low or y > high or x > y:
                raise ArithmeticError
        except ArithmeticError:
            tkMessageBox.showerror("Invalid input", "This range is invalid.")
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            P = norm.cdf(y, mu, sigma) - norm.cdf(x, mu, sigma)
            txt = "P(" + str(x) +"<X<" + str(y) + ") = " + format(P, ".4f")
            txt_answer = tk.Label(self.nWindow, text=txt, width=23)
            txt_answer.config(font=("Gadugi", 15), bg="white", anchor="center")
            txt_answer.place(x=5, y=105)
            X = np.arange(x, y, 0.001)
            Y = norm.pdf(X, mu, sigma)
            diagram.fill_between(X, Y, 0, alpha=0.2)
            canvas.draw()

class ThreeDimensional:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Plotter - 3D")
        self.figure = Figure(figsize = (11, 6.7))
        self.diagram = self.figure.add_subplot(111, projection="3d")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().place(x=150, y=40)
        btn_plotpoint = tk.Button(self.root, text="Plot a\npoint", width=10, height=2, command=self.point)
        btn_plotpoint.config(font=("Gadugi", 12))
        btn_plotpoint.place(x=25, y=40)
        btn_distance = tk.Button(self.root, text="Distance", width=10, height=2, command=self.distance)
        btn_distance.config(font=("Gadugi", 12))
        btn_distance.place(x=25, y=120)
        btn_drawline = tk.Button(self.root, text="Draw\nline", width=10, height=2, command=self.line)
        btn_drawline.config(font=("Gadugi", 12))
        btn_drawline.place(x=25, y=200)
        btn_annotate = tk.Button(self.root, text="Annotate\npoint", width=10, height=2, command=self.annotation)
        btn_annotate.config(font=("Gadugi", 12))
        btn_annotate.place(x=25, y=280)
        btn_setangle = tk.Button(self.root, text="Set angle\nof view", width=10, height=2, command=self.angle)
        btn_setangle.config(font=("Gadugi", 12))
        btn_setangle.place(x=25, y=360)
        btn_animate = tk.Button(self.root, text="Animate\nplot", width=10, height=2, command=self.animate)
        btn_animate.config(font=("Gadugi", 12))
        btn_animate.place(x=25, y=440)
        btn_axesnames = tk.Button(self.root, text="Change\naxes names", width=10, height=2, command=self.axesNames)
        btn_axesnames.config(font=("Gadugi", 12))
        btn_axesnames.place(x=25, y=520)
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Add graph title", command=self.graphTitle)
        filemenu.add_command(label="Save image", command=self.saveFigure)
        filemenu.add_command(label="Restart", command=self.restartProgram)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quitProgram)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

        self.pointWindow = ""
        self.distanceWindow = ""
        self.annotateWindow = ""
        self.angleWindow = ""
        self.axesWindow = ""

        self.ent_point1x = ""
        self.ent_point1y = ""
        self.ent_point1z = ""
        self.ent_point2x = ""
        self.ent_point2y = ""
        self.ent_point2z = ""

        self.ent_x = ""
        self.ent_y = ""
        self.ent_z = ""
        self.ent_text = ""

        self.var = tk.BooleanVar()
        self.var.set(False)

        self.s_el = ""
        self.s_sv = ""
        self.var1 = ""
        self.var2 = ""

        self.ent_newxname = ""
        self.ent_newyname = ""
        self.ent_newzname = ""
        
    def eOrPi(self, value):
        if value == "": return 1
        elif value == "-" : return -1
        elif value == "e": return math.e
        elif value == "-e": return -math.e
        elif value == "p" or value == "π": return math.pi
        elif value == "-p" or value == "-π": return -math.pi
        else:
            letter_pos = 0
            for digit in value:
                if digit == "e":
                    new_value = value[0:letter_pos]
                    try:
                        new_value = float(new_value) * math.e
                    except TypeError:
                        return TypeError
                    else:
                        if letter_pos < (len(value)-1):
                            return ValueError
                        else:
                            return new_value
                else:
                    letter_pos = letter_pos + 1

            letter_pos = 0
            for digit in value:
                if digit == "p" or digit == "π":
                    new_value = value[0:letter_pos]
                    try:
                        new_value = float(new_value) * math.pi
                    except TypeError:
                        return TypeError
                    else:
                        if letter_pos < (len(value)-1):
                            return ValueError
                        else:
                            return new_value
                else:
                    letter_pos = letter_pos + 1
            return value

    def point(self):
        self.pointWindow = tk.Tk()
        self.pointWindow.title("Plot a point")
        self.pointWindow.geometry("355x65")
        txt_coords = tk.Label(self.pointWindow, text="Enter the coordinates of the point:")
        txt_coords.config(font=("Gadugi", 12))
        txt_coords.place(x=5, y=5)
        txt_point = tk.Label(self.pointWindow, text="(         ,         ,         )")
        txt_point.config(font=("Gadugi", 12))
        txt_point.place(x=5, y=30)
        self.ent_pointx = tk.Entry(self.pointWindow, width=2, font="Gadugi", justify="center")
        self.ent_pointx.place(x=15, y=32)
        self.ent_pointy = tk.Entry(self.pointWindow, width=2, font="Gadugi", justify="center")
        self.ent_pointy.place(x=55, y=32)
        self.ent_pointz = tk.Entry(self.pointWindow, width=2, font="Gadugi", justify="center")
        self.ent_pointz.place(x=95, y=32)
        btn_plotpoint = tk.Button(self.pointWindow, text="Plot\npoint", width=10
                                  , height=2, command=self.plotPoint)
        btn_plotpoint.config(font=("Gadugi", 12))
        btn_plotpoint.place(x=250, y=5)

    def plotPoint(self):
        try:
            x = float(self.eOrPi(self.ent_pointx.get()))
            y = float(self.eOrPi(self.ent_pointy.get()))
            z = float(self.eOrPi(self.ent_pointz.get()))
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            self.diagram.scatter(x, y, z, marker="x", s=100, color="#2cab05")
            self.canvas.draw()

    def distance(self):
        self.distanceWindow = tk.Tk()
        self.distanceWindow.title("Distance")
        self.distanceWindow.geometry("380x140")
        txt_coords = tk.Label(self.distanceWindow, text="Enter the coordinates of the first and second points:")
        txt_coords.config(font=("Gadugi", 12))
        txt_coords.place(x=5, y=5)
        txt_point1 = tk.Label(self.distanceWindow, text="Point 1: (         ,         ,         )")
        txt_point1.config(font=("Gadugi", 12))
        txt_point1.place(x=5, y=30)
        self.ent_point1x = tk.Entry(self.distanceWindow, width=2, font="Gadugi", justify="center")
        self.ent_point1x.place(x=75, y=32)
        self.ent_point1y = tk.Entry(self.distanceWindow, width=2, font="Gadugi", justify="center")
        self.ent_point1y.place(x=115, y=32)
        self.ent_point1z = tk.Entry(self.distanceWindow, width=2, font="Gadugi", justify="center")
        self.ent_point1z.place(x=155, y=32)
        txt_point2 = tk.Label(self.distanceWindow, text="Point 2: (         ,         ,         )")
        txt_point2.config(font=("Gadugi", 12))
        txt_point2.place(x=5, y=60)
        self.ent_point2x = tk.Entry(self.distanceWindow, width=2, font="Gadugi", justify="center")
        self.ent_point2x.place(x=75, y=62)
        self.ent_point2y = tk.Entry(self.distanceWindow, width=2, font="Gadugi", justify="center")
        self.ent_point2y.place(x=115, y=62)
        self.ent_point2z = tk.Entry(self.distanceWindow, width=2, font="Gadugi", justify="center")
        self.ent_point2z.place(x=155, y=62)
        btn_distance = tk.Button(self.distanceWindow, text="Calculate\ndistance", width=10, height=2, command=self.calculateDistance)
        btn_distance.config(font=("Gadugi", 12))
        btn_distance.place(x=250, y=32)

    def calculateDistance(self):
        try:
            x1 = float(self.eOrPi(self.ent_point1x.get()))
            x2 = float(self.eOrPi(self.ent_point2x.get()))
            y1 = float(self.eOrPi(self.ent_point1y.get()))
            y2 = float(self.eOrPi(self.ent_point2y.get()))
            z1 = float(self.eOrPi(self.ent_point1z.get()))
            z2 = float(self.eOrPi(self.ent_point2z.get()))
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            distance = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
            txt = "Distance: " + format(distance, ".3f") + " (3dp)"
            txt_distance = tk.Label(self.distanceWindow, text=txt, width=33)
            txt_distance.config(font=("Gadugi", 15), bg="white", anchor="center")
            txt_distance.place(x=5, y=105)
        
    def line(self):
        self.distance()
        self.distanceWindow.title("Draw line")
        btn_line = tk.Button(self.distanceWindow, text="Draw\nline", width=10, height=2, command=self.drawLine)
        btn_line.config(font=("Gadugi", 12))
        btn_line.place(x=250, y=32)
        btn_line.lift()

    def drawLine(self):
        try:
            x1 = float(self.eOrPi(self.ent_point1x.get()))
            x2 = float(self.eOrPi(self.ent_point2x.get()))
            y1 = float(self.eOrPi(self.ent_point1y.get()))
            y2 = float(self.eOrPi(self.ent_point2y.get()))
            z1 = float(self.eOrPi(self.ent_point1z.get()))
            z2 = float(self.eOrPi(self.ent_point2z.get()))
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invaliid input", "Only real values, e and π/p can be entered.")
        else:
            x = [x1, x2]
            y = [y1, y2]
            z = [z1, z2]
            self.diagram.plot(x, y, z, color="red")
            self.canvas.draw()

    def annotation(self):
        self.annotateWindow = tk.Tk()
        self.annotateWindow.geometry("380x115")
        self.annotateWindow.title("Annotate point")
        txt_coords = tk.Label(self.annotateWindow, text="Coordinates where the text")
        txt_coords.config(font=("Gadugi", 12))
        txt_coords.place(x=5, y=5)
        txt_drawn = tk.Label(self.annotateWindow, text="should be drawn: (       ,       ,       )") 
        txt_drawn.config(font=("Gadugi", 12))
        txt_drawn.place(x=5, y=28)
        self.ent_x = tk.Entry(self.annotateWindow, width=2, font="Gadugi", justify="center")
        self.ent_x.place(x=140, y=30)
        self.ent_y = tk.Entry(self.annotateWindow, width=2, font="Gadugi", justify="center")
        self.ent_y.place(x=170, y=30)
        self.ent_z = tk.Entry(self.annotateWindow, width=2, font="Gadugi", justify="center")
        self.ent_z.place(x=200, y=30)
        txt_text = tk.Label(self.annotateWindow, text="Text for annotation: ")
        txt_text.config(font=("Gadugi", 12))
        txt_text.place(x=5, y=60)
        self.ent_text = tk.Entry(self.annotateWindow, width=25, font="Gadugi")
        self.ent_text.place(x=5, y=85)
        self.var = tk.BooleanVar(self.annotateWindow)
        self.var.set(False)
        self.cbtn_mark = tk.Checkbutton(self.annotateWindow, text="Mark point", variable=self.var)
        self.cbtn_mark.config(font=("Gadugi", 12))
        self.cbtn_mark.place(x=245, y=85)
        btn_annotate = tk.Button(self.annotateWindow, text="Annotate\npoint", width=10, height=2, command=self.annotatePoint)
        btn_annotate.config(font=("Gadugi", 12))
        btn_annotate.place(x=250, y=25)

    def annotatePoint(self):
        try:
            x = float(self.eOrPi(self.ent_x.get()))
            y = float(self.eOrPi(self.ent_y.get()))
            z = float(self.eOrPi(self.ent_z.get()))
        except TypeError:
            tkMessageBox.showerror("Invalid input", "Check digits before special characters.")
        except ValueError:
            tkMessageBox.showerror("Invalid input", "Only real values, e and π/p can be entered.")
        else:
            text = self.ent_text.get()
            point = self.diagram.scatter(x, y, z, marker="x", s=150, color="#9e7503")
            if self.var.get() == False: point.set_visible(False)
            self.diagram.text(x, y, z, text, fontsize=12)
            self.canvas.draw()

    def angle(self):
        self.angleWindow = tk.Tk()
        self.angleWindow.geometry("340x165")
        self.angleWindow.title("Set angle of view")
        txt_angle = tk.Label(self.angleWindow, text="Set angles for side view and elevation:")
        txt_angle.config(font=("Gadugi", 12))
        txt_angle.place(x=5, y=5)
        txt_el = tk.Label(self.angleWindow, text="Elevation")
        txt_el.config(font=("Gadugi", 12))
        txt_el.place(x=85, y=32)
        self.var1 = tk.DoubleVar(self.angleWindow)
        self.scale_el = tk.Scale(self.angleWindow, variable=self.var1, length=200, from_=1.0, to=90.0, orient="horizontal")
        self.scale_el.place(x=5, y=50)
        txt_sv = tk.Label(self.angleWindow, text="Side view")
        txt_sv.config(font=("Gadugi", 12))
        txt_sv.place(x=85, y=102)
        self.var2 = tk.DoubleVar(self.angleWindow)
        self.scale_sv = tk.Scale(self.angleWindow, variable=self.var2, length=200, from_=1.0, to=90.0, orient="horizontal")
        self.scale_sv.place(x=5, y=120)
        btn_angle = tk.Button(self.angleWindow, text="Set angle\nof view", width=10, height=2, command=self.changeAngle)
        btn_angle.config(font=("Gadugi", 12))
        btn_angle.place(x=230, y=60)

    def changeAngle(self):
        elevation = self.var1.get()
        side_view = self.var2.get()
        self.diagram.view_init(elevation, side_view)
        self.canvas.draw()

    def animate(self):
        for view in range(0, 90):
            self.diagram.view_init(30, view)
            self.canvas.draw()
        plt.pause(3)
        self.diagram.view_init(30, 300)
        self.canvas.draw()

    def axesNames(self):
        self.axesWindow = tk.Tk()
        self.axesWindow.title("Change axes names")
        self.axesWindow.geometry("450x90")
        txt_newxname = tk.Label(self.axesWindow, text="New x-axis name:")
        txt_newxname.config(font=("Gadugi", 12))
        txt_newxname.place(x=5, y=5)
        self.ent_newxname = tk.Entry(self.axesWindow, width=20, font="Gadugi")
        self.ent_newxname.place(x=135, y=7)
        txt_newyname = tk.Label(self.axesWindow, text="New y-axis name:")
        txt_newyname.config(font=("Gadugi", 12))
        txt_newyname.place(x=5, y=30)
        self.ent_newyname = tk.Entry(self.axesWindow, width=20, font="Gadugi")
        self.ent_newyname.place(x=135, y=32)
        txt_newzname = tk.Label(self.axesWindow, text="New z-axis name:")
        txt_newzname.config(font=("Gadugi", 12))
        txt_newzname.place(x=5, y=55)
        self.ent_newzname = tk.Entry(self.axesWindow, width=20, font="Gadugi")
        self.ent_newzname.place(x=135, y=57)
        btn_axnames = tk.Button(self.axesWindow, text="Change\naxes names", width=10, height=2, command=self.changeAxesNames)
        btn_axnames.config(font=("Gadugi", 12))
        btn_axnames.place(x=330, y=20)

    def changeAxesNames(self):
        x = self.ent_newxname.get()
        y = self.ent_newyname.get()
        z = self.ent_newzname.get()
        self.diagram.set_xlabel(x, fontsize=18)
        self.diagram.set_ylabel(y, fontsize=18)
        self.diagram.set_zlabel(z, fontsize=18)
        self.canvas.draw()

    def graphTitle(self):
        self.titleWindow = tk.Tk()
        self.titleWindow.title("Add graph title")
        self.titleWindow.geometry("305x65")
        txt_title = tk.Label(self.titleWindow, text="Title of graph:")
        txt_title.config(font=("Gadugi", 12))
        txt_title.place(x=5, y=5)
        self.ent_title = tk.Entry(self.titleWindow, width=20, font="Gadugi")
        self.ent_title.place(x=5, y=32)
        btn_title = tk.Button(self.titleWindow, text="Add title", width=10, height=2, command=self.addGraphTitle)
        btn_title.config(font=("Gadugi", 12))
        btn_title.place(x=200, y=5)

    def addGraphTitle(self):
        new_title = self.ent_title.get()
        self.diagram.set_title(new_title, fontsize=20)
        self.canvas.draw()

    def saveFigure(self):
        image = tk.filedialog.asksaveasfilename(title="Save graph", defaultextension=".png", filetypes=(("PNG Image", "*.png"), ("All Files", "*.*")))
        if image:
            self.figure.savefig(image, bbox_inches="tight")

    def restartProgram(self):
        restart = tkMessageBox.askquestion("Restart", "Are you sure you wish to restart?")
        if restart == "yes":
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    def quitProgram(self):
        sys.exit()

figure = Figure(figsize = (7, 6.5))
diagram = figure.add_subplot(111)
diagram.grid()
canvas = ""
global distributions, coefficients, points_list, last_action, graph_num, scatter_num, functions
coefficients = [[]*5 for i in range(5)]
functions = ["", "", "", "", ""]
start_fx = []
stop_fx = []
start_pt = []
stop_pt = []
start_qt = []
stop_qt = []
distributions = ["", "", "", "", ""]
dist_parameters = [[]*5 for i in range(5)]
scatterx = [[]*5 for i in range(5)]
scattery = [[]*5 for i in range(5)]
scatter_num = 0
is_window_made = False
graph_num = 0
qt_functions = ["", "", "", "", ""]
qt_coefficients = [[]*5 for i in range(5)]
pt_functions = ["", "", "", "" ""]
pt_coefficients = [[]*5 for i in range(5)]
user_graph = 0
lower_c = []
upper_c = []
lower_p = []
upper_p = []

def main():
    global window, app
    window = tk.Tk()
    window.overrideredirect(True)
    window.geometry("950x450")
    app = Design(window)
    window.mainloop()

if __name__ == "__main__":
    main()
