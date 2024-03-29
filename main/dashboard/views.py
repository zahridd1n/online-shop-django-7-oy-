from django.shortcuts import render, redirect
from main import models
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from main.models import User


def index(request):
    context = {}
    return render(request, 'dashboard/index.html', context)


# ---------CATEGORY-------------

@login_required()
def category_list(request):
    queryset = models.Category.objects.all()

    context = {
        'queryset': queryset
    }
    return render(request, 'dashboard/category/list.html', context)


@login_required()
def category_create(request):
    if request.method == 'POST':
        models.Category.objects.create(
            name=request.POST['name']
        )
        return redirect('dashboard:category_list')
    return render(request, 'dashboard/category/create.html')


@login_required()
def category_update(request, id):
    queryset = models.Category.objects.get(id=id)
    queryset.name = request.POST['name']
    queryset.save()
    return redirect('dashboard:category_list')


@login_required()
def category_delete(request, id):
    queryset = models.Category.objects.get(id=id)
    queryset.delete()
    return redirect('dashboard:category_list')


# ---------PRODUCT----------------
@login_required()
def product_list(request):
    categorys = models.Category.objects.all()
    category_id = request.GET.get('category_id')
    if category_id and category_id != '0':
        queryset = models.Product.objects.filter(category__id=category_id)
        i = models.Category.objects.get(id=category_id)
    else:
        queryset = models.Product.objects.all()
        i = None
    context = {
        'queryset': queryset,
        'categorys': categorys,
        'i': i
    }
    return render(request, 'dashboard/product/list.html', context)


@login_required()
def product_detail(request, code):
    queryset = models.Product.objects.get(code=code)
    images = models.ProductImg.objects.filter(product=queryset)
    reviews = models.Review.objects.filter(product=queryset)
    context = {
        'queryset': queryset,
        'images': images,
        'reviews': reviews
    }
    return render(request, 'dashboard/product/detail.html', context)


@login_required()
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


@login_required()
def product_update(request, code):
    product = models.Product.objects.get(code=code)
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

        # return redirect('dashboard:product_list')
    return render(request, 'dashboard/product/update.html', context)


@login_required()
def product_delete(request, code):
    product = models.Product.objects.get(code=code)
    product.delete()
    return redirect('dashboard:product_list')


def image_delete(request, id):
    image = models.ProductImg.objects.get(id=id)
    # product = models.Product.objects.get(id=image.product)
    # print(product.id)
    image.delete()

    return redirect('dashboard:product_update', image.product.id)


def video_delete(request, id):
    video = models.ProductVideo.objects.get(id=id)
    video.delete()

    return redirect('dashboard:product_update', video.product.id)


# ---------Settings----------------
@login_required()
def profile_update(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']
        user.save()
        return redirect('dashboard:index')
    return render(request, 'dashboard/setting.html', )


def edit_password(request):
    user = request.user
    password = request.POST.get('password')
    password_new = request.POST.get('password_new')
    password_conf = request.POST.get('password_conf')
    if user.check_password(password) and password_new==password_conf:
        user.set_password(password_new)
        user.save()
        return redirect('dashboard:index')