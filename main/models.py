from django.db import models
from django.contrib.auth.models import AbstractUser
from random import sample
import string


class CodeGenerate(models.Model):
    code = models.CharField(max_length=255, blank=True, unique=True)

    @staticmethod
    def generate_code():
        return ''.join(sample(string.ascii_letters, 15))

    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate, self).save(*args, **kwargs)

    class Meta:
        abstract = True


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


class Product(CodeGenerate):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)  # +
    discount_price = models.DecimalField(decimal_places=2, max_digits=10,
                                         blank=True, null=True)  # +
    banner_img = models.ImageField(upload_to='banner-img')
    quantity = models.IntegerField()
    delivery = models.BooleanField(default=False)  # +


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

        if 0 < mark <= 5:
            try:
                existing_review = Review.objects.get(user=user, product=product)
                existing_review.mark = mark
                existing_review.text = text
                existing_review.save()
            except:
                super(Review, self).save(*args, **kwargs)


class Cart(CodeGenerate):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    order_date = models.DateField(null=True, blank=True)

    @property
    def total(self):
        count = 0
        queryset = CartProduct.objects.filter(cart=self)
        for item in queryset:
            count += item.count
        return count

    @property
    def price(self):
        queryset = CartProduct.objects.filter(cart=self)
        total = 0
        for item in queryset:
            if item.product.discount_price:
                total += item.count * item.product.discount_price
            else:
                total += item.count * item.product.price
        return total

    @property
    def total_price(self):
        queryset = CartProduct.objects.filter(cart=self)
        total = 0
        for item in queryset:
            total += item.count * item.product.price
        return total


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    count = models.IntegerField()

    @property
    def price(self):
        if self.product.discount_price:
            return self.count * self.product.discount_price
        else:
            return self.count * self.product.price


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # def save(self, *args, **kwargs):
    #     if WishList.objects.filter(user=self.user, product=self.product).count():
    #         raise ValueError('Ma`lumot bor')
    #     super(WishList, self).save(*args, **kwargs)
