#! /usr/bin/python
# -*- coding: utf-8 -*-

# -- INCLUDES -- 
import os
import sys, getopt
import urllib
import zipfile
import Tkinter, tkFileDialog
import tkMessageBox as box
import shutil

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

# -- PROGRAMA --

if os.path.exists(os.path.dirname(sys.argv[0]) + "\\installed.txt"):
    raw_input(u"Günther instalado correctamente. Presione una enter para continuar...")
    exit(0)

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

    try:
        if os.path.exists(GuntherPath):
            shutil.rmtree(GuntherPath)
        if not os.path.exists(GuntherPath):
            os.makedirs(GuntherPath)
    except Exception as e:
        print(e)
        raw_input('Press enter to continue . . .')

    # Primero, chequeo las dependencias.

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

    #---------------------
    #Bajo Günther del repo
    #---------------------

    #chequeo si el directorio actual es un checkout del repo
    info = None
    print u"Path donde se instalará Günther: " + GuntherPath
    print u"Normalizado: " + os.path.normpath(GuntherPath)
    if not os.path.exists(GuntherPath):
        os.makedirs(GuntherPath)
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

    #----------------------------------------------------------
    #Y ahora guardo el resto de las configuraciones en Windows.
    #----------------------------------------------------------
    ConfigError = []
    print "Guardando configuraciones en el registro de Windows..."
    import _winreg
    print "...el path de Python..."
    try:
        windir = os.environ.get("WINDIR")
        HKLM = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
        rama = _winreg.OpenKey(HKLM, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",0,_winreg.KEY_READ) 
        path = _winreg.QueryValueEx(rama, "Path")
        path = path[0] + r";"+PythonPath+";"+PythonPath+"\Scripts\;C:\liquidsoap\;"+GuntherPath+";"+windir+";"+windir+"\system32;"
        rama = _winreg.OpenKey(HKLM, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",0,_winreg.KEY_WRITE) 
        _winreg.SetValueEx(rama,"Path",0, _winreg.REG_SZ, path)
        _winreg.CloseKey(rama)
        _winreg.CloseKey(HKLM)
        print "...ok..."
    except:
        print "...error..."
        ConfigError.append(u"Registrar el path de Python en el registro de Windows para las sesiones de DOS automatizadas.")
        pass

    print u"...el tipo de archivos de Günther..."
    try:
        EXT, EXT_TYPE = ".gun", "Gunther.transmision"
        EXE_PATH = "c:\\gunther.bat"
        extCmd = '"%s" "%%L" %%*' % EXE_PATH
        assert os.system('assoc %s=%s' % (EXT, EXT_TYPE))==0
        assert os.system('ftype %s=%s' % (EXT_TYPE, extCmd))==0
        print "...ok..."
    except:
        print "...error..."
        ConfigError.append(u"Registrar en el registro de Windows el tipo de archivos de Günther.")
        pass
    print u"...el ícono para los archivos de Günther..."
    try:
        ICON_PATH = GuntherPath+"\\gunther.ico"
        ext = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, EXT_TYPE)
        _winreg.SetValue(ext, "DefaultIcon", _winreg.REG_SZ, ICON_PATH)
        _winreg.CloseKey(ext)
        print "...ok."
    except:
        print "...error..."
        ConfigError.append(u"Registrar el ícono para los tipos de archivos de Günther.")
        pass


    #Creo el bat para Günther
    print u"...Creo el .bat Günther..."
    try:
        tmp = "@echo off\r\ncd \""+GuntherPath+"\" \r\n"
        tmp = tmp + PythonPath + "python.exe \"" + GuntherPath + "\\GuntherLauncher.py\" \"\"%1 \r\n"
        path = "c:\\gunther.bat"
        f = open(path, "w")
        print>>f, tmp
        f.close()
        print "...ok..."
    except:
        print "...error..."
        ConfigError.append(u"Creando el archivo .bat para los tipos de archivo de Günther.")
        pass

    #Creo el shortcut
    print u"...Creo el shortcut en el escritorio..."
    try:
        tmp = "[InternetShortcut]\r\n"
        tmp = tmp + "URL=file:///c:\\gunther.bat\r\n"
        tmp = tmp + "WorkingDirectory="+GuntherPath+"\\\r\n"
        tmp = tmp + "IconIndex=0\r\n"
        tmp = tmp + r"IconFile="+GuntherPath+"\gunther.ico"
        
        #Quick Launch
        path = os.environ.get("APPDATA")
        path = path + r"\Microsoft\Internet Explorer\Quick Launch\Gunther.url"
        f = open(path, "w")
        print>>f, tmp
        f.close()

        #Escritorio
        path = os.environ.get("HOMEPATH")
        if os.path.exists(path + r"\Escritorio"): 
            path = path + r"\Escritorio"
        elif os.path.exists(path + r"\Desktop"): 
            path = path + r"\Desktop"

        path = path + r"\Gunther.url"
        f = open(path, "w")
        print>>f, tmp
        f.close()
        
        print "...ok"
    except:
        print "...error."
        ConfigError.append(u"Creando el shortcut para Günther en el escritorio.")
        pass

    if len(ConfigError) > 0:
        ConfigStr = u"\n".join(ConfigError)
        box.showwarning(u"Información", u"La instalación de Günther finalizó, pero se detectaron errores intentando realizar las siguientes acciones:\n\n"+ConfigStr+u"\n\n\nRevise que su configuración de seguridad no esté bloqueando la instalación, y luego pruebe ejecutar nuevamente GüntherInstall.")
    else:
        t = open(os.path.dirname(sys.argv[0]) + "\\installed.txt","w")
        t.write("instalado ok")
        t.close()
        box.showinfo(u"Información", u"¡Instalación finalizada!\n:D")

    log.close()
    exit(0)
except Exception as general:
    print(general)
    raw_input("Presione una tecla para continuar...")
    exit(1)
