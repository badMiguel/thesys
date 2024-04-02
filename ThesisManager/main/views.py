from django.shortcuts import render
from .models import Thesis, create_thesis, delete_data


def home(request):
    return render(request, 'main/home.html')

def about_us(request):
    pass

def thesis_details(request):
    pass

def thesis_list(request):
    # Deletes any existing data to avoid duplication. 
    delete_data()

    # Creates thesis list
    create_thesis()
    
    theses = Thesis.objects.all() 

    # Structure the data into a dictionary nested inside a list
    thesis_data = []
    for thesis in theses:
        thesis_dict = {
        'topic_number': thesis.topic_number,
        'title': thesis.title,
        'category': thesis.category,
        'supervisor': thesis.supervisor,
        'description': thesis.description,
        'campuses': [campus.campus for campus in thesis.campus.all()],
        'courses': [course.course for course in thesis.course.all()]
        }
        thesis_data.append(thesis_dict)
    
    # Adds a maximum word count displayed for the description (50 words)
    for thesis in thesis_data:
        description = thesis['description']
        word_count = description.split()
        if len(word_count) > 50:
            description = ' '.join(word_count[:50])
            punctuation = ['.', ',', '/', ';', ':']
            
            if description[-1] in punctuation:
                description = description[:-1] + '...'
            else:
                description = description + '...'
                
        thesis['description'] = description

    context = {'theses': thesis_data}  
    
    return render(request, 'main/thesis_list.html', context)
    

