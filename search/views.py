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

        posts = BlogPost.objects.filter(title__contains=keywords)

        context['title'] = keywords
        context['posts'] = posts
        return context