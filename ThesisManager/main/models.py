from django.db import models

# Create your models here.

class Campus(models.Model):
    campus = models.CharField(max_length=20)
    
    def __str__(self):
        return self.campus

class Course(models.Model):
    course = models.CharField(max_length=50)
    
    def __str__(self):
        return self.course
    
class Category(models.Model):
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category
    
class Supervisor(models.Model):
    supervisor = models.CharField(max_length=50)
    
    def __str__(self):
        return self.supervisor
    
class Thesis(models.Model):           
    topic_number = models.IntegerField()
    title = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    supervisor = models.ManyToManyField(Supervisor)
    description = models.TextField()
    course = models.ManyToManyField(Course)
    campus = models.ManyToManyField(Campus)
        
    def __str__(self):
        return str(self.topic_number) + ' - ' + self.title 
        
def create_campus():
    campus_data = [
        {"campus":'Casuarina'},
        {"campus":'Sydney'},
        {"campus":'External'}    
    ]
    
    campus = [Campus(**data) for data in campus_data]
    Campus.objects.bulk_create(campus)
        
def create_course():
    course_data = [
        {"course" : 'Chemical Engineering'},
        {"course" : 'Civil and Structural Engineering'},
        {"course" : 'Electrical and Electronics Engineering'},
        {"course" : 'Mechanical Engineering'},
        {"course" : 'Computer Science'},
        {"course" : 'Cyber Security'},
        {"course" : 'Data Science'},
        {"course" : 'Information Systems and Data Science'},
        {"course" : 'Software Engineering'},
    ]    

    course = [Course(**data) for data in course_data]
    Course.objects.bulk_create(course)
        
def create_category():
    category_data = [
        {"category" :'Artificial Intelligence, Machine Learning and Data Science'},
        {"category" :'Biomedical Engineering and Health Informatics'},
        {"category" :'Cyber Security'},
    ]
    
    category = [Category(**data) for data in category_data]
    Category.objects.bulk_create(category)
    
def create_supervisor():
    supervisor_data = [
        {'supervisor': 'Yakub Sebastian'},
        {'supervisor': 'Bharanidharan Shanmugam'},
        {'supervisor': 'Sami Azam'},
        {'supervisor': 'Asif Karim'},
    ]
    
    supervisor = [Supervisor(**data) for data in supervisor_data]
    Supervisor.objects.bulk_create(supervisor)
    
def create_thesis():   
    create_campus()
    create_course()
    create_category()
    create_supervisor()

    thesis_data = [
        {
            'topic_number': 1,       
            'title' : 'Machine learning approaches for Cyber Security',
            'category': 'Artificial Intelligence, Machine Learning and Data Science',
            'supervisor': 'Bharanidharan Shanmugam',
            'description':"As we use internet more, the data produced by us is enormous. But are these data being secure? The goal of applying machine learning or intelligence is to better risk modelling and prediction and for an informed decision support. Students will be working with either supervised or unsupervised machine learning approaches to solve the problem/s in the broader areas of Cyber Security.",
            'campus': ['Casuarina', 'Sydney', 'External'],
            'course': ['Computer Science', 'Information Systems and Data Science', 'Software Engineering'],
        },
        {
            'topic_number': 9,
            'title':'Informetrics applications in multidisciplinary domain',
            'category': 'Artificial Intelligence, Machine Learning and Data Science',
            'supervisor': 'Yakub Sebastian',
            'description':"Informetrics studies are concerned with the quantitative aspects of information. The applications of advanced machine learning, information retrieval, network science and bibliometric techniques on various information artefact have contributed fresh insights into the evolutionary nature of research fields. This project aims at discovering informetric properties of multidisciplinary research literature using various machine learning, network analysis, data visualisation and data wrangling tools.",
            'campus': ['Casuarina', 'Sydney', 'External'],
            'course': ['Computer Science', 'Cyber Security', 'Data Science', 'Information Systems and Data Science', 'Software Engineering'],
        },
        {
            'topic_number':16,
            'title':'Development of a Virtual Reality System to Test Binaural Hearing',
            'category': 'Biomedical Engineering and Health Informatics',
            'supervisor':'Sami Azam',
            'description':"A virtual reality system could be used to objectively test the binaural hearing ability of humans (the ability to hear stereo and locate the direction and distance of sound). This project aims to design, implement and evaluate a VR system using standard off the shelf components (VR goggle and headphones) and standard programming techniques.",
            'campus': ['Casuarina', 'External'],
            'course': ['Electrical and Electronics Engineering', 'Computer Science', 'Software Engineering'],
        },
        {
            'topic_number':41,
            'title':'Current trends on cryptomining and its potential impact on cryptocurrencies',
            'category': 'Cyber Security',
            'supervisor':'Sami Azam',
            'description': "Cryptomining is the process of mining crypto currencies by running a sequence of algorithms. Traditionally, to mine new crypto coins, a person (or group of people) would buy expensive computers and spend a lot of time and money running them to perform the difficult calculations to generate crypto coins. Some website owners have started taking a different approach; they have put the software which runs those difficult calculations into their website's Javascript. This then causes the computers belonging to the visitors of their website to run those calculations for them, instead of running them themselves. In other words, when you visit a website with an embedded crypto-miner in it, your computer and electricity is used to try to generate crypto-coins for the owners of that website. Although there are various measures being applied to stop these illegitimate minings, the trend is still increasing. This research aims to find out potential gaps in current methodologies and develop a solution that can fulfil the gap. It also aims to find out: (1) What type crypto mining methodologies are being applied?, (2) Apart from crypto-mining, what other security risks may it introduce? For example: cryptojacking,  and (3) How current web standards are tackling this problem?",
            'campus': ['Casuarina', 'Sydney', 'External'],
            'course': ['Computer Science', 'Cyber Security', 'Software Engineering'],
        },
        {
            'topic_number':176,
            'title':'Artificial Intelligence in Health Informatics',
            'category': 'Artificial Intelligence, Machine Learning and Data Science',
            'supervisor':'Asif Karim',
            'description':"The project aims to use multiple publicly available health datasets to formulate a different dataset that may have features from the original set along with new ones developed through feature engineering. The dataset will then be used to build predictive model based on both general and deep learning based algorithm. The findings will be analysed and compared to similar research works.",
            'campus': ['Casuarina', 'Sydney', 'External'],
            'course': ['Electrical and Electronics Engineering', 'Computer Science', 'Data Science', 'Software Engineering'],
        },
        {
            'topic_number': 180,
            'title':'Unsupervised Model Development from Autism Screening Data',
            'category': 'Artificial Intelligence, Machine Learning and Data Science',
            'supervisor':'Asif Karim',
            'description':'The proposed system will present a two-cluster solution from a given dataset which will group toddlers based on multiple common medical traits. In depth literature survey of similar studies, both supervised and unsupervised will be carried out before the cluster-based model is implemented. The solution will be validated using both External and Internal validation measures and statistical significance tests.',
            'campus': ['Casuarina', 'Sydney', 'External'],
            'course': ['Electrical and Electronics Engineering', 'Computer Science', 'Data Science', 'Software Engineering'],
        },    
        {
            'topic_number': 226,
            'title':'Applying Artificial Intelligence to solve real world problems',
            'category': 'Artificial Intelligence, Machine Learning and Data Science',
            'supervisor':'Bharanidharan Shanmugam',
            'description':'Artificial Intelligence has been used in many applications to solve certain problems through out the academia and the industry – from electricity to writing text. AI has a multitude of applications and this project will pick up a problem and explore the applications of AI with minimal human intervention. Examples of applications include -building a bot, predicting the power usage, spam filtering and the list is endless.',
            'campus': ['Casuarina', 'Sydney', 'External'],
            'course': ['Chemical Engineering', 'Civil and Structural Engineering', 'Electrical and Electronics Engineering', 'Mechanical Engineering', 'Computer Science', 'Cyber Security', 'Data Science', 'Information Systems and Data Science', 'Software Engineering'],
        }
    ]
    
    thesis_objects =  []
    for thesis_info in thesis_data:
            
        thesis = Thesis(
            topic_number = thesis_info['topic_number'],
            title = thesis_info['title'],
            description = thesis_info['description'],
        )       
        
        thesis_objects.append(thesis)   
    Thesis.objects.bulk_create(thesis_objects)    
    print(thesis_objects)

    for thesis_info in thesis_data:
        supervisor = Supervisor.objects.get(supervisor=thesis_info['supervisor'])
        category = Category.objects.get(category=thesis_info['category'])
        courses = Course.objects.filter(course=thesis_info['course'])
        campuses = Campus.objects.filter(campus=thesis_info['campus'])
        
        thesis.supervisor.set([supervisor])
        thesis.category.set([category]) 
        thesis.course.add(*courses)
        thesis.campus.add(*campuses)

def delete_data():
    Campus.objects.all().delete()
    Course.objects.all().delete()
    Category.objects.all().delete()
    Supervisor.objects.all().delete()
    Thesis.objects.all().delete()