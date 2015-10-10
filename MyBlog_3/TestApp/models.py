from django.db import models

class Article(models.Model):
    name    = models.CharField(max_length=30, primary_key=True)
    content = models.TextField()

    @classmethod
    def getByName(cls, name):
        return cls.objects.get(name=name)

    @classmethod
    def exists(cls, name):
        return len(cls.objects.filter(name=name)) > 0

class Blog(models.Model):
    title = models.CharField(max_length=30)
    content_body= models.TextField()
    timestamp=models.DateTimeField()


    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(id=id)

    @classmethod
    def exists(cls, id):
        return len(cls.objects.filter(id=id)) > 0
