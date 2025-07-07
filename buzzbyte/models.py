from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Blog(models.Model):
        id = models.AutoField(primary_key=True)
        title = models.CharField(max_length=200)
        content = models.TextField()
        description = models.TextField()
        category=models.CharField(max_length=50)
        tags=models.CharField(max_length=50)
        imgurl=models.CharField(max_length=200)
        authname=models.CharField(max_length=50)
        date=models.DateTimeField(auto_now_add=True)
        

        def __str__(self):
            return self.title
    
class User(AbstractUser):
    pass
    
class Comment(models.Model):
    # ForeignKey to Blog and User models
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.blog.title}"