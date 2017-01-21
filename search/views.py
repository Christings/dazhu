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

        final_result = []
        class SearchItem(object):
            pass

        def _get_search_item(guid, category, title, body, keywords):
            tempItem = SearchItem()
            tempItem.guid = guid
            tempItem.category = category
            tempItem.title = self.GetContent(title,keywords)
            tempItem.search_content = self.GetContent(body, keywords)
            return tempItem

        title_result = [_get_search_item(
                        x.guid, 
                        x.category, 
                        tools.RemoveHttpStr(x.title),
                        tools.RemoveHttpStr(x.body),
                        keywords) for x in posts_title]

        body_result = [_get_search_item(
                        x.guid, 
                        x.category, 
                        tools.RemoveHttpStr(x.title),
                        tools.RemoveHttpStr(x.body),
                        keywords) for x in posts_body if keywords in tools.RemoveHttpStr(x.body)]

        final_result += title_result
        final_result += body_result

        no_repeat_id_map = {}
        no_repeat_result = []
        for item in final_result:
            if item.guid not in no_repeat_id_map:
                no_repeat_id_map[item.guid] = True
                no_repeat_result.append(item)

        context['title'] = keywords
        context['posts'] = no_repeat_result
        return context

    def GetContent(self,input_str,keyword):
        color_fmt="<span style='color:red;'>@#k</span>"
        content_length = 60
        tools.debug("GetContent ",input_str)
        # input_str = tools.RemoveHttpStr(input_str)
        index= input_str.find(keyword)
        start = index - content_length
        if start < 0:
            start = 0
        end = index + content_length
        if end > len(input_str):
            end = len(input_str)

        input_str = input_str[start:end]
        color_keyword = color_fmt.replace("@#k",keyword)
        input_str = input_str.replace(keyword,color_keyword)
        return input_str