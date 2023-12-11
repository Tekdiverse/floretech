from django.shortcuts import render

# Create your views here.
def custom_error_page(request,exception):
    return render(request, 'errors/custom_error.html')

def custom_error_page1(request):
    return render(request, 'errors/500.html')

def index(request):

    return render(request, "core/index.html")