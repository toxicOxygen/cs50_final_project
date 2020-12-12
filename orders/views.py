from .tasks import order_created
from django.shortcuts import render
from .forms import OrderForm
from cart.cart import Cart
from .models import OrderItem

def order_create(request):
    cart = Cart(request)

    if request.method == "GET":
        form = OrderForm()
        return render(request, 'orders/order/create.html', {'cart': cart, 'form':form})
    
    #that mean this is a post
    form = OrderForm(request.POST)

    if form.is_valid():
        order = form.save()
        order_created.delay(order.id) #a celery task to send an email to the user
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
        cart.clear()
        return render(request,'orders/order/created.html', {'order': order})
        
    return render(request, 'orders/order/create.html', {'cart': cart, 'form':form})
