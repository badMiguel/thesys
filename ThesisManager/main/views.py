from django.shortcuts import render
from .data import create_thesis
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect


def home(request):
    return render(request, 'main/home.html')

def about_us(request):
    return render(request, 'main/about_us.html')

def thesis_details(request, topic_number):
    theses = create_thesis()

    thesis = None
    
    for t in theses:
        if t.topic_number == topic_number:
            thesis = t
            break

    if thesis is None:
        error_message = "Invalid thesis number. Topic number: {} does not exist." .format(topic_number)
        return render(request, 'main/thesis_details.html',  {'error_message': error_message})
    
    context = {'thesis': thesis}
    
    return render(request, 'main/thesis_details.html', context)
    pass

@csrf_protect
def previous_page_view(request):
    if request.method == 'POST':
        previous_page = request.POST.get('previous_page', None)
        if previous_page:
            return redirect(previous_page)
    return redirect('home')
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
    

