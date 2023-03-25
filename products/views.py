from django.shortcuts import render

def products(request, *args, **kwargs):
    breakpoint()
    return render(request, 'products/index.html')