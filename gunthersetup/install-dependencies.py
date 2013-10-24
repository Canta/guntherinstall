#! /usr/bin/python
# -*- coding: utf-8 -*-

# -- INCLUDES -- 
import os
import sys, getopt
import urllib
import zipfile
import Tkinter, tkFileDialog
import tkMessageBox as box

try:
    #Primero declaraciones para todo el script
    iDir = None
    GuntherPath = None
    PythonPath = sys.executable.replace("python.exe","")

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

    #chequeo las dependencias.

    try:
        import setuptools
    except:
        #box.showinfo(u"Información", u"No se encontró el módulo setuptools.\nSe descargará e instalará a continuación.\nPor favor, presione OK y espere...")
        print u"No se encontró el módulo setuptools. Es necesario descargarlo e instalarlo."
        
        #tengo que bajar http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe#md5=57e1e64f6b7c7f1d2eddfc9746bbaf20
        #print u"Descargando setuptools... (http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe)"
        #urllib.urlretrieve("http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe", iDir + "setuptools-0.6c11.win32-py2.7.exe")
        ret = os.system("\""+iDir + "setuptools-0.6c11.win32-py2.7.exe"+"\"")
        
        if ret != 0:
            print u"Ocurrió un error durante la instalación de setuptools."
            box.showerror(u"Error", u"Ocurrió un error durante la instalación de setuptools.\nImposible continuar.\nIntente ejecutando la instalación nuevamente.")
            f.write("Error: instalación de setuptools.")
            exit(ret)

    try:
        import git
    except:
        print u"No se encontró el módulo GitPython. Es necesario descargarlo e instalarlo."
        #box.showinfo(u"Información", u"No se encontró el módulo pysvn.\nSe descargará e instalará a continuación.\nPor favor, presione OK y espere...")
        #print u"Descargando pysvn... (http://pysvn.tigris.org/files/documents/1233/49177/py27-pysvn-svn173-1.7.6-1457.exe)"
        #urllib.urlretrieve("http://pysvn.tigris.org/files/documents/1233/49177/py27-pysvn-svn173-1.7.6-1457.exe", iDir + "py27-pysvn-svn173-1.7.6-1457.exe")
        #ret = os.system("\""+iDir + "py27-pysvn-svn173-1.7.6-1457.exe"+"\"")
        ret = os.system(PythonPath + "\\Scripts\\easy_install.exe gitpython")
            
        if ret != 0:
            print u"Ocurrió un error durante la instalación de GitPython."
            box.showerror(u"Error", u"Ocurrió un error durante la instalación de GitPython.\nImposible continuar.\nIntente ejecutando la instalación nuevamente.")
            f.write("Error: instalación de gitpython.")
            exit(ret)

    try:
        import lxml.etree
    except:
        print u"No se encontró el módulo lxml. Es necesario descargarlo e instalarlo."
        #box.showinfo(u"Información", u"No se encontró el módulo lxml.\nSe descargará e instalará a continuación.\nPor favor, presione OK y espere...")
        ##easy_install --allow-hosts=lxml.de,*.python.org lxml==2.3
        ret = os.system(PythonPath + "\\Scripts\\easy_install.exe --allow-hosts=lxml.de,*.python.org lxml==2.3")
            
        if ret != 0:
            print u"Ocurrió un error durante la instalación de lxml."
            box.showerror(u"Error", u"Ocurrió un error durante la instalación de lxml.\nImposible continuar.\nIntente ejecutando la instalación nuevamente.")
            f.write("Error: instalación de lxml.")
            exit(ret)

    try:
        import requests
    except:
        print u"No se encontró el módulo requests. Es necesario descargarlo e instalarlo."
        #box.showinfo(u"Información", u"No se encontró el módulo requests.\nSe descargará e instalará a continuación.\nPor favor, presione OK y espere...")
        ret = os.system(PythonPath + "\\Scripts\\easy_install.exe requests")
            
        if ret != 0:
            print u"Ocurrió un error durante la instalación de requests."
            box.showerror(u"Error", u"Ocurrió un error durante la instalación de requests.\nImposible continuar.\nIntente ejecutando la instalación nuevamente.")
            f.write("Error: instalación de requests.")
            exit(ret)

    try:
        import numpy
    except:
        print u"No se encontró el módulo numpy. Es necesario descargarlo e instalarlo."
        #box.showinfo(u"Información", u"No se encontró el módulo numpy.\nSe descargará e instalará a continuación.\nPor favor, presione OK y espere...")
        ret = os.system(PythonPath + "\\Scripts\\easy_install.exe numpy")
            
        if ret != 0:
            print u"Ocurrió un error durante la instalación de numpy."
            box.showerror(u"Error", u"Ocurrió un error durante la instalación de numpy.\nImposible continuar.\nIntente ejecutando la instalación nuevamente.")
            f.write("Error: instalación de numpy.")
            exit(ret)

    try:
        import PyQt4
    except:
        print u"No se encontró el módulo PyQt4. Es necesario descargarlo e instalarlo."
        #box.showinfo(u"Información", u"No se encontró el módulo PyQt4.\nSe descargará e instalará a continuación.\nPor favor, presione OK y espere...")
        print u"Instalando PyQt4... (http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.9.4/PyQt-Py2.7-x86-gpl-4.9.4-1.exe)"
        #urllib.urlretrieve("http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.9.4/PyQt-Py2.7-x86-gpl-4.9.4-1.exe", iDir + "PyQt-Py2.7-x86-gpl-4.9.4-1.exe")
        ret = os.system("\""+iDir + "PyQt-Py2.7-x86-gpl-4.9.4-1.exe"+"\"")
        
        if ret != 0:
            print u"Ocurrió un error durante la instalación de PyQt4."
            box.showerror(u"Error", u"Ocurrió un error durante la instalación de PyQt4.\nImposible continuar.\nIntente ejecutando la instalación nuevamente.")
            f.write("Error: instalación de pyqt4.")
            exit(ret)

    try:
        import pyaudio
    except:
        print u"No se encontró el módulo pyaudio. Es necesario descargarlo e instalarlo."
        #box.showinfo(u"Información", u"No se encontró el módulo pyaudio.\nSe descargará e instalará a continuación.\nPor favor, presione OK y espere...")
        
        print "Instalando pyaudio... (http://people.csail.mit.edu/hubert/pyaudio/packages/pyaudio-0.2.4.py27.exe)"
        #urllib.urlretrieve("http://people.csail.mit.edu/hubert/pyaudio/packages/pyaudio-0.2.4.py27.exe", iDir + "pyaudio-0.2.4.py27.exe")
        ret = os.system("\""+iDir + "pyaudio-0.2.4.py27.exe"+"\"")
            
        if ret != 0:
            print u"Ocurrió un error durante la instalación de pyaudio."
            box.showerror(u"Error", u"Ocurrió un error durante la instalación de pyaudio.\nImposible continuar.\nIntente ejecutando la instalación nuevamente.")
            f.write("Error: instalación de pyaudio.")
            exit(ret)


    #ahora busco Liquidsoap
    directorio = None

    if os.path.exists("c:\\liquidsoap\\liquidsoap.exe"):
        directorio = "c:\\liquidsoap"
    for path in os.environ.get('PATH', '').split(';'):
        if os.path.exists(os.path.join(path, "liquidsoap.exe")) and not os.path.isdir(os.path.join(path, "liquidsoap.exe")):
            directorio = path

    if directorio == None:
        print u"No se encontró el Liquidsoap. Es necesario descargarlo e instalarlo."
        #box.showinfo(u"Información", u"No se encontró Liquidsoap.\nSe descargará e instalará a continuación.\nPor favor, presione OK y espere...")
        
        print u"descargando liquidsoap... (http://downloads.sourceforge.net/project/savonet/liquidsoap/1.1.0/liquidsoap-1.1.0-win32-beta5.zip?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fsavonet%2Ffiles%2Fliquidsoap%2F1.1.0%2F&ts=1365446377&use_mirror=ufpr)"
        #urllib.urlretrieve("http://downloads.sourceforge.net/project/savonet/liquidsoap/1.1.0/liquidsoap-1.1.0-win32-beta5.zip?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fsavonet%2Ffiles%2Fliquidsoap%2F1.1.0%2F&ts=1365446377&use_mirror=ufpr", iDir + "liquidsoap.zip")
        #ret = os.system("\""+iDir + "liquidsoap.zip"+"\"")
        if not os.path.exists("C:\\liquidsoap\\"):
            os.makedirs("C:\\liquidsoap")
        zipy = zipfile.ZipFile(os.path.dirname(sys.argv[0]) + "\\liquidsoap.zip")
        zipy.extractall("C:\\liquidsoap\\")
        ret = os.system("xcopy /s /e /h c:\\liquidsoap\\liquidsoap-win32\\*.* C:\\liquidsoap\\")
        os.environ["PATH"] = os.environ["PATH"] + ";C:\\liquidsoap\\"
                
        if ret != 0:
            print u"Ocurrió un error durante la instalación de Liquidsoap."
            box.showerror(u"Error", u"Ocurrió un error durante la instalación de Liquidsoap.\nImposible continuar.\nIntente ejecutando la instalación nuevamente.")
            f.write("Error: instalación de liquidsoap.")
            exit(ret)
    print("Dependencias instaladas correctamente")
    exit(0)
except Exception as general:
    print(general)
    raw_input("Presione enter para continuar")
    exit(1)
