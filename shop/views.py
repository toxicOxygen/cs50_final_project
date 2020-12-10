from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from cart.forms import CartAddProductForm

# Create your views here.
def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,'product/list.html', {'products': products, 'categories': categories})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    cart_product_form = CartAddProductForm()
    return render(request, 'product/detail.html', {'product': product, 'form':cart_product_form})