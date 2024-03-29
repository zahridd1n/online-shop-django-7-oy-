from django.shortcuts import render, redirect
from main import models


def index(request):
    categorys = models.Category.objects.all()

    context = {
        'categorys': categorys,
    }
    return render(request, 'front/index.html', context)


def category_list(request, id):
    categorys = models.Category.objects.all()
    catg = models.Category.objects.get(id=id)
    products = models.Product.objects.filter(category=catg)
    context = {
        'categorys': categorys,
        'products': products,
        'categor': catg,

    }

    return render(request, 'front/shoplist.html', context)


def product_detail(request, code):
    categorys = models.Category.objects.all()
    product = models.Product.objects.get(code=code)
    images = models.ProductImg.objects.filter(product=product.id)
    reviews = models.Review.objects.filter(product=product.id)
    # videos = models.ProductVideo.objects.filter(product=product)
    print(images)
    context = {
        'categorys': categorys,
        'product': product,
        'images': images,
        'reviews': reviews,
        # 'videos': videos,
    }
    return render(request, 'front/shopdetail.html', context)


def cart(request):
    categorys = models.Category.objects.all()
    context = {
        'categorys': categorys,
    }
    return render(request, 'front/cart.html', context)
