# Django Built-in modules
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.shortcuts import (
    redirect,
    render,
    get_object_or_404,
)
from django.contrib import messages
from django.contrib.auth import (
    logout as _logout,
    login,
    authenticate,
    update_session_auth_hash,
)
# Local Apps
from .decorators import anonymous_required
from .models import User, Bookmark, Profile
from .forms import (
    UserLoginForm,
    UserRegisterForm,
    UserRegisterCompleteForm,
    UserCodeVerifyForm,
    UserForgetPasswordForm,
    UserNewPasswordForm,
    EditProfileForm,
    ChangePasswordForm,
)
from .utils import send_verification_code
from utils.paginator import paginator
from blog.models import Post


@login_required
def logout(request):
    _logout(request)
    return redirect('pages:home')


# User Register and Login

@anonymous_required
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd.get('mobile_number'), password=cd.get('password'))
            if user:
                login(request, user)
                next_url = request.GET.get('next')
                return redirect(next_url) if next_url else redirect('pages:home')
            messages.error(request, 'شماره موبایل یا رمز عبور اشتباه است.')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'account/authentication/login.html', context)


@anonymous_required
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data.get('mobile_number')
            request.session['register_mobile_number'] = mobile_number
            result = send_verification_code(request, mobile_number)
            messages.info(
                request,
                result.get('message'),
                extra_tags='success' if result.get('status') == 200 else 'danger'
            )
            return redirect('account:user_register_verify')
        messages.error(
            request,
            message=form.errors.as_text(),
            extra_tags='danger'
        )
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'account/authentication/register/register.html', context)


@anonymous_required
def user_register_verify(request):
    mobile_number = request.session.get('register_mobile_number')
    if not mobile_number:
        redirect('account:user_register')
    if request.method == 'POST':
        form = UserCodeVerifyForm(request.POST, mobile_number=mobile_number)
        if form.is_valid():
            return redirect('account:user_register_complete')
        messages.error(
            request,
            message=form.errors.as_text(),
            extra_tags='danger'
        )
    else:
        form = UserCodeVerifyForm()
    context = {'form': form}
    return render(request, 'account/authentication/register/confirm.html', context)


@anonymous_required
def user_register_complete(request):

    if request.method == 'POST':
        form = UserRegisterCompleteForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            mobile_number = request.session.get('register_mobile_number')
            first_name = cd.get('first_name')
            last_name = cd.get('last_name')
            password = cd.get('password2')
            new_user = User.objects.create_user(
                username=mobile_number,
                password=password,
                first_name=first_name,
                last_name=last_name,
                mobile_number=mobile_number,
            )
            new_user.save()
            u = authenticate(request, username=mobile_number, password=password)
            login(request, u)
            return redirect('pages:home')
        messages.error(
            request,
            message=form.errors.as_text(),
            extra_tags='danger'
        )
    else:
        form = UserRegisterCompleteForm()
    context = {'form': form}
    return render(request, 'account/authentication/register/complete.html', context)


@anonymous_required
def user_forgot_password(request):
    if request.method == 'POST':
        form = UserForgetPasswordForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data.get('mobile_number')
            request.session['forget_password_mobile_number'] = mobile_number
            result = send_verification_code(request, mobile_number)
            messages.info(
                request,
                result.get('message'),
                extra_tags='success' if result.get('status') == 200 else 'danger'
            )
            return redirect('account:user_forgot_password_verify')
        messages.info(
                request,
                form.errors.as_text(),
                extra_tags='danger'
            )
    else:
        form = UserForgetPasswordForm()
    context = {'form': form}
    return render(request, 'account/authentication/forget_password/forgot_password.html', context)


@anonymous_required
def user_forgot_password_verify(request):
    mobile_number = request.session.get('forget_password_mobile_number')
    if not mobile_number:
        redirect('account:user_register')
    if request.method == 'POST':
        form = UserCodeVerifyForm(request.POST, mobile_number=mobile_number)
        if form.is_valid():
            return redirect('account:user_forgot_password_complete')
        messages.info(
                request,
                form.errors.as_text(),
                extra_tags='danger'
            )
    else:
        form = UserCodeVerifyForm()
    context = {'form': form}
    return render(request, 'account/authentication/forget_password/confirm.html', context)


@anonymous_required
def user_forgot_password_complete(request):
    if request.method == 'POST':
        form = UserNewPasswordForm(request.POST)
        if form.is_valid():
            mobile_number = request.session.get('forget_password_mobile_number')
            user = get_object_or_404(User, username=mobile_number)
            user.set_password(form.cleaned_data.get('password2'))
            user.save()
            messages.success(request, _('رمز عبور شما با موفقیت تغییر کرد.'), 'success')
            return redirect('account:login')
        messages.info(
                request,
                form.errors.as_text(),
                extra_tags='danger'
            )
    else:
        form = UserNewPasswordForm()
    context = {'form': form}
    return render(request, 'account/authentication/forget_password/complete.html', context)


@require_POST
@anonymous_required
def resend_verification_code(request):
    if request.method == 'POST':
        if request.session.get('register_mobile_number'):
            mobile_number = request.session['register_mobile_number']
        elif request.session.get('forget_password_mobile_number'):
            mobile_number = request.session['forget_password_mobile_number']
        else:
            return JsonResponse({'status': '404'})
        result = send_verification_code(request, mobile_number)
        messages.info(
            request,
            result.get('message'),
            extra_tags='success' if result.get('status') == 200 else 'danger'
        )
        return JsonResponse({'status': '200'})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard/dashboard.html')


# Address
@login_required
def addresses(request):
    addresses_qs = request.user.addresses.all()
    context = {'addresses': addresses_qs}
    return render(request, 'account/dashboard/address/addresses.html', context)


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _('اطلاعات کاربری شما با موفقیت ویرایش شد'), 'success')
            return redirect('account:profile')
    else:
        form = EditProfileForm(instance=user)
    context = {'form': form, }
    return render(request, 'account/dashboard/profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if request.user.check_password(cd['current']):
                user = request.user
                user.set_password(cd['password2'])
                user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, _('رمز عبور با موفقیت تغییر کرد'), 'success')
                return redirect('account:dashboard')
            messages.error(request, _('رمز عبور اشتباه است'), 'danger')

    else:
        form = ChangePasswordForm()

    context = {'form': form, }
    return render(request, 'account/dashboard/password_change.html', context)


@login_required
def bookmark(request):
    qs = Post.objects.filter(bookmark__user=request.user)
    posts = paginator(request=request, qs=qs, per_page=12)
    context = {'posts': posts, }
    return render(request, 'account/dashboard/bookmark.html', context)


@login_required
def bookmark_remove(request, post_id):
    try:
        Bookmark.objects.get(user=request.user, post__id=post_id).delete()
        messages.success(request, _('پست از لیست مطالعه شما حذف شد'))
    except Exception:
        messages.error(request, _('مشکلی در حذف این پست وجود دارد'))
    return redirect('account:bookmark')


def author_profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug, user__is_superuser=True, user__is_staff=True)
    qs = Post.objects.published().filter(author__profile=profile)
    post_count = qs.count()
    posts = paginator(request=request, qs=qs, per_page=9)
    context = {'profile': profile, 'posts': posts, 'post_count': post_count, }
    return render(request, 'account/author/profile.html', context)
