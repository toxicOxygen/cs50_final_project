from .tasks import order_created
from django.shortcuts import render, redirect, reverse
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
        
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
        cart.clear()

        order_created.delay(order.id) # deploy a celery task
        request.session['order_id'] = order.id
        return redirect(reverse('payment:process'))

        
    return render(request, 'orders/order/create.html', {'cart': cart, 'form':form})
