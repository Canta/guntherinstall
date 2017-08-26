#! /usr/bin/python
# -*- coding: utf-8 -*-

#import pysvn
import os, re
import sys, getopt
import urllib
import zipfile

if os.geteuid() != 0:
    exit("Tenés que ejecutar este comando con sudo. Es decir, con permisos de root. Sino no puede instalar los componentes de Günther.\nImposible continuar.")

#FUNCIONES

def CreateInstallDir():
    iDir = ""
    iDir = "/usr/local/gunther"
    if not os.path.exists(iDir): 
        os.system("mkdir augo+rw " + iDir + " && chmod augo+rw "+iDir)
    return iDir


def get_desktop_path():
    D_paths = list()
    try:
        fs = open(os.sep.join((os.path.expanduser("~"), ".config", "user-dirs.dirs")),'r')
        data = fs.read()
        fs.close()
    except:
        data = ""

    D_paths = re.findall(r'XDG_DESKTOP_DIR=\"([^\"]*)', data)

    if len(D_paths) == 1:
        D_path = D_paths[0]
        D_path = re.sub(r'\$HOME', os.path.expanduser("~"), D_path)

    else:
        D_path = os.sep.join((os.path.expanduser("~"), 'Desktop'))

    if os.path.isdir(D_path):
        return D_path
    else:
        return None

def query_si_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"si":True,   "s":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [s/n] "
    elif default == "yes":
        prompt = " [S/n] "
    elif default == "no":
        prompt = " [s/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Por favor, responda 'si' o 'no' "\
                             "(o 's' o 'n' en su defecto).\n")


#PROGRAMA

# Primero, chequeo las dependencias.
iDir = None
PythonPath = os.path.dirname(sys.executable)

try:
    import setuptools
except:
    print u"No se encontró el módulo setuptools. Es necesario descargarlo e instalarlo."
    print "apt-get -y install python-setuptools"
    ret = os.system("apt-get -y install python-setuptools")
    if ret != 0:
        print u"Ocurrió un error durante la instalación de setuptools."
        exit(ret)

try:
    import pip
except:
    print u"No se encontró el módulo pip. Es necesario descargarlo e instalarlo."
    print "apt-get -y install python-pip"
    ret = os.system("apt-get -y install python-pip")
    if ret != 0:
        print u"Ocurrió un error durante la instalación de setuptools."
        exit(ret)

try:
    import git
except:
    print u"No se encontró el módulo gitpython. Es necesario descargarlo e instalarlo."
    print "apt-get -y install git"
    ret = os.system("apt-get -y install git")
    if ret != 0:
        print u"Ocurrió un error durante la instalación de git."
        exit(ret)
    print "pip install gitpython"
    ret = os.system("pip install gitpython")
    if ret != 0:
        print u"Ocurrió un error durante la instalación de gitpython."
        exit(ret)

try:
    import lxml.etree
except:
    print u"No se encontró el módulo lxml. Es necesario descargarlo e instalarlo."
    print "apt-get -y install python-lxml"
    os.system("apt-get -y install python-lxml")
    print "easy_install --allow-hosts=lxml.de,*.python.org lxml==2.3"
    ret = os.system("easy_install --allow-hosts=lxml.de,*.python.org lxml==2.3")
    if ret != 0:
        print u"Ocurrió un error durante la instalación de lxml."
        exit(ret)

try:
    import numpy
except:
    print u"No se encontró el módulo numpy. Es necesario descargarlo e instalarlo."
    print "pip install numpy"
    ret = os.system("pip install numpy")
        
    if ret != 0:
        print u"Ocurrió un error durante la instalación de numpy."
        exit(ret)

try:
    import PyQt4
except:
    print u"No se encontró el módulo PyQt4. Es necesario descargarlo e instalarlo."
    print "apt-get -y install python-qt4"
    ret = os.system("apt-get -y install python-qt4")
    if ret != 0:
        print u"Ocurrió un error durante la instalación de PyQt4."
        exit(ret)

try:
    import requests
except:
    print u"No se encontró el módulo requests. Es necesario descargarlo e instalarlo."
    print "pip install requests"
    ret = os.system("pip install requests")
    if ret != 0:
        print u"Ocurrió un error durante la instalación de requests."
        exit(ret)

#ahora busco Liquidsoap
directorio = None
for path in os.environ.get('PATH', '').split(':'):
    if os.path.exists(os.path.join(path, "liquidsoap")) and not os.path.isdir(os.path.join(path, "liquidsoap")):
        directorio = path
if directorio == None:
    print u"No se encontró el Liquidsoap. Es necesario descargarlo e instalarlo."
    print "apt-get -y install liquidsoap python-pyaudio python-simplejson"
    ret = os.system("apt-get -y install liquidsoap python-pyaudio python-simplejson")
    if ret != 0:
        print u"Ocurrió un error durante la instalación de Liquidsoap."
        exit(ret)


#Bajo Günther del repo
#chequeo si el directorio actual es un checkout del repo
info = None
GuntherPath = CreateInstallDir() #os.path.join(os.getcwd(), "Gunther")
print u"Path donde se instalará Günther: " + GuntherPath
if os.path.exists(GuntherPath):
    if query_si_no("Ya existe el directorio de Günther("+GuntherPath+").\n¿Desea eliminarlo para instalar nuevamente el programa?\nATENCIÓN: ESTA ACCIÓN NO PUEDE DESHACERSE\nSi tiene información guardada en ese directorio, copiela primero a otro directorio y recién entonces escriba 'si'.","no"):
        print("Borrando "+GuntherPath+"...")
        os.system("rm -r \""+GuntherPath+"\"")
        print(GuntherPath+" borrado con éxito.")
    else:
        exit("Instalación cancelada.")
print("Creando "+GuntherPath+"...")
os.makedirs(GuntherPath)
os.chdir(GuntherPath)

print("Clonando el repositorio de Günther...")
ret = os.system("git clone https://github.com/Canta/gunther .")
if ret != 0:
    print("Error al intentar clonar el repositorio de Günther")
    exit(ret)

tmp = "#!/usr/bin/env xdg-open\n\n"
tmp = tmp + "[Desktop Entry]\n"
tmp = tmp + "Version=1.0\n"
tmp = tmp + "Type=Application\n"
tmp = tmp + "Terminal=true\n"
tmp = tmp + "Path="+GuntherPath.replace(" ","\\ ")+"\n"
tmp = tmp + "Exec=python "+GuntherPath.replace(" ","\\ ")+"/GuntherLauncher.py\n"
tmp = tmp + "Name=Günther\n"
tmp = tmp + "Icon="+GuntherPath.replace(" ","\\ ")+"/gunther.png\n"

path = get_desktop_path() + "/Gunther.desktop"
f = open(path, "w")
print>>f, tmp
f.close()

print "chmod augo+rwx " + path
os.system("chmod augo+rwx " + path)
print "chmod -R augo+rw " + GuntherPath
os.system("chmod -R augo+rw " + GuntherPath)

#corrijo un problema en la instalación de Liquidsoap: no tiene permisos para escribir en el log.
print "chmod -R augo+rw /var/log/liquidsoap"
os.system("chmod -R augo+rw /var/log/liquidsoap")

print u"Instalación finalizada."
