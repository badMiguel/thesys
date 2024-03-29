from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')







class Thesis:
    def __init__(self, topic_number, title, campus, course, category, supervisor):
            
        self.topic_number = topic_number
        self.title = title
        self.campus = campus
        self.course = course
        self.category = category
        self.supervisor = supervisor

def thesis_list():
    topics = []
    
    campuses = ['Casuarina', 'Sydney', 'External']
    area = {
        'chemical': 'Chemical Engineering',
        'civil' : 'Civil and Structural Engineering',
        'electrical' :'Electrical and Electronics Engineering',
        'mechanical' : 'Mechanical Engineering',
        'computer' : 'Computer Science',

        'data' : 'Data Science',
        'information' : 'Information Systems and Data Science',
        'software' : 'Software Engineering',
        } 
    categories = {
        'artificial' : 'Artificial Intelligence, Machine Learning and Data Science',
        'biomedical' : 'Biomedical Engineering and Health Informatics',
        'cyber' : 'Cyber Security',
    }

    topics.append(Thesis(
        topic_number=1,       
        title= 'Machine learning approaches for Cyber Security',
        campus = campuses,
        course= [area['computer'], area['software']],
        category= categories['artificial'],
        supervisor= 'Bharanidharan Shanmugam'
    )) 
     
    topics.append(Thesis(
        topic_number= 9,
        title= 'Informetrics applications in multidisciplinary domain',
        campus= campuses,
        course= [area['computer'], area['cyber'], area['data'], area['information'], area['software']],
        category= categories['artificial'],
        supervisor= 'Yakub Sebastian',
    ))
     
    topics.append(Thesis(
        topic_number=16,
        title='Development of a Virtual Reality System to Test Binaural Hearing',
        campus=[campuses[0], campuses[2]],
        course=[area['electrical'], area['computer'],  area['software']],
        category=categories['biomedical'],
        supervisor='Sami Azam',
    ))
    
    topics.append(Thesis(
        topic_number=41,
        title='Current trends on cryptomining and its potential impact on cryptocurrencies',
        campus=campuses,
        course=[area['computer'], area['cyber'], area['software']],
        category= categories['cyber'],
        supervisor= 'Sami Azam',
    ))
    
    topics.append(Thesis(
        topic_number=,
        title=,
        campus=,
        course=,
        category=,
        supervisor=,
    ))
    
    topics.append(Thesis(
        topic_number=,
        title=,
        campus=,
        course=,
        category=,
        supervisor=,
    ))    
    
    