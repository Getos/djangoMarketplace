from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.models import User


def group_required(*group_names):
    def in_groups(user):
        if user.is_authenticated:
            if user.groups.filter(name__in=group_names).exists():
                return True
        return False

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if in_groups(request.user) or User.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                # Redirect to a forbidden page or show an error message
                # Update this to your forbidden URL or view
                return redirect('forbidden')
        return _wrapped_view
    return decorator
