import random
import copy
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Thesis, ThesisRequestAdd, ThesisRequestModify, ThesisRequestDelete, Course, Campus, Category, Supervisor
from .forms import ThesisForm, ThesisRequestFormAdd, ThesisRequestFormModify, ThesisRequestFormDelete
from .decorators import account_type_required
from users.models import CustomUser

def truncate_description(thesis):
    new_description = {}
            
    for item in thesis:     
        # truncates words longer than 250 characters 
        # i.e. only shows 250 character of the  thesis description
        description = item.description
        word_count = description.split()
        if len(description) > 230:
            description = ''.join(description[:230])
            
            punctuation = ['.', ',', '/', ';', ':', ' ']
            if description[-1] in punctuation:
                description = description[:-1] + '...'
            else:
                description = description + '...'
                
            new_description[item.topic_number] = description
        
        else:
            new_description[item.topic_number] = description
            
    return new_description

def paginator(request, thesis):
    # gets the thesis per page. default value = 5
    items_per_page = int(request.GET.get('items_per_page', 5))    

    # use built-in tool of django for paginating the theses
    page = Paginator(thesis, items_per_page)
    page_number = request.GET.get("page")
    page_obj = page.get_page(page_number)

    # values used to show the number of items shown and total number of theses
    total_pages = range(1, page.num_pages + 1)
    start_num = (page_obj.number - 1) * items_per_page + 1
    end_num = min(start_num + items_per_page - 1, page_obj.paginator.count)
    total_theses = len(thesis)
    
    return page_obj, total_pages, start_num, end_num, total_pages, items_per_page, total_theses

def home(request):
    theses = Thesis.objects.all()
    
    available_thesis = len(theses)
    available_supervisor = []
    
    for thesis in theses:
        available_supervisor.append(thesis.supervisor)
    
    context = {
        'available_thesis': available_thesis,
        'available_supervisor': len(set(available_supervisor))
    }
    
    return render(request, 'main/home.html', context)

def about_us(request):
    students = [
        {'name': 'Kye James Johnstone', 'number': 'S365934'},
        {'name': 'Juan Miguel Badayos', 'number': 'S365958'},
        {'name': 'Mark Joshua Tayco', 'number': 'S368036'},
        {'name': 'Agnes Juliana Javier', 'number': 'S364240'},
    ]
    
    context = {
        'students':students
    }
    
    return render(request, "main/about_us.html", context)

# prevents caching - ensure page is updated to users
def thesis_details(request, topic_number):
    theses = Thesis.objects.all()

    current_thesis = None
    
    for thesis in theses:
        if thesis.topic_number == topic_number:
            current_thesis = thesis
            break

    if current_thesis is None:
        error_message = f"Invalid thesis number. Topic number: {topic_number} does not exist."
        # 2 Thesis title are generated under see other thesis
        random_theses = random.sample(list(theses), min(3, len(list(theses))))
        context = {
            'error_message': error_message,
            'random_theses': random_theses
        }
    
        return render(request, 'main/thesis_details.html', context)
    
    remaining_theses = [thesis for thesis in theses if thesis.topic_number != topic_number]

    random_theses = random.sample(remaining_theses, min(2, len(remaining_theses)))
    
    context = {
        'thesis': current_thesis,
        'random_theses': random_theses,
    }

    return render(request, 'main/thesis_details.html', context)

@csrf_protect
def previous_page_view(request):
    if request.method == 'POST':
        return redirect('thesis_list')


def thesis_list(request):    
    theses = Thesis.objects.all()
    
    # created a separate list for different filter categories
    supervisor_list = []
    campus_list = []
    course_list = []
    category_list = []
    
    new_description = truncate_description(theses)
    
    for thesis in theses:
        # appends each category in the list
        campus_list_specific = []
        course_list_specific = []
        supervisor_list.append(thesis.supervisor)
        for campus in thesis.campus.all():
            campus_list_specific.append(campus)
        campus_list.append(campus_list_specific)
        for course in thesis.course.all():
            course_list_specific.append(course)
        course_list.append(course_list_specific)
        category_list.append(thesis.category)

    # extraccts the specific names e.g. <Campus: External> will extract External
    supervisor_names = [supervisor.supervisor for supervisor in supervisor_list]
    campus_names = [campus.campus for sublist in campus_list for campus in sublist]
    course_names = [course.course for sublist in course_list for course in sublist]
    category_names = [category.category for category in category_list]

    # add the number of thesis with a the filter tag
    supervisor_count = {}
    campus_count = {}    
    course_count = {}
    category_count = {}
    for supervisor in sorted(list(set(supervisor_names))):
        supervisor_count[supervisor] = supervisor_names.count(supervisor)
    for campus in sorted(list(set(campus_names))):
        campus_count[campus] = campus_names.count(campus)
    for course in sorted(list(set(course_names))):
        course_count[course] = course_names.count(course)
    for category in sorted(list(set(category_names))):
        category_count[category] = category_names.count(category)
    
    # retrieves the value of supervisor, campus, and coure when users interacts with filter
    # updates theses shown depending on the value set by the user
    selected_supervisor = request.GET.getlist('supervisor')
    selected_campus = request.GET.getlist('campus')
    selected_course = request.GET.getlist('course')
    selected_category = request.GET.getlist('category')
    filter_supervisor = ''
    filter_campus = ''
    filter_course= ''
    filter_category=''
    if selected_supervisor:
        theses = Thesis.objects.filter(supervisor__in = selected_supervisor)
        '''
            changes the url of the page to filter the list
            this fixes the issue where the the filter thesis is not stored
            in the paginator, causing the filter to reset when user
            goes to the next/previous page 
        '''
        filter_supervisor = "&".join([f'&supervisor={supervisor}' for supervisor in selected_supervisor])
    if selected_campus:
        theses = Thesis.objects.filter(campus__in = selected_campus)
        filter_campus = '&'.join([f'&campus={campus}' for campus in selected_campus])
    if selected_course:
        theses = Thesis.objects.filter(course__in = selected_course)
        filter_course = '&'.join([f'&course={course}' for course in selected_course])
    if selected_category:
        theses = Thesis.objects.filter(category__in = selected_category)
        filter_category = '&'.join([f'&category={category}' for category in selected_category])

    page_obj, total_pages, start_num, end_num, total_pages, items_per_page, total_theses = paginator(request, theses)
    
    context = {
        # for the paginator feature
        'page_obj': page_obj, # contains various data about the current page
        'total_pages': total_pages, 
        'start_num': start_num, # starting number of the thesis in the page
        'end_num': end_num,
        'total_theses': total_theses, 
        'items_per_page': items_per_page, 
        # for the filter feature
        'supervisor_list': supervisor_count,
        'campus_list': campus_count,
        'course_list': course_count,
        'category_list': category_count,
        'selected_supervisor': selected_supervisor,
        'selected_campus': selected_campus,
        'selected_course': selected_course,
        'selected_category': selected_category,
        # for the mix of filter and paginator feature
        'filter_supervisor': filter_supervisor,
        'filter_campus': filter_campus,
        'filter_course': filter_course,
        'filter_category': filter_category,
        # new shortened thesis description    
        'new_description': new_description,   
    }

    return render(request, 'main/thesis_list.html', context)
       
# Page not found function
def handling_404(request, exception):
    print("Handling 404 error")
    return render(request, '404.html', {})

@login_required
@account_type_required('admin', 'unit coordinator')
# functions for creating new data
def create_data(request):
    if request.method == 'POST':
        form = ThesisForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form.save()
            thesis = Thesis.objects.get(topic_number = form_data['topic_number'])
            context = {
                'type': 'created',
                'thesis': thesis,
                'page_title': 'Successfully Added ' + form_data['title']
            }
            return render(request, 'main/success.html', context)
    else:
        form = ThesisForm()
    
    context = {
        'form': form,
    }
    return render(request, 'main/create.html', context)

@login_required
@account_type_required('admin', 'unit coordinator')
#Delete data
def modify_or_delete(request, topic_number=None):
    if topic_number is None:
        if request.path == '/thesis/modify/':
            modify_or_delete = 'Modify'
        elif request.path == '/thesis/delete/':
            modify_or_delete = 'Delete'

        thesis = Thesis.objects.all()
        
        new_description = truncate_description(thesis)
            
        page_obj, total_pages, start_num, end_num, total_pages, items_per_page, total_theses = paginator(request, thesis)

        context = {
            'modify_or_delete': modify_or_delete,
            'thesis': thesis,
            'modify_or_delete_menu': True,
            'new_description': new_description,
            # for the paginator feature
            'page_obj': page_obj, # contains various data about the current page
            'total_pages': total_pages, 
            'start_num': start_num, # starting number of the thesis in the page
            'end_num': end_num,
            'total_theses': total_theses, 
            'items_per_page': items_per_page, 
        }
        
        return render(request, "main/modify_or_delete.html", context)
    else:
        if request.path[:15] == '/thesis/modify/':
            modify_or_delete = 'Modify'
        elif request.path[:15] == '/thesis/delete/':
            modify_or_delete = 'Delete'

        try:
            # Fetch the thesis object to delete based on topic_number
            thesis = Thesis.objects.get(topic_number=topic_number)
            old_thesis_data = copy.copy(thesis)
            old_thesis_campus = copy.copy(thesis.campus.all())
            old_thesis_course = copy.copy(thesis.course.all())
            old_campus_list= [campus for campus in old_thesis_campus]
            old_course_list= [course for course in old_thesis_course]
               
        except Thesis.DoesNotExist:
            return render(request, 'main/success.html', {'fail': True})
               
        if request.method == 'POST':
            if modify_or_delete == 'Modify':
                form = ThesisForm(request.POST, instance=thesis)
                if form.is_valid() and form.has_changed():
                    entries = ['topic_number', 'title', 'description', 'category_id', 'supervisor_id']
                    thesis_dict = {}
                    for key, value in vars(thesis).items():
                        if key in entries:
                            thesis_dict[key] = value 

                    old_thesis_dict = {}
                    for key, value in vars(old_thesis_data).items():
                        if key in entries:
                            old_thesis_dict[key] = value 

                    changed_data = {}
                    for key, value in thesis_dict.items():
                        if thesis_dict[key] != old_thesis_dict[key]: 
                            changed_data[key] = True
                    
                    form.save()                
                    new_campus_list= [campus for campus in thesis.campus.all()]
                    if new_campus_list != old_campus_list:
                        changed_data['campus'] = True
                        
                    new_course_list= [course for course in thesis.course.all()]
                    if new_course_list != old_course_list:
                        changed_data['course'] = True
                                                                                                        
                    context = {
                        'type': 'modified',
                        'page_title': 'Successfully Edited ' + form.cleaned_data['title'],
                        # updated thesis data
                        'thesis': thesis,
                        # old thesis data
                        'old_thesis_data': old_thesis_data,
                        'old_campus_list': old_campus_list,
                        'old_course_list': old_course_list,
                        # entries that changed data
                        'changed_data': changed_data,
                    }
                    return render(request, 'main/success.html', context)
                    
                elif not form.has_changed():
                    form = ThesisForm(instance = thesis)
                    
                    context = {
                        'thesis': thesis,
                        'form': form,
                        'modify_or_delete_menu': False,
                        'modify_or_delete': modify_or_delete,
                        'error': True
                    }
                        
                    return render(request, "main/modify_or_delete.html", context)
                
            elif modify_or_delete == 'Delete':
                try:
                    ThesisRequestDelete.objects.get(topic_number=topic_number).delete()
                    reqeust_delete = True
                except ThesisRequestDelete.DoesNotExist:
                    reqeust_delete = False
                try:
                    ThesisRequestModify.objects.get(topic_number=topic_number).delete()
                    reqeust_modify = True
                except ThesisRequestModify.DoesNotExist:
                    reqeust_modify = False

                thesis.delete()
                
                context = {
                    'thesis': thesis,
                    'old_thesis_data': old_thesis_data,
                    'old_campus_list': old_campus_list,
                    'old_course_list': old_course_list,
                    'type': 'deleted',
                }
                return render(request, 'main/success.html', context)

        else:
            if modify_or_delete == 'Modify':
                form = ThesisForm(instance = thesis)
            elif modify_or_delete =='Delete':
                form = ThesisForm(instance = thesis)
                for field in form.fields.values():
                    field.widget.attrs['readonly'] = True
                    field.widget.attrs['disabled'] = True

            
        context = {
            'thesis': thesis,
            'form': form,
            'modify_or_delete_menu': False,
            'modify_or_delete': modify_or_delete,
        }
            
        return render(request, "main/modify_or_delete.html", context)

@login_required
@account_type_required('admin', 'unit coordinator')
def review_request(request, request_type=None, topic_number=None):
    if topic_number is None:
        thesis_list = list(ThesisRequestAdd.objects.all()) + list(ThesisRequestModify.objects.all()) + list(ThesisRequestDelete.objects.all())
        thesis = sorted(thesis_list, key=lambda x: x.request_date, )

        if not thesis_list:
            context = {
                'no_requests': True
            }
            return render(request, 'main/review_request.html', context)

        new_description = truncate_description(thesis)
            
        page_obj, total_pages, start_num, end_num, total_pages, items_per_page, total_theses = paginator(request, thesis)

        context = {
            'review_menu': True,
            'thesis': thesis,
            'new_description': new_description,
            # for the paginator feature
            'page_obj': page_obj, # contains various data about the current page
            'total_pages': total_pages, 
            'start_num': start_num, # starting number of the thesis in the page
            'end_num': end_num,
            'total_theses': total_theses, 
            'items_per_page': items_per_page, 
        }
        return render(request, 'main/review_request.html', context)
    else:
        try:
            modify = False
            if request_type == 'create':
                thesis_to_review = ThesisRequestAdd.objects.get(topic_number=topic_number)
            elif request_type == 'modify':
                thesis_to_review = ThesisRequestModify.objects.get(topic_number=topic_number)
                modify = True
            elif request_type == 'delete':
                thesis_to_review = ThesisRequestDelete.objects.get(topic_number=topic_number)
                
            selected_action = request.POST.get('action')
            
            thesis_to_review_data = {
                'topic_number': thesis_to_review.topic_number,
                'title': thesis_to_review.title,
                'description': thesis_to_review.description,
                'category': thesis_to_review.category,
                'supervisor': thesis_to_review.supervisor,
                'group_taker_limit': thesis_to_review.group_taker_limit,
            }
            
            thesis_to_review_data_copy = copy.copy(thesis_to_review_data)
            thesis_to_review_data_campus = copy.copy(thesis_to_review.campus.all())
            thesis_to_review_data_course = copy.copy(thesis_to_review.course.all())
            
            old_thesis_data = None
            changed_data = None
            delete = None
            old_campus_list = None
            old_course_list = None
            
            try:
                old_thesis = Thesis.objects.get(topic_number=topic_number)
                old_thesis_data = copy.copy(old_thesis)
                old_thesis_campus = copy.copy(old_thesis.campus.all())
                old_thesis_course = copy.copy(old_thesis.course.all())
                old_campus_list= [campus for campus in old_thesis_campus]
                old_course_list= [course for course in old_thesis_course]
                old_thesis_exists = True
                               
                entries = ['topic_number', 'title', 'description', 'category_id', 'supervisor_id']
                thesis_dict = {}
                for key, value in vars(thesis_to_review).items():
                    if key in entries:
                        thesis_dict[key] = value 

                old_thesis_dict = {}
                for key, value in vars(old_thesis_data).items():
                    if key in entries:
                        old_thesis_dict[key] = value 

                changed_data = {}
                for key, value in thesis_dict.items():
                    if thesis_dict[key] != old_thesis_dict[key]: 
                        changed_data[key] = True

                new_campus_list= [campus for campus in thesis_to_review.campus.all()]
                if new_campus_list != old_campus_list:
                    changed_data['campus'] = True
                    
                new_course_list= [course for course in thesis_to_review.course.all()]
                if new_course_list != old_course_list:
                    changed_data['course'] = True
                
            except Thesis.DoesNotExist:
                old_thesis_exists = False
                
            if selected_action == 'accept':
                if request_type == 'create':
                    thesis_to_create = Thesis.objects.create(**thesis_to_review_data)    
                    thesis_to_create.campus.add(*Campus.objects.filter(campus__in = thesis_to_review_data_campus)),
                    thesis_to_create.course.add(*Course.objects.filter(course__in = thesis_to_review_data_course)),

                    thesis_to_review.delete()                    
                    type = 'accepted'
                    thesis_to_display = thesis_to_create
                    
                elif request_type == 'modify':
                    old_thesis.delete()
                    thesis_to_modify = Thesis.objects.create(**thesis_to_review_data)
                    thesis_to_modify.campus.add(*Campus.objects.filter(campus__in = thesis_to_review_data_campus)),
                    thesis_to_modify.course.add(*Course.objects.filter(course__in = thesis_to_review_data_course)),
                                     
                    thesis_to_review.delete()                    

                    thesis_to_display = old_thesis_data
                    type = 'modified'
                    modify = True
                    
                elif request_type == 'delete':
                    old_thesis.delete()
                    thesis_to_review.delete()
                              
                    thesis_to_display = old_thesis_data
                    type = 'deleted'
                    delete = True
                                            
                context = {
                    'thesis': thesis_to_display,
                    'requested_by': thesis_to_review.requested_by,
                    'request_date': thesis_to_review.request_date,
                    'request_type': thesis_to_review.request_type,
                    'type': type,
                    'delete': delete,
                    'modify': modify,
                    'old_thesis_data': old_thesis_data,
                    'old_campus_list': old_campus_list,
                    'old_course_list': old_course_list,
                    'changed_data': changed_data,                            
                }
                return render(request, 'main/success.html', context)
            
            elif selected_action == 'reject':
                thesis_to_review.delete()
                
                context = {
                    'rejected_thesis_request': True,
                    'type': 'rejected',
                    'old_thesis_data': thesis_to_review_data_copy,
                    'old_course_list': thesis_to_review_data_course,                    
                    'old_campus_list': thesis_to_review_data_campus,
                }
                
                return render(request, 'main/success.html', context)
            
        except Exception as e:
            context = {
                'error': True,
                'back_to_settings': True,
                'error_message': e
            }
            return render(request, 'main/404.html', context)
                
        context = {
            'request': True,
            'review_menu': False,
            'thesis': thesis_to_review,
            'modify_review': modify,
            'old_thesis_exists':old_thesis_exists,
            'old_thesis_data': old_thesis_data,
            'changed_data': changed_data,
        }
        return render(request, 'main/review_request.html', context)
        
@login_required
@account_type_required('admin', 'supervisor')
def request_crud(request, crud_action, status=None, topic_number=None):
    if crud_action == 'create':
        if request.method =='POST':
            form = ThesisRequestFormAdd(request.POST)
            if form.is_valid():
                thesis_request = form.save(commit=False)     
                thesis_request.requested_by = CustomUser.objects.get(username=request.user.username)
                thesis_request.request_type = crud_action
                thesis_request.save()

                form.save_m2m()
                requested_thesis = ThesisRequestAdd.objects.get(topic_number =form.cleaned_data['topic_number'])
               
                context = {
                    'request': True,
                    'request_type': 'create',
                    'type': 'create',
                    'thesis': requested_thesis,
                    'requested_by': requested_thesis.requested_by,
                    'request_date': requested_thesis.request_date,
                }

                return render(request, 'main/success.html', context)
            
        else:
            form = ThesisRequestFormAdd()
                
        context = {
            'request': True,
            'request_type': 'create',
            'form': form
        } 
        return render(request, 'main/request_crud.html', context)
    
    elif crud_action == 'modify' or crud_action == 'delete':
        if topic_number is None:
            if status is None:
                thesis = Thesis.objects.all()

                new_description = truncate_description(thesis)
                                
                page_obj, total_pages, start_num, end_num, total_pages, items_per_page, total_theses = paginator(request, thesis)
                
                context = {
                    'request_type': crud_action,
                    'menu': True,
                    'thesis': thesis,
                    'new_description': new_description,
                    # for the paginator feature
                    'page_obj': page_obj, # contains various data about the current page
                    'total_pages': total_pages, 
                    'start_num': start_num, # starting number of the thesis in the page
                    'end_num': end_num,
                    'total_theses': total_theses, 
                    'items_per_page': items_per_page, 
                }
            
                return render(request, 'main/request_crud.html', context)
            
            else:
                pass
                '''
                if request.path[:31] == '/thesis/request/modify/pending/':
                    modify_or_delete = 'modify'
                elif request.path[:31] == '/thesis/request/delete/pending/':
                    modify_or_delete = 'delete'
                
                thesis_list = list(ThesisRequestAdd.objects.all()) + list(ThesisRequestModify.objects.all())
                thesis = sorted(thesis_list, key=lambda x: x.topic_number)


                context = {
                    
                }
                
                return render(request, 'main/request_crud.html', context)
                '''
        
        else:
            if request.path[:23] == '/thesis/request/modify/':
                modify_or_delete = 'modify'
            elif request.path[:23] == '/thesis/request/delete/':
                modify_or_delete = 'delete'
            
            exists_in_database = False
            thesis_exists = Thesis.objects.filter(topic_number = topic_number).exists()
            if thesis_exists:
                exists_in_database = True            
            
            thesis = Thesis.objects.get(topic_number=topic_number)
            old_thesis_data = copy.copy(thesis)
            old_thesis_campus = copy.copy(old_thesis_data.campus.all())
            old_thesis_course = copy.copy(old_thesis_data.course.all())
            old_campus_list= [campus for campus in old_thesis_campus]
            old_course_list= [course for course in old_thesis_course]
            
            try:
                request_modify_exists = ThesisRequestModify.objects.get(topic_number=topic_number)
                request_exists_modify = True
            except ThesisRequestModify.DoesNotExist:
                request_exists_modify = False

            try:
                request_delete_exists = ThesisRequestDelete.objects.get(topic_number=topic_number)
                request_exists_delete = True
            except ThesisRequestDelete.DoesNotExist:
                request_exists_delete = False
                
            initial_form_data = {
                'topic_number': thesis.topic_number,
                'title': thesis.title,
                'description': thesis.description,
                'category': thesis.category,
                'supervisor': thesis.supervisor,
                'course': thesis.course.all(),
                'campus': thesis.campus.all(),
                'group_taker_limit': thesis.group_taker_limit,
            }

            if request.method == 'POST':
                if modify_or_delete == 'modify':  
                    try:                        
                        request_modify_exists.delete()
                        request_exists_modify = True
                    except UnboundLocalError:
                        request_exists_modify = False
                        
                    form = ThesisRequestFormModify(request.POST, initial=initial_form_data)
                    if form.is_valid() and form.has_changed():
                        thesis_request = form.save(commit=False)     
                        thesis_request.requested_by = CustomUser.objects.get(username=request.user.username)
                        if exists_in_database:
                            thesis_request.request_type = crud_action
                        else:
                            thesis_request.request_type = 'add'
                                     
                        thesis_request.save()            
                        form.save_m2m()                       
                                           
                        requested_thesis = ThesisRequestModify.objects.get(topic_number =form.cleaned_data['topic_number'])
                
                        entries = ['topic_number', 'title', 'description', 'category_id', 'supervisor_id']
                        thesis_dict = {}
                        for key, value in vars(requested_thesis).items():
                            if key in entries:
                                thesis_dict[key] = value 

                        old_thesis_dict = {}
                        for key, value in vars(old_thesis_data).items():
                            if key in entries:
                                old_thesis_dict[key] = value 

                        changed_data = {}
                        for key, value in thesis_dict.items():
                            if thesis_dict[key] != old_thesis_dict[key]: 
                                changed_data[key] = True

                        new_campus_list= [campus for campus in requested_thesis.campus.all()]
                        if new_campus_list != old_campus_list:
                            changed_data['campus'] = True
                            
                        new_course_list= [course for course in requested_thesis.course.all()]
                        if new_course_list != old_course_list:
                            changed_data['course'] = True
                            
                        context = {
                            'request': True,
                            'request_type': 'modify',
                            'type': 'modify',
                            'thesis': requested_thesis,
                            'requested_by': requested_thesis.requested_by,
                            'request_date': requested_thesis.request_date,
                            'old_thesis_data': old_thesis_data,
                            'old_campus_list': old_campus_list,
                            'old_course_list': old_course_list,
                            'changed_data': changed_data,
                        }

                        return render(request, 'main/success.html', context)    
                    elif form.has_changed() is not True:                   
                        form = ThesisRequestFormModify(initial=initial_form_data)
                        
                        context = {
                            'request_exists_modify': request_exists_modify,
                            'request_exists_delete': request_exists_delete,
                            'form': form,
                            'request_type': 'modify',
                            'selected_thesis': thesis,
                            'no_change': True,
                        }
                            
                        return render(request, 'main/request_crud.html',context)
                elif modify_or_delete == 'delete':
                    form = ThesisRequestFormDelete(initial_form_data)
                    for field in form.fields.values():
                        field.widget.attrs['readonly'] = True
                        field.widget.attrs['disabled'] = True
                    if form.is_valid():
                        thesis_request = form.save(commit=False)     
                        thesis_request.requested_by = CustomUser.objects.get(username=request.user.username)
                        thesis_request.request_type = crud_action
                        thesis_request.save()
                
                        form.save_m2m()
                        
                        requested_thesis = ThesisRequestDelete.objects.get(topic_number =form.cleaned_data['topic_number'])

                        context = {
                            'request': True,
                            'request_type': 'delete',
                            'type': 'delete',
                            'thesis': requested_thesis,
                            'requested_by': requested_thesis.requested_by,
                            'request_date': requested_thesis.request_date,
                        }
                        
                        return render(request, 'main/success.html', context)

            else:
                if modify_or_delete == 'modify':
                    form = ThesisRequestFormModify(initial=initial_form_data)
                elif modify_or_delete == 'delete':
                    form = ThesisRequestFormDelete(instance=thesis)
                    for field in form.fields.values():
                        field.widget.attrs['readonly'] = True
                        field.widget.attrs['disabled'] = True

            context = {
                'request_exists_modify': request_exists_modify,
                'request_exists_delete': request_exists_delete,
                'form': form,
                'request_type': modify_or_delete,
                'menu': False,
                'selected_thesis': thesis,
            }
            return render(request, 'main/request_crud.html', context)

@login_required
@account_type_required('admin', 'unit coordinator', 'supervisor')
def admin_settings(request, account_type):
       
    return render(request, 'main/CRUD_thesis.html')



'''       
FUNCTION FOR INSERTING SAMPLE DATA TO MODELS.PY 
-----------------------------------------------

def add_previous_data(request):
    campuses = ['Casuarina', 'Sydney', 'External']
    area = {
        'chemical': 'Chemical Engineering',
        'civil' : 'Civil and Structural Engineering',
        'electrical' :'Electrical and Electronics Engineering',
        'mechanical' : 'Mechanical Engineering',
        'computer' : 'Computer Science',
        'cyber' : 'Cyber Security',
        'data' : 'Data Science',
        'information' : 'Information Systems and Data Science',
        'software' : 'Software Engineering',
        } 
    categories = {
        'artificial' : 'Artificial Intelligence, Machine Learning and Data Science',
        'biomedical' : 'Biomedical Engineering and Health Informatics',
        'cyber' : 'Cyber Security',
    }
    supervisors = ['Bharanidharan Shanmugam', 'Yakub Sebastian', 'Sami Azam', 'Asif Karim']

    for campus in campuses:
        new_campus = Campus(campus = campus)
        new_campus.save()

    for course in area:
        new_course = Course(course = area[course])
        new_course.save()

    for category in categories:
        new_category = Category(category = categories[category])
        new_category.save()
    
    for supervisor in supervisors:
        new_supervisor = Supervisor(supervisor = supervisor)
        new_supervisor.save()
    
    thesis_1 = Thesis.objects.create(
        topic_number=1,       
        title= 'Machine learning approaches for Cyber Security',
        category= Category.objects.get(category = categories['artificial']),
        supervisor= Supervisor.objects.get(supervisor = supervisors[0]),
        description='As we use internet more, the data produced by us is enormous. But are these data being secure? The goal of applying machine learning or intelligence is to better risk modelling and prediction and for an informed decision support. Students will be working with either supervised or unsupervised machine learning approaches to solve the problem/s in the broader areas of Cyber Security.'
    )

    thesis_1.campus.add(*Campus.objects.filter(campus__in=campuses))
    thesis_1.course.add(*Course.objects.filter(course__in =[area['computer'], area['software']]))

    thesis_2 = Thesis.objects.create(
        topic_number= 9,
        title= 'Informetrics applications in multidisciplinary domain',
        category= Category.objects.get(category = categories['artificial']),
        supervisor= Supervisor.objects.get(supervisor = supervisors[1]),
        description='Informetrics studies are concerned with the quantitative aspects of information. The applications of advanced machine learning, information retrieval, network science and bibliometric techniques on various information artefact have contributed fresh insights into the evolutionary nature of research fields. This project aims at discovering informetric properties of multidisciplinary research literature using various machine learning, network analysis, data visualisation and data wrangling tools.'
    )
    thesis_2.campus.add(*Campus.objects.filter(campus__in=campuses))
    thesis_2.course.add(*Course.objects.filter(course__in = [area['computer'], area['cyber'], area['data'], area['information'], area['software']]))
     
    thesis_3 = Thesis.objects.create(
        topic_number=16,
        title='Development of a Virtual Reality System to Test Binaural Hearing',
        category=Category.objects.get(category = categories['biomedical']),
        supervisor= Supervisor.objects.get(supervisor = supervisors[2]),
        description='A virtual reality system could be used to objectively test the binaural hearing ability of humans (the ability to hear stereo and locate the direction and distance of sound). This project aims to design, implement and evaluate a VR system using standard off the shelf components (VR goggle and headphones) and standard programming techniques.'
    )
    thesis_3.campus.add(*Campus.objects.filter(campus__in=[campuses[0], campuses[2]]))
    thesis_3.course.add(*Course.objects.filter(course__in =[area['electrical'], area['computer'],  area['software']]))
    
    thesis_4 = Thesis.objects.create(
        topic_number=41,
        title='Current trends on cryptomining and its potential impact on cryptocurrencies',
        category= Category.objects.get(category = categories['cyber']),
        supervisor= Supervisor.objects.get(supervisor = supervisors[2]),
        description= "Cryptomining is the process of mining crypto currencies by running a sequence of algorithms. Traditionally, to mine new crypto coins, a person (or group of people) would buy expensive computers and spend a lot of time and money running them to perform the difficult calculations to generate crypto coins. Some website owners have started taking a different approach; they have put the software which runs those difficult calculations into their website's Javascript. This then causes the computers belonging to the visitors of their website to run those calculations for them, instead of running them themselves. In other words, when you visit a website with an embedded crypto-miner in it, your computer and electricity is used to try to generate crypto-coins for the owners of that website. Although there are various measures being applied to stop these illegitimate minings, the trend is still increasing. This research aims to find out potential gaps in current methodologies and develop a solution that can fulfil the gap. It also aims to find out: (1) What type crypto mining methodologies are being applied?, (2) Apart from crypto-mining, what other security risks may it introduce? For example: cryptojacking,  and (3) How current web standards are tackling this problem?"
    )
    thesis_4.campus.add(*Campus.objects.filter(campus__in=campuses))
    thesis_4.course.add(*Course.objects.filter(course__in =[area['computer'], area['cyber'], area['software']]))
    
    thesis_5 = Thesis.objects.create(
        topic_number=176,
        title='Artificial Intelligence in Health Informatics',
        category= Category.objects.get(category = categories['artificial']),
        supervisor= Supervisor.objects.get(supervisor = supervisors[3]),
        description='The project aims to use multiple publicly available health datasets to formulate a different dataset that may have features from the original set along with new ones developed through feature engineering. The dataset will then be used to build predictive model based on both general and deep learning based algorithm. The findings will be analysed and compared to similar research works.'
    )
    thesis_5.campus.add(*Campus.objects.filter(campus__in=campuses))
    thesis_5.course.add(*Course.objects.filter(course__in =[area['electrical'], area['computer'], area['data'], area['software']]))
    
    thesis_ = Thesis.objects.create(
        topic_number= 180,
        title='Unsupervised Model Development from Autism Screening Data',
        category= Category.objects.get(category = categories['artificial']),
        supervisor= Supervisor.objects.get(supervisor = supervisors[3]),
        description='The proposed system will present a two-cluster solution from a given dataset which will group toddlers based on multiple common medical traits. In depth literature survey of similar studies, both supervised and unsupervised will be carried out before the cluster-based model is implemented. The solution will be validated using both External and Internal validation measures and statistical significance tests.'
    )
    thesis_.campus.add(*Campus.objects.filter(campus__in=campuses))
    thesis_.course.add(*Course.objects.filter(course__in =[area['electrical'], area['computer'], area['data'], area['software']]))

    thesis_ = Thesis.objects.create(
        topic_number= 226,
        title= 'Applying Artificial Intelligence to solve real world problems',
        category= Category.objects.get(category = categories['artificial']),
        supervisor= Supervisor.objects.get(supervisor = supervisors[0]),
        description='Artificial Intelligence has been used in many applications to solve certain problems through out the academia and the industry – from electricity to writing text. AI has a multitude of applications and this project will pick up a problem and explore the applications of AI with minimal human intervention. Examples of applications include -building a bot, predicting the power usage, spam filtering and the list is endless.'
    )
    thesis_.campus.add(*Campus.objects.filter(campus__in=campuses))
    thesis_.course.add(*Course.objects.filter(course__in =[area['chemical'], area['civil'], area['computer'], area['cyber'], area['data'], area['electrical'], area['information'], area['mechanical'], area['software']]))
    return render(request, 'main/home.html')
'''
'''
FOR TROUBLESHOOTING PURPOSES
----------------------------
def data_retrieval_test(request):
    
    thesis_list = Thesis.objects.all()
    
    context = {
        'thesis_list': thesis_list,      
    }
    
    return render(request, 'main/data_retrieval_test.html', context)
'''