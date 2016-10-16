import tools.webTools as tools
import dazhu
import json
def configstr():
    fileData = tools.readFile(dazhu.settings.BASE_DIR + "/dazhu/static/ueditor/net/config.json")
    return  fileData

def configJson():
    return json.loads(configstr())