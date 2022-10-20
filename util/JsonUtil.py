import json


# 从配置文件读取JSON，转换为python字典
def readJson(jsonPath):
    f = open(jsonPath, 'r', encoding='UTF-8')
    data = json.load(f)
    f.close()
    return data


# 读取用户选项 json
def getJsonUserOption():
    jsonPath = __file__ + "\\..\\..\\config\\UserOption.json"
    jsonDict = readJson(jsonPath)
    for (k, v) in jsonDict.items():
        jsonDict[k] = v.strip()
    return jsonDict


# 读取 selectors json
def getJsonSelectors():
    file = __file__ + "\\..\\..\\config\\CssSelector.json"
    return readJson(file)
