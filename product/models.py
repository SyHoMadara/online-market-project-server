import uuid
from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from account.models import User


def get_image_profile_default():
    return 'files/images/products/default/default_image.jpg'


class Product(models.Model):
    id = models.UUIDField(verbose_name="UUID", default=uuid.uuid4, editable=False, primary_key=True)
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True)
    title = models.CharField(max_length=50, blank=False)
    cost = models.DecimalField(decimal_places=0, max_digits=12)
    rate = models.IntegerField(choices=[(i, i) for i in range(0, 6)])  # between 0 and 5.
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    image = models.ImageField(
        default=get_image_profile_default,
        verbose_name='Product Image',
        upload_to='files/images/products/'
    )
    description = models.CharField(
        max_length=400,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        'ProductCategory',
        related_name="Products",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # create slug
        self.slug = f'{slugify(self.user.email)}/{self.id.__str__()}'
        self.image.name = f'{self.id}_product_image.png'
        if not self.description or self.description == "":
            self.description = f'{self.title} with rate {self.rate.__str__()} you can pay for it {self.cost.__str__()}$'
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title + " : " + self.user.email


# DIGITAL_TYPE = (
#     (-1, "Another"),
#     (0, "Phones"),
#     (1, "Laptop"),
#     (3, "Accessories"),
#     (4, "TV"),
# )
#
# HOME_APPLICATION_TYPE = (
#     (-1, "Another"),
#     (0, "Washing Machine"),
#     (1, "Dishwasher"),
#     (2, "Refrigerators"),
#     (3, "Vacuum Cleaners"),
#     (4, "Kitchen appliances")  # like dishes , fork , etc.
# )
#
# VEHICLE_TYPE = (
#     (-1, "Another"),
#     (0, "Automobile"),
#     (1, "Motorcycle"),
#     (2, "Boat and Tools")
# )
#
# GENERAL_PRODUCT_TYPE = (
#     (-1, "Another"),
#     (0, DIGITAL_TYPE),
#     (1, "Builds"),
#     (2, HOME_APPLICATION_TYPE),
#     (3, VEHICLE_TYPE),
#     (4, "Self Tools"),
#
# )
class ProductCategory(MPTTModel):
    name = models.CharField(max_length=200)
    id = models.UUIDField(verbose_name="UUID", default=uuid.uuid4, editable=False, primary_key=True)
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True)
    is_root = models.BooleanField(default=False)
    parent = TreeForeignKey(
        'ProductCategory',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('name', 'parent')
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        # create slug with self.name and parents names recursively
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        self.slug = '/'.join(list(map(slugify, full_path[::-1])))  # digital-and-tools/laptop
        # set is_root value
        self.is_root = not bool(self.parent)
        super().save(*args, **kwargs)

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' / '.join(full_path[::-1])  # Digital and Tools/Laptop
