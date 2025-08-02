import json


def getRec():
    with open('recipe.json', 'r', encoding='utf-8') as file:
        return json.load(file)
    

def setRec(rec):
    with open('recipe.json', 'w', encoding='utf-8') as file:
        json.dump(rec, file, indent=4, ensure_ascii=False)


def getLog():
    with open('log.json', 'r', encoding='utf-8') as file:
        return json.load(file)
    

def setLog(Log):
    with open('log.json', 'w', encoding='utf-8') as file:
        json.dump(Log, file, indent=4, ensure_ascii=False)
