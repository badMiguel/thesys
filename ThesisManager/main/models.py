from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import CustomUser

# Create your models here.

class Campus(models.Model):
    campus = models.CharField(
        max_length=20,
        verbose_name='Campus Name',
        primary_key=True,
    )
    
    def __str__(self):
        return self.campus

class Course(models.Model):
    course = models.CharField(
        max_length=50,
        verbose_name='Course Name',
        primary_key=True,
    )
    
    def __str__(self):
        return self.course
    
class Category(models.Model):
    category = models.CharField(
        max_length=100,
        verbose_name='Category Name',
        primary_key=True,
    )
    
    def __str__(self):
        return self.category
    
class Supervisor(models.Model):
    supervisor = models.CharField(
        max_length=50,
        verbose_name='Supervisor Name',
        primary_key=True,
    )
    
    def __str__(self):
        return self.supervisor
# ABSTRACT BASE CLASSES - FOR MODEL INHERITANCE
class ThesisBase(models.Model):       
    topic_number = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000),
        ],
        verbose_name='Thesis Number',
        primary_key=True,
    )
    title = models.CharField(max_length=100, verbose_name='Thesis Title',)
    description = models.TextField(verbose_name='Thesis Description')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Category Name')
    supervisor = models.ForeignKey(Supervisor, on_delete= models.PROTECT, verbose_name='Supervisor Name')
    course = models.ManyToManyField(Course, verbose_name='Course Name')
    campus = models.ManyToManyField(Campus, verbose_name='Campus Name',)

    group_taker_limit = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(20),
        ], 
        verbose_name='Number Limit of group takers', 
        null = True,
        blank=True
    )

    class Meta:
        abstract = True
        ordering = ['topic_number']       
        
class ThesisRequestBase(models.Model):    
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected')        
    ]    
    REQUEST_CHOICES = [
        ('add', 'add'),
        ('modify', 'modify'),
        ('delete', 'delete'),
    ]    

    request_date = models.DateTimeField(auto_now_add=True, verbose_name = 'Date Requested')
    requested_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Requested by', )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name='Status',
        default='pending'
    )
    
    class Meta:
        abstract = True

class Thesis(ThesisBase):
    date_created = models.DateTimeField(auto_now_add=True, verbose_name = 'Date Created')
    last_edited = models.DateTimeField(auto_now=True, verbose_name = 'Date Edited')

    def __str__(self):
        return f'{str(self.topic_number)} - {self.title}' 

class ThesisRequestAdd(ThesisBase, ThesisRequestBase):
    request_type = models.CharField(
        max_length=10,
        choices=ThesisRequestBase.REQUEST_CHOICES,
        verbose_name='Request Type',
        default='add'
    )
    
    def __str__(self):
        return f'{str(self.topic_number)} - {self.title} - {self.requested_by}' 
    
class ThesisRequestModify(ThesisBase, ThesisRequestBase):
    request_type = models.CharField(
        max_length=10,
        choices=ThesisRequestBase.REQUEST_CHOICES,
        verbose_name='Request Type',
        default='modify'
    )
    
    def __str__(self):
        return f'{str(self.topic_number)} - {self.title} - {self.requested_by}' 
    
class ThesisRequestDelete(ThesisBase, ThesisRequestBase):
    request_type = models.CharField(
        max_length=10,
        choices=ThesisRequestBase.REQUEST_CHOICES,
        verbose_name='Request Type',
        default='delete'
    )
    
    def __str__(self):
        return f'{str(self.topic_number)} - {self.title} - {self.requested_by}' 
           
class GroupApplicationBase(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
        ('cancelled', 'cancelled')        
    ]    
    group_application_id = models.AutoField(verbose_name='Group Application ID', primary_key=True)
    thesis = models.ForeignKey(Thesis, on_delete=models.CASCADE, verbose_name='Thesis')
    group = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Group')
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Status', default='pending')

    class Meta:
        abstract = True

class GroupApplication(GroupApplicationBase):
    class Meta:
        unique_together = ('thesis', 'group')
    
    def __str__(self):
        return f'{self.group} - {self.thesis}'
        