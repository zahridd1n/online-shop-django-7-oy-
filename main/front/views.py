from django.shortcuts import render, redirect
from main import models
from django.contrib.auth.decorators import login_required
from datetime import date


@login_required(login_url='auth:sign-in')
def index(request):
    categorys = models.Category.objects.all()
    products = models.Product.objects.all()
    cart = models.Cart.objects.get_or_create(user=request.user, status=1)
    wishlist = models.WishList.objects.filter(user=request.user)

    wishlisted_codes = [item.product.code for item in wishlist]
    # print(wishlisted_codes)
    for product in products:
        v = product.code in wishlisted_codes
        setattr(product, 'is_wishlisted', v)

    context = {
        'categorys': categorys,
        'products': products,
        'wishlist': wishlist,
        'cart': cart,

    }
    return render(request, 'front/index.html', context)


def category_list(request, id):
    categorys = models.Category.objects.all()
    catg = models.Category.objects.get(id=id)
    products = models.Product.objects.filter(category=catg)
    cart = models.Cart.objects.get_or_create(user=request.user, status=1)
    wishlist = models.WishList.objects.filter(user=request.user)
    context = {
        'categorys': categorys,
        'products': products,
        'categor': catg,
        'cart': cart,
        'wishlist': wishlist,

    }

    return render(request, 'front/shoplist.html', context)


def product_detail(request, code):
    categorys = models.Category.objects.all()
    product = models.Product.objects.get(code=code)
    images = models.ProductImg.objects.filter(product=product.id)
    reviews = models.Review.objects.filter(product=product.id)
    cart = models.Cart.objects.get_or_create(user=request.user, status=1)
    wishlist = models.WishList.objects.filter(product=product, user=request.user)
    if wishlist:
        wishlist = wishlist[0]
    # videos = models.ProductVideo.objects.filter(product=product)
    print(images)
    context = {
        'categorys': categorys,
        'product': product,
        'images': images,
        'reviews': reviews,
        'wishlist': wishlist,
        'cart': cart,
        # 'videos': videos,
    }
    return render(request, 'front/shopdetail.html', context)


@login_required(login_url='auth:sign-in')
def cart_list(request):
    categorys = models.Category.objects.all()
    queryset = models.Cart.objects.filter(user=request.user, status=2)
    cart = models.Cart.objects.get_or_create(user=request.user, status=1)
    context = {
        'categorys': categorys,
        'queryset': queryset,
        'cart': cart,
    }
    return render(request, 'front/carts/list.html', context)


@login_required(login_url='auth:sign-in')
def active_cart(request):
    queryset, _ = models.Cart.objects.get_or_create(user=request.user, status=1)
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


@login_required(login_url='auth:sign-in')
def cart_product_delete(request, id):
    cart_product = models.CartProduct.objects.get(id=id)
    cart_product.delete()
    return redirect('front:cart', cart_product.cart.code)


@login_required(login_url='auth:sign-in')
def add_cart_product(request, code):
    product = models.Product.objects.get(code=code)
    cart, _ = models.Cart.objects.get_or_create(user=request.user, status=1)
    count = 1
    if models.CartProduct.objects.filter(product=product, cart=cart).count():
        c = models.CartProduct.objects.get(product=product, cart=cart)
        c.count += 1
        c.save()
    else:
        p = models.CartProduct.objects.create(
            product=product,
            cart=cart,
            count=count,
        )

    return redirect('front:cart', cart.code)


@login_required(login_url='auth:sign-in')
def product_order(request):
    cart = models.Cart.objects.get(user=request.user, status=1)
    cart_product = models.CartProduct.objects.filter(cart=cart)
    for item in cart_product:
        item.product.quantity -= item.count
        item.product.save()

    cart.status = 2
    cart.save()

    return redirect('front:order_list')


@login_required(login_url='auth:sign-in')
def order_list(request):
    queryset = models.Cart.objects.filter(user=request.user, status__in=[2, 3, 4]).order_by('-date')
    context = {
        'queryset': queryset,
    }

    return render(request, 'front/order/list.html', context)


@login_required(login_url='auth:sign-in')
def order_confirm(request, code):
    cart = models.Cart.objects.get(code=code, user=request.user)
    cart.status = 4
    cart.save()
    return redirect('front:order_list')


@login_required(login_url='auth:sign-in')
def order_rejection(request, code):
    cart = models.Cart.objects.get(code=code, user=request.user)
    cart.status = 3
    cart.save()
    return redirect('front:order_list')


@login_required(login_url='auth:sign-in')
def order_review(request, code):
    cart = models.Cart.objects.get(code=code, user=request.user)
    products = models.CartProduct.objects.filter(cart=cart)
    if request.method == 'POST':
        for product in products:
            review = models.Review.objects.create(
                product=product.product,
                user=request.user,
                mark=int(request.POST.get('mark')),
                text=request.POST.get('message')
            )

    return redirect('front:order_list')


# ---------WISHLIST---------
@login_required(login_url='auth:sign-in')
def wishlist(request):
    categorys = models.Category.objects.all()
    queryset = models.WishList.objects.filter(user=request.user)

    context = {
        'categorys': categorys,
        'queryset': queryset,
    }

    return render(request, 'front/wishlist.html', context)


@login_required(login_url='auth:sign-in')
def wishlist_delete(request, code):
    wishlist = models.WishList.objects.get(product__code=code, user=request.user)
    if wishlist:
        wishlist.delete()
    else:
        pass
    # return redirect('front:wishlist')
    return redirect(request.META.get('HTTP_REFERER', 'front:wishlis'))


@login_required(login_url='auth:sign-in')
def wishlist_add(request, code):
    product = models.Product.objects.get(code=code)
    models.WishList.objects.create(product=product, user=request.user)
    # return redirect('front:wishlist')
    return redirect(request.META.get('HTTP_REFERER', 'front:wishlis'))
