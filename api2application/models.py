from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# users
class User(models.Model):
    USER_TYPE = (
        (0, 'SUPER_ADMIN'),
        (1, 'NORMAL_ADMIN'),
        (2, 'NORMAL_USER')
    )

    USER_RATE = (
        (0, "Newbie"),
        (1, "Pupil"),
        (2, "Specialist"),
        (3, "Expert"),
        (4, "CandiDate Master"),
        (5, "Master"),
        (6, "Grand Master"),
        (7, "International Grand Master"),
        (8, "International Legendary Grand Master"),
        (9, "Admin"),
        (10, "Creator")
    )

    email_address = models.CharField(max_length=60, blank=False)
    password = models.CharField(max_length=60, blank=False)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=False)

    user_type = models.SmallIntegerField(choices=USER_TYPE, default=2)
    user_rate = models.SmallIntegerField(choices=USER_RATE, default=0)

    def __str__(self):
        return str(self.id) + "." + self.first_name + " " + self.last_name + " " + self.email_address


class Product(models.Model):
    title = models.CharField(max_length=50, blank=False)
    cost = models.DecimalField(decimal_places=3, max_digits=12)
    rate = models.IntegerField(default=0)  # between 0 and 5.
    user = models.ForeignKey('User', null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=400, default="description", blank=True)
    product_category = models.ForeignKey('ProductCategory', related_name="Products", null=True,
                                         on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " : " + str(self.user.id) + "." + self.user.email_address


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
    # slug = models.SlugField(unique=True, allow_unicode=True, blank=True)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE
    )

    class Meta:
        # unique_together = ('slug', 'parent',)
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

    # def get_all_picture_address(self):


class Picture(models.Model):
    name = models.CharField(max_length=25, blank=False)
    # image = models.ImageField(nam)
