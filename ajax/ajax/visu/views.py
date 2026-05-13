from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils import timezone
import platform
import psutil
import json
from django.utils.decorators import method_decorator
import random



# Create your views here.
def index(request):
    return render(request, 'visu/index.html')

"""@csrf_exempt
def ajax_ex(request):

    if request.method == "POST":
        content_type = request.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            data = json.loads(request.body)
            name = data.get('text')
            return JsonResponse({'system': platform.system() + platform.version(), 'disks' : psutil.disk_partitions(), 'text' : name })
        else:
            print('Обычный запрос')
            return HttpResponse('<h1>Обычный запрос</h1>') """

@method_decorator(csrf_exempt, name='dispatch')
class MyView(View):

    def post(self, request, *args, **kwargs):
        content_type = request.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            data = json.loads(request.body)
            print(data)
            name = data.get('name')
            age = data.get('age')            
            return JsonResponse({'system': platform.system() + platform.version(), 'disks' : psutil.disk_partitions(), 'name' : name, 'age' : age })    

    def get(self, request, *args, **kwargs):
            return HttpResponse('<h1>Обычный запрос</h1>')    


@method_decorator(csrf_exempt, name='dispatch')
class Runtime(View):

    def post(self, request, *args, **kwargs):
        content_type = request.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            
            data = {"timestamp" : timezone.now().isoformat()} 

            return JsonResponse(data)    

    def get(self, request, *args, **kwargs):
            data = {"timestamp" : timezone.now().isoformat(), "value" : random.randint(0,50)} 
            return JsonResponse(data)    
    
@csrf_exempt
def ajax_ex_plus(request):

    if request.method == "POST":
        content_type = request.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            data = json.loads(request.body)
            current_page = int(data.get('current_page'))

            if current_page == 0:
                current_page += 1
            elif current_page == 50:
                current_page = 1
            else:
                current_page += 1

            return JsonResponse({'new_page': current_page})
        else:
            print('Обычный запрос')
            return HttpResponse('<h1>Обычный запрос</h1>')

@csrf_exempt
def ajax_ex_minus(request):

    if request.method == "POST":
        content_type = request.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            data = json.loads(request.body)
            current_page = int(data.get('current_page'))

            if current_page == 1:
                current_page = 50
            elif current_page == 50:
                current_page -= 1
            else:
                current_page -= 1

            return JsonResponse({'new_page': current_page})
        else:
            print('Обычный запрос')
            return HttpResponse('<h1>Обычный запрос</h1>')

           