# coding:utf-8
from django.template import loader, Context
from django.http import HttpResponse
import json
import dazhu.settings
import datetime
try:
    import Image
except:
    from PIL import Image
from urllib import quote
from django.views.decorators.csrf import csrf_exempt

import tools.webTools as tools
from blog.models import BlogPost
import  os
import fileconfig
from models import attachment
import account.secu as secu

@csrf_exempt
@secu.login_filter
def controller(request):
    if request.method == "POST":
        if request.GET['action'] == 'uploadfile':
            return ueditor_FileUp(request)
        if request.GET['action'] == 'uploadimage':
            return ueditor_ImgUp(request) 
    else:        
        try:            
            if request.GET['action'] == 'config':            
                return HttpResponse(fileconfig.configstr())
            if request.GET['action'] == 'listimage' or request.GET['action'] == 'listfile':                
                return file_list(request.GET['action'], request.GET['aid']) 
            if request.GET['action'] == 'deletefile':   
                #print(request.GET)
                return delete_file(request.GET['filename'])        
            
        except Exception as err: 
            print("error is :", err) 
    return HttpResponse("hello")



def uploadfile(fileObj, source_filename, aid):        
    """ 一个公用的上传文件的处理 """
    class myrespones(object):
        def __init__(self):
            self.filename = ""
            self.real_url = ""
            self.state = u"未知错误"
            self.error = ""
            
        def getRespones(self):
            return  "{\"original\":\"%s\",\"url\":\"%s\",\"title\":\"%s\",\"state\":\"%s\",\"error\":\"%s\"}" \
            % (self.filename, self.real_url, self.filename, self.state, quote(self.error))
        
    result = myrespones()
    
    if isinstance(aid, basestring):
        if aid == "":
            result.state = u"未知错误"
            return result.getResponse()
    else:
        result.state = u"未知错误"
        return result.getResponse()
    
    if fileObj:        
        filename = quote(fileObj.name.encode("utf8"))
        fileExt = ""
        fileInfo = []
        if "." in filename:            
            fileInfo = filename.split('.')
            fileExt = fileInfo[len(fileInfo) - 1]
            fileExt = '.' + fileExt
            tools.debug("fileext is " + fileExt)
            
        file_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        result.filename = source_filename
        
        subfolder = dazhu.settings.BASE_DIR + "/dazhu/static/upload/"
        
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)
        filePath = str(subfolder + '/' + file_name + fileExt)
        
        allowExt = None
        configJson = fileconfig.configJson()
        try:
            allowExt = configJson["fileAllowFiles"]
        except Exception as errors:
            tools.debug("json load file types error")
            tools.debug(errors)
            result.state = u"参数不正确"
        if allowExt == None:
            result.state = u"参数不正确"
            tools.debug("不能获取 file types")
            return result.getResponse()
        
        if fileExt.lower() in allowExt:        
            try:
                destination = open(filePath, 'wb+')
                for chunk in fileObj.chunks():
                    destination.write(chunk)            
                destination.close()
                
                tools.debug(configJson["imageManagerAllowFiles"])
                if fileExt.lower() in configJson["imageManagerAllowFiles"]:
                    im = Image.open(filePath)
                    im.thumbnail((1280, 1280))
                    im.save(filePath)
                    
                # 保存数据
                try:
                    blog = BlogPost.objects.get(guid=aid)
                    tempAttachment = attachment()
                    tempAttachment.blog = blog
                    tempAttachment.sourceName = source_filename
                    tempAttachment.rndName = file_name + fileExt                
                    tempAttachment.save()
                except Exception as errors:
                    result.state = u"未知错误"
                    tools.debug(errors)
                    return result.getRespones()
                real_url = 'static/upload/' + file_name + fileExt      
                result.real_url = real_url
                result.state = "SUCCESS"
                result.error = ""
            # print("real url", real_url)
            except Exception as aerror:                
                result.state = u"未知错误"
                tools.debug(aerror)
                return result.getRespones()
        else:
            result.state = u"参数不正确"       
    return result.getRespones()


def ueditor_FileUp(request):
    """ 上传文件 """  
    source_filename = request.POST.get('name', '')    
    # print("request aid is ",request.POST['aid'])
    fileObj = request.FILES.get('upfile')  
    response = HttpResponse()  
    myresponse = uploadfile(fileObj, source_filename, request.POST['aid'])
    # print("respones:", myresponse)
    response.write(myresponse)
    return response


@csrf_exempt
def ueditor_ImgUp(request):
    """ 上传图片 """      
    source_filename = request.POST.get('fileName', '')  
    fileObj = request.FILES.get('upfile', None)  
    response = HttpResponse()  
    myresponse = uploadfile(fileObj, source_filename, request.POST['aid'])
    response.write(myresponse)
    return response


def file_list(listtype, aid):    
    response = HttpResponse()
    
    class result(object):
        def __init__(self):
            self.state = "SUCCESS"
            self.list = []
            self.start = 0
            self.size = 0
            self.total = 0
        
        def setList(self, filelist):
            for item in filelist:
                if listtype == "listimage":
                    tools.debug("listtype is ",listtype,item)
                    ext = (os.path.splitext(item.rndName)[1]).lower()
                    tools.debug("upload ext is ",ext)
                    exts = ['.jpg', '.bmp', '.png', '.jpeg']
                    if ext not in exts:
                        continue                    
                tempItem = {'url':"static/upload/" + os.path.basename(item.rndName), 'title':item.sourceName}
                self.list.append(tempItem)
    
    filelist = BlogPost.objects.get(guid=aid).attachment_set.all()
    tools.debug("get filelist over")
    myresponse = result()
    myresponse.setList(filelist)
    myresponse.start = 0
    myresponse.total = len(filelist)
    myresponse.size = len(filelist)
    m = json.dumps(myresponse.__dict__, ensure_ascii=False)
    response.write(m)
    return response


def delete_file(filename):
    try:
        tools.debug("delete file :")
        tools.debug(filename)
        
        filename = os.path.basename(filename)        
        
        tempFile = attachment.objects.get(rndName = filename)
        tempFile.delete()       
        return HttpResponse("true")
    except Exception as err: 
            tools.debug("error is :", err)

