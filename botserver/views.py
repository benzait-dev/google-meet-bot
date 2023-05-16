from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import os

def index(request):
    link = ''
    if request.method == "POST":
        link = request.POST.get('meetlink')
        if link != '':
            # get current working directory            
            subprocess.run(['C:/Users/max/Documents/Benzait/google-meet-bot/botserver/meetbot.py',link])

    return render(request,'index.html',context=None)


