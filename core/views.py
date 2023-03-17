from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Category,Product,Order,OrderItem
from django.contrib import messages
from .forms import OrderCreateForm
# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    context = {'product': product}
    return render(request, 'detail.html', context)


@login_required
def order_create(request):
    cart = OrderItem.objects.filter(order__user=request.user, order__paid=False)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item.product,
                                         price=item.price,
                                         quantity=item.quantity)
            cart.delete()
            messages.success(request, 'Order successfully created!')
            return redirect('order_detail', id=order.id)
    else:
        form = OrderCreateForm()
    context = {'cart': cart, 'form': form}
    return render(request, 'create.html', context)


@login_required
def order_detail(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    context = {'orders': order}
    return render(request, 'detail.html', context)
