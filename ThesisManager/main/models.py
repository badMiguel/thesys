from django.db import models

# Create your models here.

class Campus(models.Model):
    campus = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.campus)

class Course(models.Model):
    course = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.course)
    
class Thesis(models.Model):           
    topic_number = models.IntegerField()
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    supervisor = models.CharField(max_length=100)
    description = models.TextField()
    course = models.ManyToManyField(Course)
    campus = models.ManyToManyField(Campus)
        
    def __str__(self):
        return str(self.topic_number) + ' - ' + self.title 
        
def create_campus():
    casuarina = Campus.objects.create(campus='Casuarina')
    sydney = Campus.objects.create(campus='Sydney')
    external = Campus.objects.create(campus='External')    
    
    return casuarina, sydney, external
        
def create_course():
    chemical = Course.objects.create(course= 'Chemical Engineering')
    civil = Course.objects.create(course= 'Civil and Structural Engineering')
    electrical = Course.objects.create(course= 'Electrical and Electronics Engineering')
    mechanical = Course.objects.create(course= 'Mechanical Engineering')
    computer_science = Course.objects.create(course= 'Computer Science')
    cyber_security = Course.objects.create(course= 'Cyber Security')
    data_science = Course.objects.create(course= 'Data Science')
    information_system = Course.objects.create(course= 'Information Systems and Data Science')
    software = Course.objects.create(course= 'Software Engineering')
    
    return chemical, civil, electrical, mechanical, computer_science, cyber_security, data_science, information_system, software
        
def create_thesis():   
    casuarina, sydney, external = create_campus()
    chemical, civil, electrical, mechanical, computer_science, cyber_security, data_science, information_system, software = create_course()
    
    thesis_1= Thesis.objects.create(
        topic_number=1,       
        title= 'Machine learning approaches for Cyber Security',
        category = 'Artificial Intelligence, Machine Learning and Data Science',
        supervisor= 'Bharanidharan Shanmugam',
        description='As we use internet more, the data produced by us is enormous. But are these data being secure? The goal of applying machine learning or intelligence is to better risk modelling and prediction and for an informed decision support. Students will be working with either supervised or unsupervised machine learning approaches to solve the problem/s in the broader areas of Cyber Security.'
    ) 
    
    thesis_1.campus.add(casuarina, sydney, external)
    thesis_1.course.add(computer_science, information_system, software)
     
    thesis_2 = Thesis.objects.create(
        topic_number= 9,
        title= 'Informetrics applications in multidisciplinary domain',
        category = 'Artificial Intelligence, Machine Learning and Data Science',
        supervisor= 'Yakub Sebastian',
        description='Informetrics studies are concerned with the quantitative aspects of information. The applications of advanced machine learning, information retrieval, network science and bibliometric techniques on various information artefact have contributed fresh insights into the evolutionary nature of research fields. This project aims at discovering informetric properties of multidisciplinary research literature using various machine learning, network analysis, data visualisation and data wrangling tools.'
    )
    
    thesis_2.campus.add(casuarina, sydney, external)
    thesis_2.course.add(computer_science, cyber_security, data_science, information_system, software)
     
    thesis_3 = Thesis.objects.create(
        topic_number=16,
        title='Development of a Virtual Reality System to Test Binaural Hearing',
        category = 'Biomedical Engineering and Health Informatics',
        supervisor='Sami Azam',
        description='A virtual reality system could be used to objectively test the binaural hearing ability of humans (the ability to hear stereo and locate the direction and distance of sound). This project aims to design, implement and evaluate a VR system using standard off the shelf components (VR goggle and headphones) and standard programming techniques.'
    )
    
    thesis_3.campus.add(casuarina, external)
    thesis_3.course.add(electrical, computer_science, software)
    
    thesis_4 = Thesis.objects.create(
        topic_number=41,
        title='Current trends on cryptomining and its potential impact on cryptocurrencies',
        category = 'Cyber Security',
        supervisor= 'Sami Azam',
        description= "Cryptomining is the process of mining crypto currencies by running a sequence of algorithms. Traditionally, to mine new crypto coins, a person (or group of people) would buy expensive computers and spend a lot of time and money running them to perform the difficult calculations to generate crypto coins. Some website owners have started taking a different approach; they have put the software which runs those difficult calculations into their website's Javascript. This then causes the computers belonging to the visitors of their website to run those calculations for them, instead of running them themselves. In other words, when you visit a website with an embedded crypto-miner in it, your computer and electricity is used to try to generate crypto-coins for the owners of that website. Although there are various measures being applied to stop these illegitimate minings, the trend is still increasing. This research aims to find out potential gaps in current methodologies and develop a solution that can fulfil the gap. It also aims to find out: (1) What type crypto mining methodologies are being applied?, (2) Apart from crypto-mining, what other security risks may it introduce? For example: cryptojacking,  and (3) How current web standards are tackling this problem?"
    )
    
    thesis_4.campus.add(casuarina, sydney, external)
    thesis_4.course.add(computer_science, cyber_security, software)
    
    thesis_5 = Thesis.objects.create(
        topic_number=176,
        title='Artificial Intelligence in Health Informatics',
        category = 'Artificial Intelligence, Machine Learning and Data Science',   
        supervisor= 'Asif Karim',
        description='The project aims to use multiple publicly available health datasets to formulate a different dataset that may have features from the original set along with new ones developed through feature engineering. The dataset will then be used to build predictive model based on both general and deep learning based algorithm. The findings will be analysed and compared to similar research works.'
    )
    
    thesis_5.campus.add(casuarina, sydney, external)
    thesis_5.course.add(electrical, computer_science, data_science, software)
    
    thesis_6 = Thesis.objects.create(
        topic_number= 180,
        title='Unsupervised Model Development from Autism Screening Data',
        category = 'Artificial Intelligence, Machine Learning and Data Science',
        supervisor='Asif Karim',
        description='The proposed system will present a two-cluster solution from a given dataset which will group toddlers based on multiple common medical traits. In depth literature survey of similar studies, both supervised and unsupervised will be carried out before the cluster-based model is implemented. The solution will be validated using both External and Internal validation measures and statistical significance tests.'
    )    

    thesis_6.campus.add(casuarina, sydney, external)
    thesis_6.course.add(electrical, computer_science, data_science, software)
    
    thesis_7 = Thesis.objects.create(
        topic_number= 226,
        title= 'Applying Artificial Intelligence to solve real world problems',
        category = 'Artificial Intelligence, Machine Learning and Data Science',
        supervisor= 'Bharanidharan Shanmugam',
        description='Artificial Intelligence has been used in many applications to solve certain problems through out the academia and the industry – from electricity to writing text. AI has a multitude of applications and this project will pick up a problem and explore the applications of AI with minimal human intervention. Examples of applications include -building a bot, predicting the power usage, spam filtering and the list is endless.'
    )    
    
    thesis_7.campus.add(casuarina, sydney, external)
    thesis_7.course.add(chemical,civil,electrical,mechanical,computer_science,cyber_security,data_science,information_system,software)
    
def delete_data():
    Campus.objects.all().delete()
    Course.objects.all().delete()
    Thesis.objects.all().delete()