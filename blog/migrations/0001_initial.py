# Generated by Django 3.2.2 on 2021-05-12 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('content', models.TextField(max_length=5000)),
                ('author', models.CharField(max_length=30)),
                ('category', models.CharField(default='blog', max_length=50)),
                ('upload_date', models.DateTimeField()),
                ('viewsCount', models.IntegerField(default=0)),
                ('thumbnail', models.ImageField(upload_to='blog/images')),
                ('is_featured', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-upload_date'],
            },
        ),
    ]