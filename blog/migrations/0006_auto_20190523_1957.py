# Generated by Django 2.2 on 2019-05-23 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_merge_20190519_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='img',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='类别图片'),
        ),
        migrations.AlterField(
            model_name='link',
            name='linkurl',
            field=models.URLField(verbose_name='网址'),
        ),
    ]