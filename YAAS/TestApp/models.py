from django.db import models

class Auction(models.Model):
    title   = models.CharField(max_length="20")
    description = models.TextField()
    seller = models.CharField(max_length="30")
    minimun_price = models.DecimalField(max_digits="7",decimal_places="2")
    deadline = models.DateTimeField()
    status = models.CharField(max_length="3")
    last_bid = models.DecimalField(max_digits="7",decimal_places="2")
    last_bider = models.CharField(max_length="30", blank="True")

    @classmethod
    def exists(cls,title):
        return len(cls.objects.filter(title=title))>0
    @classmethod
    def exists(cls,id):
        return len(cls.objects.filter(id=id))>0

    @classmethod
    def get_by_id(cls,id):
        return  cls.objects.get(id=id)

    @classmethod
    def get_by_title(cls,title):
        return cls.objects.get(title=title)


