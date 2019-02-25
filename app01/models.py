from django.db import models

# Create your models here.
class Book(models.Model):
    '''
    书籍 结构表
    '''
    bid = models.AutoField(primary_key=True)
    bname = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    pub_date = models.DateTimeField()
    publish = models.ForeignKey('Publish',on_delete=models.CASCADE)
    authors = models.ManyToManyField('Author')

    def __str__(self):
        return self.bname

class Publish(models.Model):
    '''
    出版社 结构表
    '''
    pid = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=32)
    email = models.CharField(max_length=32)

    def __str__(self):
        return self.pname
class Author(models.Model):
    '''
    作者 结构表
    '''
    aid = models.AutoField(primary_key=True)
    aname = models.CharField(max_length=32)
    age = models.IntegerField()
    phone = models.IntegerField()
    a_info = models.OneToOneField('Author_info',on_delete=models.CASCADE)

    def __str__(self):
        return self.aname

class Author_info(models.Model):
    '''
    作者详情信息 结构表
    '''
    addr = models.CharField(max_length=32)
    tel = models.IntegerField()

    # author=models.OneToOneField("Author",on_delete=models.CASCADE)
    def __str__(self):
        return self.addr

class User_info(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    email = models.EmailField()