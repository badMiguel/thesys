from django.shortcuts import render
from .data import create_thesis
from django.http import Http404
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_control
import random


def home(request):
    return render(request, 'main/home.html')

def about_us(request):
    return render(request, 'main/about_us.html')

# prevents caching - ensure page is updated to users
@cache_control(no_cache=True, must_revalidate=True, max_age=0)
def thesis_details(request, topic_number):
    all_theses = create_thesis()

    current_thesis = None
    
    for thesis in all_theses:
        if thesis.topic_number == topic_number:
            current_thesis = thesis
            break

    if current_thesis is None:
        error_message = "Invalid thesis number. Topic number: {} does not exist." .format(topic_number)
        return render(request, 'main/thesis_details.html',  {'error_message': error_message})
    
    remaining_theses = [thesis for thesis in all_theses if thesis.topic_number != topic_number]
    
    if len(remaining_theses) <= 3:
        random_theses = remaining_theses
    else:
        random_theses = random.sample(remaining_theses, 3)
    
    context = {'thesis': current_thesis,
               'random_theses' : random_theses,
        }
    
    return render(request, 'main/thesis_details.html', context)

@csrf_protect
def previous_page_view(request):
    if request.method == 'POST':
        previous_page = request.POST.get('previous_page', None)
        if previous_page:
            return redirect(previous_page)
    return redirect('home')


# prevents caching - ensure page is updated to users
@cache_control(no_cache=True, must_revalidate=True, max_age=0)
def thesis_list(request):
    theses = create_thesis()
    
    # created a separate list for different filter categories
    supervisor_list = []
    campus_list = []
    course_list = []
    category_list = []
    
    for thesis in theses:
        # appends each category in the list
        supervisor_list.append(thesis.supervisor)
        for campus in thesis.campus:
            campus_list.append(campus)
        for course in thesis.course:
            course_list.append(course)
        for category in thesis.category:
            category_list.append(thesis.category)
        
        # truncates words longer than 250 characters 
        # i.e. only shows 250 character of the  thesis description
        description = thesis.description
        word_count = description.split()
        if len(description) > 230:
            description = ''.join(description[:230])
            
            punctuation = ['.', ',', '/', ';', ':', ' ']
            if description[-1] in punctuation:
                description = description[:-1] + '...'
            else:
                description = description + '...'
                
            thesis.description = description

    # retrieves the value of supervisor, campus, and coure when users interacts with filter
    # updates theses shown depending on the value set by the user
    selected_supervisor = request.GET.getlist('supervisor')
    if selected_supervisor:
        theses = [thesis for thesis in theses if thesis.supervisor in selected_supervisor]

    selected_campus = request.GET.getlist('campus')
    if selected_campus:
        theses = [thesis for thesis in theses if thesis if any(campus in thesis.campus for campus in selected_campus)]

    selected_course = request.GET.getlist('course')
    if selected_course:
        theses = [thesis for thesis in theses if thesis if any(course in thesis.course for course in selected_course)]

    selected_category = request.GET.getlist('category')
    if selected_category:
        theses = [thesis for thesis in theses if thesis if any(category in thesis.category for category in selected_category)]

    # gets the thesis per page. default value = 5
    items_per_page = int(request.GET.get('items_per_page', 5))    

    # use built-in tool of django for paginating the theses
    page = Paginator(theses, items_per_page)
    page_number = request.GET.get("page")
    page_obj = page.get_page(page_number)

    # values used to show the number of items shown and total number of theses
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
        'items_per_page': items_per_page,
        'supervisor_list': set(supervisor_list), #set() removes items in list that are repeated
        'campus_list': set(campus_list),
        'course_list': set(course_list),
        'category_list': set(category_list),
        'selected_supervisor': selected_supervisor,
        'selected_campus': selected_campus,
        'selected_course': selected_course,
        'selected_category': selected_category
        }

    return render(request, 'main/thesis_list.html', context)
    

