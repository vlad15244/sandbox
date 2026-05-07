from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import platform
import psutil

# Create your views here.
def index(request):
    return render(request, 'visu/index.html')

@csrf_exempt
def ajax_ex(request):

    if request.method == "POST":
        return JsonResponse({'system': platform.system() + platform.version(), 'disks' : psutil.disk_partitions() }) 
           