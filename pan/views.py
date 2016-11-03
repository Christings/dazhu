#coding:utf-8
from django.shortcuts import render
import subprocess
import os, sys
from django.views.generic.base import TemplateView
import dazhu
import tools.webTools as tools
from django.shortcuts import redirect
from multiprocessing.dummy import Pool as ThreadPool


class index(TemplateView):    
    template_name = "pan/index.html"

    def get(self, request, *args, **kwargs):
        return TemplateView.get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        class tempFile(object):
            pass

        result = []
        subfolder = dazhu.settings.BASE_DIR + "/dazhu/static/pan/"
        files = os.listdir(subfolder)
        for item in files:            
            tools.debug("pan index get_context_data item", item)
            if os.path.isfile(subfolder + item):
                stdin_encoding = sys.stdin.encoding
                if stdin_encoding == None:
                    stdin_encoding = "ANSI_X3.4-1968"
                item = item.decode(stdin_encoding)
                tempfile = tempFile()
                tempfile.filename = item
                tempfile.filelength = os.path.getsize(subfolder + item)
                result.append(tempfile)
        
        context['downloadfiles'] = result 
        context['title'] = u'下载'
        return context

pool = ThreadPool(4)
def download_file(request):
    subfolder = dazhu.settings.BASE_DIR + "/dazhu/static/pan/"
    dp_url = request.GET["dp"]
    tools.debug("download_file dp_url = ", dp_url)
    # out_bytes = subprocess.check_output('wget {}'.format(download_path), shell=True)
    def __download(url):
        tools.debug("__download url", url)
        out_bytes = subprocess.check_output('wget {} -P {}'.format(url, subfolder), shell=True)
        tools.debug("download_file", out_bytes)

    pool.apply_async(__download, (dp_url,))

    return redirect("/pan")

def del_file(request):
    del_path = request.GET["dp"]
    subfolder = dazhu.settings.BASE_DIR + "/dazhu/static/pan/"
    tools.debug("del_file path = ", del_path)
    os.remove(subfolder + del_path)
    # out_bytes = subprocess.check_output('wget {}'.format(download_path), shell=True)
    return redirect("/pan")
    