from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def role_required(allowed_roles):
    def decorator(view_function):

        @wraps(view_function)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("login")

            # Django superusers receive administrator access.
            if (
                request.user.is_superuser
                and "admin" in allowed_roles
            ):
                return view_function(
                    request,
                    *args,
                    **kwargs,
                )

            try:
                user_role = request.user.userprofile.role
            except AttributeError:
                messages.error(
                    request,
                    "Your account does not have an assigned role.",
                )
                return redirect("dashboard")

            if user_role not in allowed_roles:
                messages.error(
                    request,
                    "You do not have permission to perform this action.",
                )
                return redirect("dashboard")

            return view_function(
                request,
                *args,
                **kwargs,
            )

        return wrapper

    return decorator