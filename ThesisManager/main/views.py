from django.shortcuts import render
from .models import Thesis, create_thesis

def home(request):
    return render(request, 'main/home.html')

def about_us(request):
    pass

def thesis_details(request):
    pass

def thesis_list(request):
    ''' 
    create_thesis()
    
        ONLY NEED TO RUN THIS ONES UNLESS THERE ARE CHANGES IN DATABASE. 
        Running this will create the objects. 
        Rerunning it will make duplicates.
    
    '''
    theses = Thesis.objects.all() 

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
        print(thesis)

    context = {'theses': thesis_data}  
    
    return render(request, 'main/thesis_list.html', context)
    

