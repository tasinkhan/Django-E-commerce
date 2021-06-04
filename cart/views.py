from django.shortcuts import render

# Create your views here.
def add_cart(request):
    pass

def cart(request):
    return render(request,'store/cart.html')