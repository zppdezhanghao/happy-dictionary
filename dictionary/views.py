from urllib.parse import quote
from django.core import serializers
from django.shortcuts import render

from .forms import TranslationForm
from .iciba import iciba


def show_index(request):
    if request.method == 'POST':
        # 接受request.POST参数构造form类的实例
        form = TranslationForm(request.POST)
    else:
        form = TranslationForm()

    logo = 'static/images/logo2.jpg'
    return render(request, 'translate/index.html', {'form': form, 'logo': logo})


def translate(request):
    form = TranslationForm()
    
    request.encoding = 'utf-8'
    if 'q' in request.GET and request.GET['q']:
        message = iciba(quote(request.GET['q'], 'utf-8'))

    message2 = []
    if type(message) != str:
        print('{}/n{}'.format(message.getElementsByTagName('pos')[0].childNodes.length,message.getElementsByTagName('acceptation').length))
        if message.getElementsByTagName('pos').length > 0:
            for acceptationlist, poslist in zip(message.getElementsByTagName('acceptation'),
                                            message.getElementsByTagName('pos')):
                if poslist.childNodes.length > 0:
                   for acceptation, pos in zip(acceptationlist.childNodes, poslist.childNodes):
                        message2.append(pos.data + acceptation.data)
                else:
                    for acceptation in acceptationlist.childNodes:
                        message2.append(acceptation.data)


        else:
            for acceptationlist in message.getElementsByTagName('acceptation'):
                for acceptation in acceptationlist.childNodes:
                    message2.append(acceptation.data)
                    print(acceptation.data)
    else:
        message2.append(message)
    


    return render(request, 'translate/result.html', {'form': form, 'acceptation': message2})