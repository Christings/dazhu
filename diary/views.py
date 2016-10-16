#coding:utf-8
from django.shortcuts import render

from django.views.generic.base import TemplateView
import tools.webTools as tools
from models import Diary
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.decorators import method_decorator
from datetime import datetime
from tools.secu import xssFilter

from account.secu import login_filter,user_login


def weekday(input):
    weekday_arr = [u"星期一", u"星期二", u"星期三", u"星期四", u"星期五", u"星期六", u"星期日", ]
    return weekday_arr[input]

def getDiary(pages,user):
    pageCount = 12  
    pages = int(pages)   

    allCounts = user.diary_set.count()
    allPages = allCounts // pageCount + 1
    posts = None
            
    if True:
        posts = user.diary_set.all().order_by("-timestamp")[(pages - 1) * pageCount:pages * pageCount]
    
    return posts, allPages


@login_filter
def ajaxDiary(request, pages):
    tools.debug("ajax get posts ", pages)
    try:
        pages = int(pages)
    except:
        pages = 1

    pagesInfo = getDiary(pages,request.user)
    posts = pagesInfo[0]
    allpages = pagesInfo[1]

    if allpages < pages:
        #tools.debug("allpages < pages ", allpages, pages)
        return HttpResponse()    

    result = []
    for item in posts:
        result.append({'id':item.id, 'weather':item.weather,\
                       'timestamp':item.timestamp.strftime("%Y-%m-%d"),\
                       'body':item.body.replace('\r', '<br>').replace('\n', '<br>'),\
                        'weekday':weekday(item.timestamp.weekday()),})
    #tools.debug("ajax post  is ",result)
    return HttpResponse(json.dumps(result, ensure_ascii=False))



# Create your views here.
class index(TemplateView):    
    template_name = "diary/index.html" 

    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        context['title'] = u'日记'
        return context
    
    @method_decorator(login_filter)
    @method_decorator(user_login)
    def get(self, request, *args, **kwargs):
        return TemplateView.get(self, request, *args, **kwargs)

    

    

# Create your views here.

class edit(TemplateView):    
    template_name = "diary/edit.html" 
    def get_context_data(self, **kwargs):
        context = super(edit, self).get_context_data(**kwargs)
        id = 0
        try:
            id = int(self.args[0])
        except:
            pass
        
        if id == 0:
            context['title'] = u'日记'
            return context
        else:
            tempDiary = Diary.objects.get(id=id)
            tempDiary.body = tempDiary.body.replace("<br/>", "\r\n")
            context['diary'] = tempDiary                  

        context['title'] = u'日记'
        return context
    
    @method_decorator(login_filter)
    def get(self, request, *args, **kwargs):
        return TemplateView.get(self, request, *args, **kwargs)
    
    @method_decorator(csrf_protect)
    @method_decorator(xssFilter)
    @method_decorator(login_filter)
    def post(self, request, id):
        tools.debug("id is ", id)      
        
        weather = request.POST['weather']
        textbody = request.POST['textbody']
        DiaryDate = request.POST['DiaryDate']
        
        textbody = textbody.replace("\r\n", "<br/>")        
        id = int(id)
        
        tempDiary = Diary()
        if id != 0:
            tempDiary = Diary.objects.get(id=id)
        tempDiary.author = request.user
        tempDiary.body = textbody
        tempDiary.weather = weather
        tools.debug("weather is ", weather)
        tempDiary.timestamp = datetime.strptime(DiaryDate, "%Y-%m-%d").date()            
        tempDiary.save()
        
        return HttpResponseRedirect('/diary/') 
    
    @method_decorator(csrf_protect)
    @method_decorator(login_filter)
    def delete(self, request, id):
        tools.debug("delete id is ", id)
        try:
            Diary.objects.get(id=int(id)).delete()
        except Exception as error:
            tools.debug("delete method error", error)
            return HttpResponse("error")
        return HttpResponse("success")
    
    
import xml.dom.minidom as dom
import dazhu
def recover(request):
    xmldoc = dom.parse(dazhu.settings.BASE_DIR +'/diary.xml')
    itemlist = xmldoc.getElementsByTagName('diary')
    result = "over"
    tools.debug("start import")
    for item in itemlist:
        try:
            temp_time = datetime.strptime(item.attributes["diaryDate"].value, "%Y%m%d").date()
            tempdiary = Diary.objects.filter(timestamp=temp_time)[0]
        except:
            tempdiary = Diary()
            tempdiary.author = request.user
            tempdiary.weather = item.attributes["diaryWeather"].value

            tempdiary.timestamp = datetime.strptime(item.attributes["diaryDate"].value, "%Y%m%d").date()

            tempdiary.body = item.firstChild.nodeValue

            result += item.attributes["diaryDate"].value + " imported <br>"
            #tools.debug("body",tempdiary.body)
            tempdiary.save()

    return HttpResponse(result)

from django.core.files.base import ContentFile
def download(request):
    doc = dom.Document()
    root = doc.createElement("diarys")
    doc.appendChild(root)

    diaries = request.user.diary_set.all()

    for diary in diaries:
        blognode = doc.createElement("diary")
        blognode.setAttribute("diaryWeather", diary.weather)
        tools.debug("download diary", diary.weather,weekday(diary.timestamp.weekday()))
        blognode.setAttribute("diaryWeekDay", weekday(diary.timestamp.weekday()))
        blognode.setAttribute("diaryDate", diary.timestamp.strftime("%Y%m%d"))
        bv = doc.createTextNode(diary.body)
        blognode.appendChild(bv)

        root.appendChild(blognode)
    xmlstr = doc.toprettyxml("\t", "\n", 'utf-8')
    f = ContentFile(xmlstr)

    response = HttpResponse(f.read(), content_type='xml')
    response['Content-Disposition'] = \
        'attachment; filename=%s' % "diary"+datetime.now().strftime("%Y%m%d")+".xml"
    return response