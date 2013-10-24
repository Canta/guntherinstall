#! /usr/bin/python
# -*- coding: utf-8 -*-

#import pysvn
import os, re
import sys, getopt
import urllib
import zipfile

def CreateInstallDir():
    iDir = ""
    iDir = "/usr/local/gunther"
    if not os.path.exists(iDir): 
        os.system("sudo mkdir augo+rw " + iDir + " && sudo chmod augo+rw "+iDir)
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

# Primero, chequeo las dependencias.
iDir = None
PythonPath = os.path.dirname(sys.executable)

try:
    import setuptools
except:
    print u"No se encontró el módulo setuptools. Es necesario descargarlo e instalarlo."
    print "sudo apt-get install python-setuptools"
    ret = os.system("sudo apt-get install python-setuptools")
    if ret != 0:
        print u"Ocurrió un error durante la instalación de setuptools."
        exit(ret)

try:
    import pysvn
except:
    print u"No se encontró el módulo pysvn. Es necesario descargarlo e instalarlo."
    print "sudo apt-get install python-svn"
    ret = os.system("sudo apt-get install python-svn")
    if ret != 0:
        print u"Ocurrió un error durante la instalación de pysvn."
        exit(ret)

try:
    import lxml.etree
except:
    print u"No se encontró el módulo lxml. Es necesario descargarlo e instalarlo."
    print "sudo apt-get install python-lxml"
    os.system("sudo apt-get install python-lxml")
    print "sudo easy_install --allow-hosts=lxml.de,*.python.org lxml==2.3"
    ret = os.system("sudo easy_install --allow-hosts=lxml.de,*.python.org lxml==2.3")
    if ret != 0:
        print u"Ocurrió un error durante la instalación de lxml."
        exit(ret)

try:
    import numpy
except:
    print u"No se encontró el módulo numpy. Es necesario descargarlo e instalarlo."
    print "sudo easy_install numpy"
    ret = os.system("sudo easy_install numpy")
        
    if ret != 0:
        print u"Ocurrió un error durante la instalación de numpy."
        exit(ret)

try:
    import PyQt4
except:
    print u"No se encontró el módulo PyQt4. Es necesario descargarlo e instalarlo."
    print "sudo apt-get install python-qt4"
    ret = os.system("sudo apt-get install python-qt4")
    if ret != 0:
        print u"Ocurrió un error durante la instalación de PyQt4."
        exit(ret)

try:
    import pyaudio
except:
    print u"No se encontró el módulo pyaudio. Es necesario descargarlo e instalarlo."
    print "sudo apt-get install python-pyaudio"
    ret = os.system("sudo apt-get install python-pyaudio")
    if ret != 0:
        print u"Ocurrió un error durante la instalación de pyaudio."
        exit(ret)

try:
    import requests
except:
    print u"No se encontró el módulo requests. Es necesario descargarlo e instalarlo."
    print "sudo apt-get install python-requests"
    ret = os.system("sudo apt-get install python-requests")
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
    print "sudo apt-get install liquidsoap"
    ret = os.system("sudo apt-get install liquidsoap")
    if ret != 0:
        print u"Ocurrió un error durante la instalación de Liquidsoap."
        exit(ret)


#Bajo Günther del repo
svnclient = pysvn.Client()
#chequeo si el directorio actual es un checkout del repo
info = None
GuntherPath = CreateInstallDir() #os.path.join(os.getcwd(), "Gunther")
print u"Path donde se instalará Günther: " + GuntherPath
if not os.path.exists(GuntherPath):
    os.makedirs(GuntherPath)
os.chdir(GuntherPath)

try:
    info = svnclient.info(GuntherPath)
except Exception as e:
    svnclient.checkout('svn://svn.code.sf.net/p/radiocefyl/code/trunk/gunther', GuntherPath)
    info = svnclient.info(GuntherPath)

#Borro cualquier cambio
svnclient.revert(GuntherPath)

#Actualizo la versión
svnclient.update(GuntherPath)

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

print "sudo chmod augo+rwx " + path
os.system("sudo chmod augo+rwx " + path)
print "sudo chmod -R augo+rw " + GuntherPath
os.system("sudo chmod -R augo+rw " + GuntherPath)

#corrijo un problema en la instalación de Liquidsoap: no tiene permisos para escribir en el log.
print "sudo chmod -R augo+rw /var/log/liquidsoap"
os.system("sudo chmod -R augo+rw /var/log/liquidsoap")

print u"Instalación finalizada."
