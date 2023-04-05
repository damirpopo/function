from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission


class MyUserManager(BaseUserManager):
    def _create_user(self, email, FIO, password, **extra_fields):
        if not email:
            raise ValueError("вы не вели маил")
        if not FIO:
            raise ValueError("вы не вели фИО")
        user = self.model(
            email=self.normalize_email(email),
            username=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password):
        return self._create_user(email, password)

    def create_superuser(self, email, password):
        return self._create_user(email, password, is_staff=True, is_superuser=True)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    FIO = models.CharField(max_length=500)
    gender = models.CharField(max_length=400)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='api_users',
        related_query_name='api_user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='api_users',
        related_query_name='api_user',
    )

class Category(models.Model):
    name = models.CharField(max_length=90)


class Product(models.Model):
    name = models.CharField(max_length=40)
    author = models.CharField(max_length=60)
    country = models.CharField(max_length=90)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Cart(models.Model):
    name = models.ForeignKey(Product,on_delete=models.CASCADE)

class Order(models.Model):
    name = models.ForeignKey(Cart, on_delete=models.CASCADE)
    price = models.IntegerField()


