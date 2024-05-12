from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import CustomUser

# Create your models here.

class Campus(models.Model):
    CAMPUS_CHOICES = [
        ('Casuarina', 'Casuarina'),
        ('Sydney', 'Sydney'),
        ('External', 'External'),
    ]
    campus = models.CharField(
        max_length=20,
        choices=CAMPUS_CHOICES,
        verbose_name='Campus Name',
        primary_key=True,
    )
    
    def __str__(self):
        return self.campus

class Course(models.Model):
    COURSE_CHOICES = [
        ('Chemical Engineering', 'Chemical Engineering'),
        ('Civil and Structural Engineering', 'Civil and Structural Engineering'),
        ('Electrical and Electronics Engineering', 'Electrical and Electronics Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Computer Science', 'Computer Science'),
        ('Cyber Security', 'Cyber Security'),
        ('Data Science', 'Data Science'),
        ('Information Systems and Data Science', 'Information Systems and Data Science'),
        ('Software Engineering', 'Software Engineering'),
    ]  
    course = models.CharField(
        max_length=50,
        choices=COURSE_CHOICES,
        verbose_name='Course Name',
        primary_key=True,
    )
    
    def __str__(self):
        return self.course
    
class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Artificial Intelligence, Machine Learning and Data Science', 'Artificial Intelligence, Machine Learning and Data Science'),
        ('Biomedical Engineering and Health Informatics', 'Biomedical Engineering and Health Informatics'),
        ('Cyber Security', 'Cyber Security'),
    ]
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        verbose_name='Category Name',
        primary_key=True,
    )
    
    def __str__(self):
        return self.category
    
class Supervisor(models.Model):
    SUPERVISOR_CHOICES = [
        ('Bharanidharan Shanmugam', 'Bharanidharan Shanmugam'), 
        ('Yakub Sebastian', 'Yakub Sebastian'), 
        ('Sami Azam', 'Sami Azam'), 
        ('Asif Karim', 'Asif Karim'),
    ]
    supervisor = models.CharField(
        max_length=50,
        choices=SUPERVISOR_CHOICES,
        verbose_name='Supervisor Name',
        primary_key=True,
    )
    
    def __str__(self):
        return self.supervisor

class Thesis(models.Model):       
    topic_number = models.IntegerField(
        validators=[
            MinValueValidator(0),
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
    #date_created = models.DateTimeField(auto_now_add=True, verbose_name = 'Date Created')
    last_edited = models.DateTimeField(auto_now=True, verbose_name = 'Date Edited')
    # group_taker_limit = models.IntegerField(
    #     validators=[
    #         MinValueValidator(0),
    #         MaxValueValidator(20),
    #     ], 
    #     verbose_name='Number Limit of group takers', 
    #     null = True
    # )
    
    def __str__(self):
        return str(self.topic_number) + ' - ' + self.title 
        

# class  ThesisRequest(models.Model):
#     thesis_request_number = models.IntegerField( 
#         verbose_name= 'Thesis Request',
#         primary_key=True,
#     )
#     requested_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Requested by')
#     request_date = models.DateTimeField(auto_now_add=True, verbose_name='Request Date')
#     thesis_request = models.ForeignKey(Thesis, on_delete = models.CASCADE, verbose_name='Thesis Request')
    
#     def __str__(self):
#         return self.requested_by + ' - ' + self.thesis_request
       
# class GroupApplication(models.Model):
#     group_application_number = models.AutoField(
#         verbose_name='Group Application Number', 
#         primary_key=True
#     )
        
#     group = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Group', default='')
#     thesis = models.ForeignKey(Thesis, on_delete=models.PROTECT, verbose_name='Thesis', default='')
#     application_date = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.group + ' - ' + self.thesis