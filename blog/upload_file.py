import json
import os
from urllib import quote
from django.http import HttpResponse
import tools.webTools as tools
from ueditor.models import attachment
from django.views.decorators.csrf import csrf_exempt
import random
from models import BlogPost
import dazhu.settings
import account.secu as secu

def convert_name_html_valid(input_name):
    file_name = os.path.split(input_name)
    file_name_arr = os.path.splitext(file_name[1])
    quote_name_arr = [quote(x) for x in file_name_arr]
    quote_name_arr[0] = "%s_%s" % (quote_name_arr[0], random.randint(1, 99))
    return quote_name_arr[0] + quote_name_arr[1]

@csrf_exempt
@secu.login_filter
def upload_files(request):
    class _Result(object):
        def __init__(self):
            self.success = 0
            self.message = ""
            self.url = ""
        def tojson(self):
            return json.dumps(self.__dict__)

    ret = _Result()
    aid = request.GET["aid"]
    tools.debug("upload_files guid", aid)

    fileObj = request.FILES.get('editormd-image-file')
    tools.debug("upload_files fileObj {}".format(fileObj.chunks()))
    source_filename = fileObj.name.encode("utf8")  
    rnd_file_name = convert_name_html_valid(source_filename)
    tools.debug("upload_files file_name {}".format(rnd_file_name))
    try:
        blog = BlogPost.objects.get(guid=aid)
    except Exception as errors:
        ret.message = "target blog isnt exist {}".format(errors)
        return HttpResponse(ret.tojson())

    tempAttachment = attachment()
    tempAttachment.blog = blog
    tempAttachment.sourceName = source_filename
    tempAttachment.rndName = rnd_file_name      
    tempAttachment.save()

    upload_folder = dazhu.settings.BASE_DIR + "/dazhu/static/upload/"        
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file_path = str(upload_folder + rnd_file_name)

    try:
        with open(file_path, 'wb+') as f:
            for chunk in fileObj.chunks():
                f.write(chunk)
    except Exception as errors:
        ret.message = "write file error {}".format(errors)
        return HttpResponse(ret.tojson())
    
    ret.success = 1
    ret.url = "/static/upload/"+rnd_file_name
        
    return HttpResponse(ret.tojson())

def get_attachment(request):
    aid = request.GET["aid"]
    attachment_list = BlogPost.objects.get(guid=aid).attachment_set.all()
    ret = []
    for attachment in attachment_list:
        ret.append({"rndName":attachment.rndName,"sourceName":attachment.sourceName})        
    return HttpResponse(json.dumps(ret))

            
    