# Generated by Django 4.2.3 on 2023-12-01 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_tag_remove_image_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, to='gallery.tag'),
        ),
    ]