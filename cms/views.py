from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from models import CmsItem
import tools.webTools as tools

def cms(request,tempCms):
    context = {}
    context['title'] = tempCms.title
    context['contentData'] = tempCms.contentData

    return render(request, 'cms/index.html', context)

def controller(request, *args):
    path = request.path
    tempPathArr = path.split("/")

    ctl = tempPathArr[1]
    vw =  tempPathArr[2]
    itemID = tempPathArr[3]
    tools.debug("id is ",itemID)
    try:
        if itemID == "":
            tools.debug("id is empty")
            tempCms = CmsItem.objects.filter(controller = ctl).get(view = vw)
        else:
            tempCms = CmsItem.objects.filter(controller = ctl).filter(view = vw).get(itemID=int(itemID))
        return cms(request,tempCms)
    except Exception as error:
        tools.debug("cms routing error ",error)


    valList = ""
    for item in tempPathArr:
        valList += item + " ; "

    return HttpResponse("controller:" + tempPathArr[1] + "<br/>view:" + \
                        tempPathArr[2] + "<br/>input id:" + itemID)