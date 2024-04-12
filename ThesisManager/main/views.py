from django.shortcuts import render
from .data import create_thesis
from django.http import Http404
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

    # truncates words longer than 75  words
    for thesis in theses:
        description = thesis.description
        word_count = description.split()
        if len(word_count) > 75:
            description = ' '.join(word_count[:75])
            
            punctuation = ['.', ',', '/', ';', ':']
            if description[-1] in punctuation:
                description = description[:-1] + '...'
            else:
                description = description + '...'
                
            thesis.description = description

    items_per_page = 5
    page = Paginator(theses, items_per_page)
    page_number = request.GET.get("page")
    page_obj = page.get_page(page_number)

    total_pages = range(1, page.num_pages + 1)
    
    start_num = (page_obj.number - 1) * items_per_page + 1
    end_num = min(start_num + items_per_page - 1, page_obj.paginator.count)

    total_theses = len(theses)
    
    context = {
        'page_obj': page_obj,
        'total_pages': total_pages,
        'start_num': start_num,
        'end_num': end_num,
        'total_theses': total_theses,
        }
    
    return render(request, 'main/thesis_list.html', context)
    

