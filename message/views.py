# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from models import Message
import dazhu
import tools.webTools as tools
import tools.secu as websecu
import xml.dom.minidom as dom
from django.utils.decorators import method_decorator
from datetime import datetime
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from msg.models import send_msg

def recover(request):
    xmldoc = dom.parse(dazhu.settings.BASE_DIR +'/message.xml')
    itemlist = xmldoc.getElementsByTagName('blog')
    result = "over"
    tools.debug("start import")
    for item in itemlist:
        tempguid = item.attributes['guid'].value
        tools.debug("current guid is ",tempguid)
        try:
            tools.debug(tempguid, "tempguid is exist1")
            temp_message = Message.objects.get(guid=tempguid)
            tools.debug(tempguid, "tempguid is exist2")
        except:
            tools.debug(tempguid,"tempguid is not exist")
            result += tempguid + " imported <br>"
            temp_message = Message()
            temp_message.guid = item.attributes["guid"].value
            temp_message.author = item.attributes["author"].value
            tools.debug("author ", temp_message.author)

            temp_message.timestamp = datetime.strptime(item.attributes["timestamp"].value, "%Y%m%d %H%M%S")

            bodynode = item.getElementsByTagName('value')[0]
            temp_message.body = bodynode.firstChild.nodeValue
            tools.debug("value ", temp_message.body)

            temp_message.save()

    return HttpResponse(result)


class list(TemplateView):
    template_name = "message/index.html"
    def get_context_data(self, **kwargs):
        tools.debug("kwargs is ",kwargs)
        page_id = self.args[0]
        context = super(list, self).get_context_data(**kwargs)
        pageCount = 10

        if page_id == "":
            page_id = 1
        page_id = int(page_id)

        allCounts = Message.objects.count()
        allPages = allCounts // pageCount + 1

        posts = Message.objects.all().\
                    order_by("-timestamp")[(page_id - 1) * pageCount:page_id * pageCount]


         #c = {'posts':finalPosts, "category":category, 'currentAid':aid, 'allPages':allPages, }
        context['currentAid'] = page_id
        context['posts'] = posts
        context['allPages'] = allPages
        context['title'] = u'留言板'
        return context

    @method_decorator(csrf_protect)
    def post(self, request,pid):

        commentUser = websecu.xss_white_list(request.POST['user'])
        message = websecu.xss_white_list(request.POST['message'])
        tools.debug("message:",pid,commentUser,message,request.POST['message'])

        insert_message = Message()
        insert_message.body =  message
        insert_message.author = commentUser
        insert_message.timestamp = datetime.now()
        insert_message.save()

        send_msg(rid=0,sid=0,title=u"新的留言",content=u"内容：{}".format(message))

        return redirect("/message/")

