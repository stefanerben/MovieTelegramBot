
from genericpath import isfile
from json import loads as loadJson, dump as dumpJson, load, dump
from io import open as openFile

def loadFileFromCache(name):
    print("[CACHE] [LOAD]", name)
    return jsonload('cache/' + name)

def saveFileToCache(name, data):
    jsonsave('cache/' + name, data)
    print("[CACHE] [SAVE]", name)

def jsonload(jsonpath):
    with openFile(jsonpath, 'r', encoding='utf8') as data_file:
            json_data = data_file.read()
            data = loadJson(json_data)
    return data

def jsonsave(jsonpath, data, sortkeys=False):
    with openFile(jsonpath, 'w', encoding='utf-8') as outfile:
        dumpJson(data, outfile, sort_keys=sortkeys, indent=4)

def doesCachedFileExist(name):
    return isfile('cache/' + name)