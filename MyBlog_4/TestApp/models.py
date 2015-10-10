from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=30)
    content_body= models.TextField()
    timestamp=models.DateTimeField()
    version=models.IntegerField(default=0)

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(id=id)

    @classmethod
    def exists(cls, id):
        return len(cls.objects.filter(id=id)) > 0
