
from typing import ClassVar
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
from ckeditor.fields import RichTextField
# Create your models here.

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    title= models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=False)
    content = RichTextField(blank= True, null= True)
    author = models.CharField(max_length=30)
    category = models.CharField(max_length=50, default='blog')
    upload_date = models.DateTimeField()
    viewsCount= models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to= 'blog/images')
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
 
    class Meta:
        ordering = ['-upload_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blogpost", kwargs={"slug": self.slug})

 
class BlogComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by " + self.user.username