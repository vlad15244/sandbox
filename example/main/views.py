from django.shortcuts import render

# Create your views here.
def index(request):
    content = {}
    content["message"] = "This is page"
    return render(template_name='main/index.html', request=request, context=content)