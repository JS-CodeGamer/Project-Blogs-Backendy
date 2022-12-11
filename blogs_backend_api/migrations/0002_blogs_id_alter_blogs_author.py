# Generated by Django 4.1.3 on 2022-12-05 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs_backend_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogs',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogs',
            name='author',
            field=models.CharField(max_length=200, verbose_name='Author Username'),
        ),
    ]
