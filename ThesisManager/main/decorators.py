from django.shortcuts import render
from django.shortcuts import redirect
from functools import wraps

# checks account type of user. redirects if they dont have account previlleges
def account_type_required(*account_type):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.account_type in account_type:
                    return view_func(request, *args, **kwargs)
                else:
                    context = {
                        'error': 'access',
                        'error_message': 'You do not have access to this page'
                    }
                    return render(request, 'main/account_error.html', context)

            else: 
                return redirect('login')
        return _wrapped_view
    return decorator