from django.shortcuts import render, redirect
from main import models
from decimal import Decimal


def index(request):
    context = {}
    return render(request, 'dashboard/index.html', context)


# ---------CATEGORY-------------


def category_list(request):
    queryset = models.Category.objects.all()
    context = {
        'queryset': queryset
    }
    return render(request, 'dashboard/category/list.html', context)


def category_create(request):
    if request.method == 'POST':
        models.Category.objects.create(
            name=request.POST['name']
        )
        return redirect('dashboard:category_list')
    return render(request, 'dashboard/category/create.html')


def category_update(request, id):
    queryset = models.Category.objects.get(id=id)
    queryset.name = request.POST['name']
    queryset.save()
    return redirect('dashboard:category_list')


def category_delete(request, id):
    queryset = models.Category.objects.get(id=id)
    queryset.delete()
    return redirect('dashboard:category_list')


# ---------PRODUCT----------------

def product_list(request):
    queryset = models.Product.objects.all()
    context = {
        'queryset': queryset
    }
    return render(request, 'dashboard/product/list.html', context)


def product_detail(request, id):
    queryset = models.Product.objects.get(id=id)
    images = models.ProductImg.objects.filter(product=queryset)
    reviews = models.Review.objects.filter(product=queryset)
    context = {
        'queryset': queryset,
        'images': images,
        'reviews': reviews
    }
    return render(request, 'dashboard/product/detail.html', context)


def product_create(request):
    categorys = models.Category.objects.all()
    context = {'categorys': categorys}
    if request.method == 'POST':
        delivery = True if request.POST.get('delivery') else False

        product = models.Product.objects.create(
            category_id=request.POST['category_id'],
            name=request.POST['name'],
            body=request.POST['body'],
            price=request.POST['price'],
            banner_img=request.FILES['banner_img'],
            quantity=request.POST['quantity'],
            delivery=delivery
        )
        images = request.FILES.getlist('images')
        for image in images:
            models.ProductImg.objects.create(
                product=product,
                img=image
            )

        videos = request.FILES.getlist('videos')
        for video in videos:
            models.ProductVideo.objects.create(
                product=product,
                video=video
            )

        return redirect('dashboard:product_list')
    return render(request, 'dashboard/product/create.html', context)


def product_update(request, id):
    product = models.Product.objects.get(id=id)
    categorys = models.Category.objects.all()
    images = models.ProductImg.objects.filter(product=product)
    videos = models.ProductVideo.objects.filter(product=product)
    context = {
        'product': product,
        'categorys': categorys,
        'images': images,
        'videos': videos

    }
    if request.method == 'POST':
        delivery = True if request.POST.get('delivery') else False
        product.category.id = request.POST['category_id']
        product.name = request.POST['name']
        product.body = request.POST['body']
        price = request.POST.get('price')
        product.price = Decimal(price)
        print(product.price)

        if request.FILES.get('banner_id'):
            product.banner_img = request.FILES['banner_img']
        product.quantity = request.POST['quantity']
        product.delivery = delivery
        product.save()

        for i in images:
            imgdelete = f"imgdelete{i.id}"
            if request.POST.get(imgdelete):
                i.delete()

        imagess = request.FILES.getlist('images')
        for image in imagess:
            models.ProductImg.objects.create(
                product=product,
                img=image
            )

        videos = request.FILES.getlist('videos')
        for video in videos:
            models.ProductVideo.objects.create(
                product=product,
                video=video
            )

        return redirect('dashboard:product_list')
    return render(request, 'dashboard/product/update.html', context)


def product_delete(request, id):
    product = models.Product.objects.get(id=id)
    product.delete()
    return redirect('dashboard:product_list')


# def image_delete(request, id):
#     image = models.ProductImg.objects.get(id=id)
#     image.delete()
#
# def video_delete(request, id):
#     video = models.ProductVideo.objects.get(id=id)
#     video.delete()
