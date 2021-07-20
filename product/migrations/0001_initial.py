# Generated by Django 3.2.5 on 2021-07-17 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='UUID')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, unique=True)),
                ('is_root', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productcategory')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'unique_together': {('name', 'parent')},
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, unique=True)),
                ('title', models.CharField(max_length=50)),
                ('cost', models.DecimalField(decimal_places=0, default=0, max_digits=12)),
                ('image', models.ImageField(default='product/default/default_image.png', upload_to='products/', verbose_name='Image')),
                ('description', models.CharField(blank=True, max_length=400, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Products', to='product.productcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]