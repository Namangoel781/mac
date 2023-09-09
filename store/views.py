
from django.http import HttpResponse
from django.shortcuts import render
from math import ceil
from .models import Product, Contact, Orders, OrderUpdate
import json

# Create your views here.
def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
         prod = Product.objects.filter(category=cat)
         n= len(prod)
         nSlides= n//4 + ceil((n/4)-(n//4))
         allProds.append([prod, range(1, nSlides), nSlides])
    params={'allProds':allProds }
    return render(request,"store/index.html", params)


def about(request):
     
     return render(request, 'store/about.html')


def contact(request):
    if request.method=="POST":
        print(request)
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        desc=request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, "store/contact.html")


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'store/tracker.html')


def search(request):
    return render(request, 'store/search.html')


def productView(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'store/prodView.html',{'product': product[0]})


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        order = Orders(items_json=items_json, name=name, email=email, phone=phone, address=address, city=city, state=state, zip_code=zip_code)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'store/checkout.html', {'thank': thank, 'id':id})
    return render(request, 'store/checkout.html')


