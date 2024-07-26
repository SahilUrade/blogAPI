from django.db import models


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Tag(models.Model):
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
