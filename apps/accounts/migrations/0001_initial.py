# Generated by Django 5.2.1 on 2025-05-16 14:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان آدرس')),
                ('recipient_name', models.CharField(max_length=100, verbose_name='نام گیرنده')),
                ('phone', models.CharField(max_length=15, verbose_name='شماره تماس')),
                ('address', models.TextField(verbose_name='آدرس')),
                ('postal_code', models.CharField(max_length=10, verbose_name='کد پستی')),
                ('city', models.CharField(max_length=100, verbose_name='شهر')),
                ('address_type', models.CharField(choices=[('home', 'منزل'), ('work', 'محل کار'), ('other', 'سایر')], default='home', max_length=10, verbose_name='نوع آدرس')),
                ('is_default', models.BooleanField(default=False, verbose_name='آدرس پیش\u200cفرض')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'آدرس',
                'verbose_name_plural': 'آدرس\u200cها',
                'ordering': ['-is_default', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='شماره تماس')),
                ('address', models.TextField(blank=True, null=True, verbose_name='آدرس')),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='کد پستی')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='شهر')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='تصویر پروفایل')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پروفایل',
                'verbose_name_plural': 'پروفایل\u200cها',
            },
        ),
    ]
