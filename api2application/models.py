from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def creat_user(self, email, first_name, last_name, password=None):
        if not email:
            return ValueError("User must have email address")
        elif not (first_name and last_name):
            return ValueError("First name and Last name required")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def creat_superuser(self, email, first_name, last_name, password=None):
        user = self.creat_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_supperuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    # user properties
    email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
    first_name = models.CharField(max_length=20, verbose_name="First name")
    last_name = models.CharField(max_length=20, verbose_name="Last name")
    phone_number = models.CharField(max_length=14, null=True, blank=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    # picture = models.ImageField()

    # permutations
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_supperuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True




class Product(models.Model):
    title = models.CharField(max_length=50, blank=False)
    cost = models.DecimalField(decimal_places=0, max_digits=12)
    rate = models.IntegerField(default=0)  # between 0 and 5.
    user = models.ForeignKey('User', blank=True, null=True,on_delete=models.CASCADE)
    description = models.CharField(max_length=400, default="description", blank=True)
    product_category = models.ForeignKey('ProductCategory', related_name="Products", null=True,
                                         on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " : " + self.user.id.__str__() + "." + self.user.email.__str__()


class ProductCategory(MPTTModel):
    name = models.CharField(max_length=200)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' ==> '.join(full_path[::-1])


class Pictures(models.Model):
    product = models.OneToOneField('Product', on_delete=models.CASCADE)
