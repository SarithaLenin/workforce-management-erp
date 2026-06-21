from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import UserProfile
from accounts.decorators import role_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)

            next_url = request.GET.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password.",
        )

    return render(
        request,
        "accounts/login.html",
    )
    
def logout_view(request):
    logout(request)
    return redirect('login')




@login_required
@role_required(['admin'])
def user_list(request):

    users = User.objects.select_related(
        'userprofile'
    ).order_by('username')

    return render(request, 'accounts/user_list.html', {
        'users': users
    })



@login_required
@role_required(['admin'])
def user_create(request):

    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            user.set_password(password)
            user.save()

            UserProfile.objects.create(
                user=user,
                role=role
            )

            messages.success(request, 'User created successfully.')
            return redirect('user_list')

    else:
        form = UserCreateForm()

    return render(request, 'accounts/user_form.html', {
        'form': form,
        'title': 'Add User'
    })



@login_required
@role_required(["admin"])
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user.is_superuser and not request.user.is_superuser:
        messages.error(
            request,
            "Only a superuser can edit another superuser.",
        )
        return redirect("user_list")

    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            "role": (
                "admin"
                if user.is_superuser
                else "hr"
            )
        },
    )

    if request.method == "POST":
        form = UserEditForm(
            request.POST,
            instance=user,
            user_profile=profile,
        )

        if form.is_valid():
            selected_role = form.cleaned_data["role"]
            selected_active = form.cleaned_data["is_active"]

            if user == request.user and not selected_active:
                form.add_error(
                    "is_active",
                    "You cannot deactivate your own account.",
                )

            if (
                user == request.user
                and selected_role != profile.role
            ):
                form.add_error(
                    "role",
                    "You cannot change your own role.",
                )

            if not form.errors:
                form.save()

                profile.role = selected_role
                profile.save(update_fields=["role"])

                messages.success(
                    request,
                    "User updated successfully.",
                )
                return redirect("user_list")

    else:
        form = UserEditForm(
            instance=user,
            user_profile=profile,
        )

    return render(
        request,
        "accounts/user_form.html",
        {
            "form": form,
            "title": "Edit User",
        },
    )

@login_required
@role_required(["admin"])
@require_POST
def user_toggle_active(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user == request.user:
        messages.error(
            request,
            "You cannot deactivate your own account.",
        )
        return redirect("user_list")

    if user.is_superuser:
        messages.error(
            request,
            "A superuser cannot be deactivated here.",
        )
        return redirect("user_list")

    target_role = getattr(
        getattr(user, "userprofile", None),
        "role",
        None,
    )

    # Never allow the final active administrator
    # account to be deactivated.
    if user.is_active and target_role == "admin":
        another_admin_exists = (
            UserProfile.objects.filter(
                role="admin",
                user__is_active=True,
            )
            .exclude(user=user)
            .exists()
        )

        if not another_admin_exists:
            messages.error(
                request,
                "The final active administrator cannot be deactivated.",
            )
            return redirect("user_list")

    user.is_active = not user.is_active
    user.save(update_fields=["is_active"])

    if user.is_active:
        messages.success(
            request,
            "User activated successfully.",
        )
    else:
        messages.success(
            request,
            "User deactivated successfully.",
        )

    return redirect("user_list")



@login_required
def profile(request):

    return render(request, 'accounts/profile.html')   




@login_required
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)

            messages.success(request, 'Password changed successfully.')
            return redirect('profile')

    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/change_password.html', {
        'form': form
    })



@login_required
def edit_profile(request):

    if request.method == 'POST':
        form = ProfileEditForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')

    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {
        'form': form
    })



@login_required
def settings_page(request):

    return render(request, 'accounts/settings.html')




@login_required
@role_required(['admin'])
def admin_reset_password(request, pk):

    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = AdminResetPasswordForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data['new_password']

            user.set_password(new_password)
            user.save()

            messages.success(request, 'Password reset successfully.')
            return redirect('user_list')

    else:
        form = AdminResetPasswordForm()

    return render(request, 'accounts/admin_reset_password.html', {
        'form': form,
        'user_obj': user
    })           





