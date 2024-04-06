from django.shortcuts import render
from .data import create_thesis

def home(request):
    return render(request, 'main/home.html')

def about_us(request):
    pass

def thesis_details(request):
    
    theses= create_thesis()

    context = {'theses': theses }
    
    return render(request, 'main/thesis_details.html', context)
    pass

def thesis_list(request):

    theses = create_thesis()
    
    for thesis in theses:
        description = thesis.description
        word_count = description.split()
        if len(word_count) > 50:
            description = ' '.join(word_count[:50])
            
            punctuation = ['.', ',', '/', ';', ':']
            if description[-1] in punctuation:
                description = description[:-1] + '...'
            else:
                description = description + '...'
                
            thesis.description = description
                
    context = {'theses': theses}
    
    return render(request, 'main/thesis_list.html', context)
    

