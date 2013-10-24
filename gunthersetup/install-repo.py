#! /usr/bin/python
# -*- coding: utf-8 -*-

# -- INCLUDES -- 
import os
import sys, getopt
import urllib
import zipfile
import Tkinter, tkFileDialog
import tkMessageBox as box

# -- FUNCIONES -- 
def SelectDir(root):
    gDir = ""
    tmp1 = os.getcwd()
    gDir = tkFileDialog.askdirectory(parent=root,initialdir=tmp1,title=u'Seleccione dónde crear la carpeta de Günther:')
    
    return gDir

def CreateInstallDir(root, gDir):
    iDir = gDir + "\\install\\"
    if not os.path.exists(iDir): 
        os.makedirs(iDir)
    return iDir

try:
    #Primero declaraciones para todo el script
    iDir = None
    GuntherPath = None
    PythonPath = sys.executable.replace("python.exe","")
    log = open("log.txt","a")

    #Creo una instancia de TK, para la UI de GüntherInstall.
    root = Tkinter.Tk()
    root.withdraw()

    #Es necesario seleccionar un path para Günther
    #GuntherPath = SelectDir(root)
    GuntherPath = "c:\\"
    if str(GuntherPath) == "":
        box.showerror("Error", "No se puede continuar sin seleccionar un directorio para instalar el programa.")
        f.write("Error: No se puede continuar sin seleccionar un directorio de instalación.")
        exit(0)

    GuntherPath = GuntherPath.replace("/","\\") + "\\Gunther"
    iDir = os.path.dirname(sys.argv[0]) + "\\" # = CreateInstallDir(root, GuntherPath)
    
    #---------------------
    #Bajo Günther del repo
    #---------------------

    #chequeo si el directorio actual es un checkout del repo
    info = None
    print u"Path donde se instalará Günther: " + GuntherPath
    print u"Normalizado: " + os.path.normpath(GuntherPath)
    if not os.path.exists(GuntherPath):
        os.makedirs(GuntherPath)
    if not os.environ.get("PROGRAMFILES") + "\\Git\\bin" in os.environ.get("PATH"):
        os.environ["PATH"] = os.environ.get("PATH") + ";" + os.environ.get("PROGRAMFILES") + "\\Git\\bin"
    os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = os.environ.get("PROGRAMFILES")+"\\Git\\bin\\git.exe"
    os.chdir(os.path.normpath(GuntherPath))
    try:
        import git
        print u"Estableciendo " + GuntherPath + " como repo..."
        g = git.cmd.Git(".")
        print u"Clonando el repo desde github..."
        g.clone("https://github.com/Canta/gunther", ".")
        print u"Obteniendo un status..."
        repo = git.Repo(".")
        info = repo.git.status("--porcelain")
    except Exception as e:
        print(e)
        print u"Error al intentar clonar el repositorio."
        print u"Probablemente se trate de las dependencias recién instaladas."
        print u"Pruebe volviendo a ejecutar el script"
        raw_input("Presione enter para continuar...")
        exit(1)
    print("Repo instalado correctamente")
    exit(0)
except Exception as general:
    print(general)
    raw_input("Presione una tecla para continuar...")
    exit(1)
