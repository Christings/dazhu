# coding:utf-8
from django.http import HttpResponse
from models import BlogPost, Category,Comment
import tools.webTools as tools
import json as simplejson

import urllib
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.utils import timezone
from tools.secu import xssFilter,xss_white_list
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from datetime import datetime
from ip_filter.views import ip_filter
import markdown
from django.http import Http404


def remove_pri_category(blog_posts):
    # remove privite category
    for item in blog_posts:
        try:
            category = Category.objects.get(title=item.category)
            if category.is_privite:
                blog_posts.remove(item)
        except:
            pass
    return blog_posts

def get_category_obj(is_login):
    result = Category.objects.all()
    
    if not is_login:
        result = [x for x in result if not x.is_privite]
    return result

class index(TemplateView):
    template_name = "blog/index.html"

    @method_decorator(ip_filter)
    def get(self, request, *args, **kwargs):
        return TemplateView.get(self, request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data(**kwargs)

        posts = BlogPost.objects.all().order_by("-timestamp")[:10]
        result = []        
        for item in posts:
            temp = item
            temp.commentsCount = item.comment_set.count()
            temp.body = markdown.markdown(temp.body)
            result.append(temp)

        context['posts'] = result[:10]
        if not self.request.user.is_authenticated():
            context['posts'] = remove_pri_category(context['posts'])

        context['category'] = get_category_obj(self.request.user.is_authenticated())
        context['title'] = u'大猪大兔在一起'
        return context

# ajax get category
def get_category(request):
    try:
        is_login = request.user.is_authenticated()
        result =[x.title for x in get_category_obj(is_login)] 
        return HttpResponse(simplejson.dumps(result, ensure_ascii=False))
    except:
        return HttpResponse()


class list(TemplateView):
    template_name = "blog/list.html"
    def get_context_data(self, **kwargs):
        tools.debug("kwargs is ",kwargs)
        aid = self.args[0]
        context = super(list, self).get_context_data(**kwargs)
        pageCount = 20

        if aid == "":
            aid = 1
        aid = int(aid)

        allCounts = BlogPost.objects.count()
        allPages = allCounts // pageCount + 1

        posts = BlogPost.objects.all().order_by("-timestamp")[(aid - 1) * pageCount:aid * pageCount]

        finalPosts = []
        class postBlock(object):
            def __init__(self):
                self.title = ""
                self.items = []
        #在list的时候，按月分组显示
        tempTime = ""
        tempPB = postBlock()
        group_time_fmt = '%Y-%m'
        for item in posts:
            item.commentsCount = item.comment_set.count()
            if item.timestamp.strftime(group_time_fmt) != tempTime:
                finalPosts.append(tempPB)
                tempPB = postBlock()
                tempPB.title = item.timestamp.strftime(group_time_fmt)
                tempTime = item.timestamp.strftime(group_time_fmt)
                tempPB.items.append(item)
            else:
                tempPB.items.append(item)

        finalPosts.append(tempPB)
        finalPosts.pop(0)

        category = Category.objects.all()
         #c = {'posts':finalPosts, "category":category, 'currentAid':aid, 'allPages':allPages, }
        context['posts'] = finalPosts
        if not not self.request.user.is_authenticated():
            context['posts'] = remove_pri_category(context['posts'])
        context['category'] = get_category_obj(self.request.user.is_authenticated())
        context['currentAid'] = aid
        context['allPages'] = allPages
        context['title'] = u'博客'
        return context

class catelist(TemplateView):
    template_name = "blog/catelist.html"
    def get_context_data(self, **kwargs):
        context = super(catelist, self).get_context_data(**kwargs)

        categoryID = self.args[0]
        category = Category.objects.get(id=categoryID)
        posts = BlogPost.objects.filter(category=category.title).order_by("-timestamp")

        categorys = Category.objects.all()

        context['posts'] = posts
        context['category'] = categorys
        context['title'] = category.title
        if category.is_privite and not self.request.user.is_authenticated():
            context['posts'] = []

        return context


class details(TemplateView):
    def check_answer(self, blog):
        if blog.question == "":
            return True
        else:
            return False
        return True

    template_name = "blog/details.html"
    def get_context_data(self, **kwargs):
        context = super(details, self).get_context_data(**kwargs)
        guid = self.args[0]
        tools.debug("blog details get_context_data guid %s" % guid)
        try:
            blog = BlogPost.objects.get(guid=guid)
        except BlogPost.DoesNotExist:
            tools.debug("blog details get_context_data blog %s is not found" % guid)
            raise Http404("does not exist")
        
        # check if it is privite category
        category = Category.objects.get(title=blog.category)
        if category.is_privite and not self.request.user.is_authenticated():
            raise Http404("you cant feel the blog because it is in privite group")

        # blog.body = markdown.markdown(blog.body, extensions=['markdown.extensions.extra',
        # "markdown.extensions.nl2br",
        # 'markdown.extensions.sane_lists',
        #  'codehilite'])
        category = get_category_obj(self.request.user.is_authenticated())

        context['blog'] = blog
        context['category'] = category
        context['title'] = blog.title

        comments = blog.comment_set.all()
        context['comments'] = comments
        context['commentsCount'] = len(comments)
        return context

    @method_decorator(csrf_protect)
    def post(self, request, aid):
        '''
        post blog comment NOT blog content
        :param request:
        :param aid:
        :return this page:
        '''
        tools.debug("id is ", aid)

        commentUser = xss_white_list(request.POST['user'])
        message = xss_white_list(request.POST['message'])

        tempComment = Comment()
        tempComment.author = commentUser
        tools.debug("commentUser ", commentUser)
        tempComment.body = message
        tools.debug("message ", message)
        tempComment.blog = BlogPost.objects.get(guid=aid)
        tempComment.timestamp = timezone.now()
        tools.debug("timestamp ", timezone.now())
        tempComment.save()

        return redirect("/blog/details/"+aid)


@csrf_protect
def get_content(request):
    aid = request.GET["aid"]
    answer = request.GET["answer"]
    tempblog = BlogPost.objects.get(guid=aid)
    tools.debug("getcontent",aid,answer,tempblog.answer)
    if tempblog.answer == answer:
        return HttpResponse(tempblog.body)
    else:
        return HttpResponse("error")


import xml.dom.minidom as dom
from django.core.files.base import ContentFile
import os

def download(request):
    #download as xml
    download_type = "txt"
    if download_type == "xml":
        doc = dom.Document()
        root = doc.createElement("blogs")
        doc.appendChild(root)

        blogs = BlogPost.objects.all()
        for blog in blogs:
            blognode = doc.createElement("blog")
            blognode.setAttribute("guid", blog.guid)
            blognode.setAttribute("author", blog.author)
            blognode.setAttribute("title", blog.title)
            blognode.setAttribute("category", blog.category)
            blognode.setAttribute("timestamp", blog.timestamp.strftime("%Y%m%d %H%M%S"))
            body = doc.createElement("value")
            bv = doc.createTextNode(blog.body)
            body.appendChild(bv)

            blognode.appendChild(body)

            #attachment
            ats = blog.attachment_set.all()
            for at in ats:
                atnode = doc.createElement("attachment")
                atnode.setAttribute("sourceName", at.sourceName)
                atnode.setAttribute("rndName", at.rndName)
                blognode.appendChild(atnode)
            #comment
            cms = blog.comment_set.all()
            for cm in cms:
                cmnode = doc.createElement("comment")
                cmnode.setAttribute("author", cm.author)
                cmnode.setAttribute("body", cm.body)
                cmnode.setAttribute("timestamp", cm.timestamp.strftime("%Y%m%d %H%M%S"))
                blognode.appendChild(cmnode)

            root.appendChild(blognode)

        f = ContentFile(doc.toprettyxml("\t", "\n", "utf-8"))
        response = HttpResponse(f.read(), content_type='xml')
        response['Content-Disposition'] = 'attachment; filename=%s' % "hi.xml"

    if download_type == "txt":
        blogs = BlogPost.objects.all()
        result = ""
        for blog in blogs:
            result += u"标题：" + blog.title + u"\r\n作者：" + blog.author + u"\r\n分类："\
             + blog.category + u"\r\n时间：" + blog.timestamp.strftime("%Y%m%d %H:%M:%S") + "\r\n"

            result += tools.RemoveHttpStr(blog.body.replace("\n","\r\n").replace("</p>","\r\n").replace("&nbsp;"," ").replace("<br/>","\r\n"))
            result += "\r\n\r\n"

        response = HttpResponse(result, content_type='txt')
        response['Content-Disposition'] = 'attachment; filename=%s' % "hi.txt"

    return response


import dazhu
from ueditor.models import attachment
def recover(request):
    xmldoc = dom.parse(dazhu.settings.BASE_DIR +'/backup.xml')
    itemlist = xmldoc.getElementsByTagName('blog')
    result = "over"
    tools.debug("start import")
    for item in itemlist:
        tempguid = item.attributes['guid'].value
        tools.debug("current guid is ",tempguid)
        try:
            tempblog = BlogPost.objects.get(guid=tempguid)
        except:
            tools.debug(tempguid,"tempguid is exist")
            result += tempguid + " imported <br>"
            tempblog = BlogPost()
            tempblog.guid = item.attributes["guid"].value
            tempblog.author = item.attributes["author"].value
            tools.debug("author ", tempblog.author)
            tempblog.title = item.attributes["title"].value
            tempblog.category = item.attributes["category"].value
            tempblog.timestamp = datetime.strptime(item.attributes["timestamp"].value, "%Y%m%d %H%M%S")

            bodynode = item.getElementsByTagName('value')[0]
            tempblog.body = bodynode.firstChild.nodeValue
            tools.debug("value ", tempblog.body)

            tempblog.save()

            attachments = item.getElementsByTagName('attachment')
            for atts in attachments:
                rndName = atts.attributes["rndName"].value
                sourceName = atts.attributes["sourceName"].value

                tempAttachment = attachment()
                tempAttachment.blog = tempblog
                tempAttachment.sourceName = sourceName
                tempAttachment.rndName = rndName
                tempAttachment.save()

            cmts = item.getElementsByTagName('comment')
            for cmt in cmts:
                author = cmt.attributes["author"].value
                body = cmt.attributes["body"].value
                timestamp = datetime.strptime(cmt.attributes["timestamp"].value, "%Y%m%d %H%M%S")

                tempComment = Comment()
                tempComment.author = author
                tools.debug("commentUser ", author)
                tempComment.body = body
                tools.debug("message ", body)
                tempComment.blog = tempblog
                tempComment.timestamp = timestamp
                tools.debug("timestamp ", timestamp)
                tempComment.save()

    return HttpResponse(result)

def test(request):
    return HttpResponse("haha")