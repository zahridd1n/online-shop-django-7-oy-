from django.db import models
from django.contrib.auth.models import AbstractUser
from main.func import code_generate


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=255, blank=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)  # +
    discount_price = models.DecimalField(decimal_places=2, max_digits=10,
                                         blank=True, null=True)  # +
    banner_img = models.ImageField(upload_to='banner-img')
    quantity = models.IntegerField()
    delivery = models.BooleanField(default=False)  # +

    def save(self, *args, **kwargs):
        if not self.id:
            self.code = code_generate()
        super(Product, self).save(*args, **kwargs)


class ProductImg(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='img')


class ProductVideo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    video = models.FileField(upload_to='video')
    link = models.URLField(null=True, blank=True)


class Review(models.Model):
    mark = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def save(self, *args, **kwargs):
        user = self.user
        product = self.product
        mark = self.mark
        text = self.text

        if 0<mark<=5:
            try:
                existing_review = Review.objects.get(user=user, product=product)
                existing_review.mark = mark
                existing_review.text = text
                existing_review.save()
            except:
                super(Review, self).save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    count = models.IntegerField()


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # def save(self, *args, **kwargs):
    #     if WishList.objects.filter(user=self.user, product=self.product).count():
    #         raise ValueError('Ma`lumot bor')
    #     super(WishList, self).save(*args, **kwargs)
