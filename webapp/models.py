from django.db import models
from django.contrib.auth.models import AbstractUser
import json

# User
class User(AbstractUser):
    email = models.EmailField(blank=True, null=True, verbose_name='e-mail')
    mobile = models.CharField(max_length=10, blank=True, null=True, unique=True, verbose_name='numéro de telephone')

    class Meta:
        verbose_name = 'utilisateur'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username
    
class Difficulty(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='nom de difficulté')
    index = models.IntegerField(default=1,verbose_name='ordre de difficulté')

    class Meta:
        verbose_name = 'difficulté'
        verbose_name_plural = verbose_name
        ordering = ['index',]

    def __str__(self):
        return self.name

class Need(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='nom de besoin')
    index = models.IntegerField(default=1,verbose_name='ordre de besoin')
    difficulty = models.ManyToManyField(Difficulty, verbose_name='difficulté')
    
    class Meta:
        verbose_name = 'besoin'
        verbose_name_plural = verbose_name
        ordering = ['index',]

    def __str__(self):
        return self.name

#type de technologie
class Technotype(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='nom de type')
    index = models.IntegerField(default=1,verbose_name='ordre de type')
    difficulty = models.ManyToManyField(Difficulty, verbose_name='difficulté')

    class Meta:
        verbose_name = 'type de technologie'
        verbose_name_plural = verbose_name
        ordering = ['index',]

    def __str__(self):
        return self.name


class Technology(models.Model):

    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='nom')       
    difficulty = models.ManyToManyField(Difficulty, verbose_name='difficulté')
    technotype = models.ManyToManyField(Technotype, blank=True, verbose_name='type de technologie')
    need = models.ManyToManyField(Need, blank=True, verbose_name='besoin')
    
    desc = models.TextField(null=True, blank=True,verbose_name='description')
    price = models.CharField(max_length=100,null=True, blank=True,verbose_name='prix')
    source = models.CharField(max_length=100, null=True, blank=True,verbose_name='source')
    article = models.TextField(null=True, blank=True, verbose_name='article')
    company = models.CharField(max_length=100, null=True, blank=True, verbose_name='entreprise')
    
    video = models.TextField(blank=True,null=True)    
    image = models.ImageField(upload_to='technologies/', default= 'technologies/default.jpg', verbose_name='url image', null = True)
   
    # is the techno visible on the website?
    # has to be set to true after a form submission
    # in order to see the techno on the website
    show = models.BooleanField(default=True) 
    
    class Meta:
        verbose_name = 'technologie'
        verbose_name_plural = verbose_name
        ordering = ['id']
    
    def get_type(self):
        type_list = self.technotype.all()
        tyname_list = []
        for ty in type_list:
            tyname_list.append(ty.name)
        return ', '.join(str(e) for e in tyname_list)
    def get_need(self):
        need_list = self.need.all()
        nename_list = []
        for ne in need_list:
            nename_list.append(ne.name)
        return ', '.join(str(e) for e in nename_list)

    def __str__(self):
        return self.name
    

    
#Items of wish list
class Caritem(models.Model):
    technology = models.ForeignKey(Technology, verbose_name='items dans liste de souhaits')

    class Meta:
        verbose_name = 'items dans liste de souhaits'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)

#wish list
class Cart(object):
    def __init__(self):
        self.items = []
        self.length = 0

    def add(self, technology):
        for item in self.items:
            if item.technology.id == technology.id:
                return
        self.length += 1
        self.items.append(Caritem(technology = technology))
