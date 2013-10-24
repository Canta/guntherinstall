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

    #----------------------------------------------------------
    #Y ahora guardo el resto de las configuraciones en Windows.
    #----------------------------------------------------------
    ConfigError = []
    print "Guardando configuraciones en el registro de Windows..."
    import _winreg
    print "...el path de Python..."
    
    try:
        windir = os.environ.get("WINDIR")
        pf = os.environ.get("PROGRAMFILES")
        HKLM = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
        rama = _winreg.OpenKey(HKLM, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",0,_winreg.KEY_READ) 
        path = _winreg.QueryValueEx(rama, "Path")
        added = ";\""+pf+"\\Git\\bin\";" + PythonPath + ";" + PythonPath+"Scripts\\;C:\\liquidsoap\\;" + GuntherPath + ";" + windir + ";" + windir + "\\system32;"
        if not added in path[0]:
            path = path[0] + added
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
    exit(0)
except Exception as general:
    print(general)
    raw_input("Presione enter para continuar")
    exit(1)
