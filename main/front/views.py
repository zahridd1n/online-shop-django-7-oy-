from django.shortcuts import render, redirect
from main import models
from django.contrib.auth.decorators import login_required

@login_required(login_url='auth:sign-in')
def index(request):
    categorys = models.Category.objects.all()
    products = models.Product.objects.all()
    cart = models.Cart.objects.get_or_create(user=request.user, is_active=True)

    context = {
        'categorys': categorys,
        'products': products,
        'cart': cart,

    }
    return render(request, 'front/index.html', context)


def category_list(request, id):
    categorys = models.Category.objects.all()
    catg = models.Category.objects.get(id=id)
    products = models.Product.objects.filter(category=catg)
    cart = models.Cart.objects.get_or_create(user=request.user, is_active=True)
    context = {
        'categorys': categorys,
        'products': products,
        'categor': catg,
        'cart': cart,

    }

    return render(request, 'front/shoplist.html', context)


def product_detail(request, code):
    categorys = models.Category.objects.all()
    product = models.Product.objects.get(code=code)
    images = models.ProductImg.objects.filter(product=product.id)
    reviews = models.Review.objects.filter(product=product.id)
    cart = models.Cart.objects.get_or_create(user=request.user, is_active=True)
    # videos = models.ProductVideo.objects.filter(product=product)
    print(images)
    context = {
        'categorys': categorys,
        'product': product,
        'images': images,
        'reviews': reviews,
        'cart': cart,
        # 'videos': videos,
    }
    return render(request, 'front/shopdetail.html', context)


@login_required(login_url='auth:sign-in')
def cart_list(request):
    categorys = models.Category.objects.all()
    queryset = models.Cart.objects.filter(user=request.user, is_active=False)
    cart = models.Cart.objects.get_or_create(user=request.user, is_active=True)
    context = {
        'categorys': categorys,
        'queryset': queryset,
        'cart': cart,
    }
    return render(request, 'front/carts/list.html', context)


@login_required(login_url='auth:sign-in')
def active_cart(request):
    queryset, _ = models.Cart.objects.get_or_create(user=request.user, is_active=True)
    return redirect('front:cart', queryset.code)


@login_required(login_url='auth:sign-in')
def cart_detail(request, code):
    categorys = models.Category.objects.all()
    cart = models.Cart.objects.get(code=code)
    queryset = models.CartProduct.objects.filter(cart=cart)

    context = {
        'cart': cart,
        'queryset': queryset,
        'categorys': categorys,
    }

    return render(request, 'front/carts/detail.html', context)


def nima(request, id):
    if request.method == 'POST':
        count = int(request.POST['count'])
        cart_product = models.CartProduct.objects.get(id=id)
        cart_product.count = count
        cart_product.save()
        return redirect('front:cart', cart_product.cart.code)


def cart_product_delete(request, id):
    cart_product = models.CartProduct.objects.get(id=id)
    cart_product.delete()
    return redirect('front:cart', cart_product.cart.code)


def add_cart_product(request, code):
    product = models.Product.objects.get(code=code)
    cart, _ = models.Cart.objects.get_or_create(user=request.user, is_active=True)
    count = 1
    if models.CartProduct.objects.filter(product=product, cart=cart).count():
        c = models.CartProduct.objects.get(product=product, cart=cart)
        c.count +=1
        c.save()
    else:
        p = models.CartProduct.objects.create(
            product=product,
            cart=cart,
            count=count,
        )

    return redirect('front:cart', cart.code)


def product_order(request):
    cart = models.Cart.objects.get(user=request.user, is_active=True)

    cart.is_active = False
    cart.save()

    return redirect('front:cart_list')
