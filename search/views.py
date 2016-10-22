from django.shortcuts import render
import tools.webTools as tools
from django.views.generic.base import TemplateView
import urllib
from blog.models import BlogPost
# Create your views here.
class result(TemplateView):
    template_name = "search/result.html"
    def get_context_data(self, **kwargs):
        context = super(result, self).get_context_data(**kwargs)
        keywords = None
        try:
            keywords = self.request.GET["k"]
        except:
            pass

        tools.debug("search key", keywords)
        keywords = urllib.unquote(keywords)
        tools.debug('search key2', keywords)

        posts_title = BlogPost.objects.filter(title__contains=keywords)
        posts_body = BlogPost.objects.filter(body__contains=keywords)

        final_result_map = {}
        final_result = []

        class SearchItem(object):
            pass

        for item in posts_title:
            if item.guid not in final_result_map:
                final_result_map[item.guid] = True
                tempItem = SearchItem()
                tempItem.guid = item.guid
                tempItem.category = item.category
                tempItem.title = self.GetContent(item.title,keywords)
                tempItem.search_content = self.GetContent(item.body,keywords)
                final_result.append(tempItem)

        for item in posts_body:
            if item.guid not in final_result_map:
                final_result_map[item.guid] = True
                tempItem = SearchItem()
                tempItem.guid = item.guid
                tempItem.category = item.category
                tempItem.title = self.GetContent(item.title,keywords)
                tempItem.search_content = self.GetContent(item.body,keywords)
                final_result.append(tempItem)


        context['title'] = keywords
        context['posts'] = final_result
        return context

    def GetContent(self,input_str,keyword):
        format_str="<span style='color:red;'>@#k</span>"
        content_length = 60
        tools.debug("GetContent ",input_str)

        input_str = tools.RemoveHttpStr(input_str)
        fmtkeyword = format_str.replace("@#k",keyword)
        input_str = input_str.replace(keyword,fmtkeyword)
        index= input_str.find(keyword)

        start = index - content_length
        if start < 0:
            start = 0
        end = index + content_length
        if end > len(input_str):
            end = len(input_str)

        return input_str[start:end]