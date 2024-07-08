# Django Built-in modules
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from utils.datetime import check_and_make_aware

# Local apps
from .models import (
    User,
    MobilePhoneVerify,
    Profile,
)

# Python Standard Library
from datetime import datetime

# Third Party Packages
from phonenumber_field.formfields import PhoneNumberField


# Start Admin Panel Forms #

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('رمز عبور'),
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_('تکرار رمز عبور'),
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'mobile_number',
            'email',
            'avatar',
            'is_superuser',
            'is_staff',
            'is_active',
        )

    def clean_password2(self):
        cd = self.cleaned_data
        if not cd['password1'] or not cd['password2']:
            raise forms.ValidationError(_('این فیلد الزامی است.'))
        elif cd['password1'] != cd['password2']:
            raise forms.ValidationError(_('رمز عبور و تکرار آن مطابقت ندارد.'))
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_('رمز عبور'),
        help_text=_(
            "رمزهای عبور خام ذخیره نمی شوند، بنابراین راهی برای دیدن رمز عبور این کاربر وجود ندارد، اما می توانید رمز عبور را با استفاده از <a href=\"../password/\">این فرم</a> تغییر دهید."
        ),
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'mobile_number',
            'email',
            'avatar',
            'is_superuser',
            'is_staff',
            'is_active',
        )

    def clean_password(self):
        return self.initial['password']


# End Admin Panel Forms #


# Start Login and Register Forms #

class UserLoginForm(forms.Form):
    mobile_number = PhoneNumberField(
        label=_('شماره موبایل'),
        error_messages={'invalid': _('یک شماره موبایل معتبر وارد کنید')},
        widget=forms.TextInput(
            attrs={
                'placeholder': _('شماره مویابل خود را وارد کنید'),
            }
        ),
    )
    password = forms.CharField(
        label=_('رمز عبور'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('رمز عبور خود را وارد کنید'),
            }
        )
    )

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        return str(mobile_number).replace(' ', '')


class UserRegisterForm(forms.Form):
    mobile_number = PhoneNumberField(
        label=_('شماره موبایل'),
        error_messages={'invalid': _('یک شماره موبایل معتبر وارد کنید')},
        widget=forms.TextInput(
            attrs={
                'placeholder': _('شماره مویابل خود را وارد کنید'),
            }
        ),
    )

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        mobile_number = str(mobile_number).replace(' ', '')
        user = User.objects.filter(username=mobile_number)
        if user.exists():
            raise forms.ValidationError(_('این شماره قبلا در سایت ثبت شده است.'))
        return mobile_number


class UserRegisterCompleteForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('رمز عبور'),
        min_length=8,
        max_length=200,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('رمز عبور خود را وارد کنید'),
            }
        )
    )
    password2 = forms.CharField(
        label=_('تکرار رمز عبور'),
        min_length=8,
        max_length=200,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('رمز عبور خود را مجددا وارد کنید'),
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': _('نام خود را وارد کنید'),
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': _('نام خانوادگی خود را وارد کنید'),
                }
            ),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError(_('رمز عبور و تکرار آن باهم مطابقت ندارد.'))
        return self.cleaned_data['password2']


class UserForgetPasswordForm(forms.Form):
    mobile_number = PhoneNumberField(
        label=_('شماره موبایل'),
        error_messages={'invalid': _('یک شماره موبایل معتبر وارد کنید.')},
        widget=forms.TextInput(
            attrs={
                'placeholder': _('شماره مویابل خود را وارد کنید'),
            }
        ),
    )

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        mobile_number = str(mobile_number).replace(' ', '')
        user = User.objects.filter(username=mobile_number)
        if not user.exists():
            raise forms.ValidationError(_('حساب کاربری با این شماره یافت نشد.'))
        return mobile_number


class UserNewPasswordForm(forms.Form):
    password1 = forms.CharField(
        label=_('رمز عبور جدید'),
        min_length=8,
        max_length=200,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('رمز عبور جدید را وارد کنید'),
            }
        )
    )
    password2 = forms.CharField(
        label=_('تکرار رمز عبور'),
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('تکرار رمز عبور خود را وارد کنید'),
            }
        )
    )

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if len(password2) < 8:
            raise forms.ValidationError(_('کلمه عبور باید شامل حداقل ۸ کاراکتر باشد.'))

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('کلمه عبور با تکرار آن مطابقت ندارد.'))

        return password2


class UserCodeVerifyForm(forms.Form):
    code = forms.IntegerField(
        label=_('کد تایید'),
        widget=forms.NumberInput(
            attrs={
                "placeholder": _('کد تأیید ارسال شده به شماره مویابل خود را وارد کنید.'),
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self._mobile_number = kwargs.pop('mobile_number', None)
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            record = MobilePhoneVerify.objects.get(mobile_number=self._mobile_number)

            if record.code == code:
                record.status = MobilePhoneVerify.USELESS
                if (check_and_make_aware(datetime.now()) - record.updated).seconds > 5 * 60:
                    record.save()
                    raise forms.ValidationError(_('این کد تایید منقضی شده است. لطفا یک کد دیگر درخواست دهید.'))
                record.save()
                return code
            else:
                raise forms.ValidationError(_('کد تایید اشتباه است.'))

        except MobilePhoneVerify.DoesNotExist:
            raise forms.ValidationError(_('شماره تلفن یافت نشد. لطفا مراحل ثبت نام را مجددا طی کنید.'))
        except Exception as error:
            raise forms.ValidationError(error)


# End Login and Register Forms #

# Start Profile Forms #
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'mobile_number',
            'email',
            'avatar',
        )
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': _('نام خود را وارد کنید'),
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': _('نام خانوادگی خود را وارد کنید'),
                }
            ),
            'mobile_number': forms.TextInput(
                attrs={
                    'placeholder': _('شماره موبایل خود را وارد کنید'),
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': _('ایمیل خود را وارد کنید'),
                }
            ),
        }


class ChangePasswordForm(forms.Form):
    current = forms.CharField(
        label=_('رمز عبور فعلی'),
        max_length=200,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('رمز عبور فعلی'),
            }
        )
    )
    password1 = forms.CharField(
        label=_('رمز عبور جدید'),
        max_length=200,
        min_length=8,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('رمز عبور جدید'),
            }
        )
    )
    password2 = forms.CharField(
        label=_('تکرار رمز عبور جدید'),
        max_length=200,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('تکرار رمز عبور جدید'),
            }
        )
    )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2']:
            if cd['password1'] != cd['password2']:
                raise forms.ValidationError(_("رمز عبور و تکرار آن برابر نیست"))
        else:
            raise forms.ValidationError(_('پر کردن این بخش ضروری است'))
        return cd['password2']


# End Profile Forms #

# Admin #
class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def __init__(self, *args, parent_object, **kwargs):
        self.parent_object = parent_object
        super(ProfileAdminForm, self).__init__(*args, **kwargs)
        if parent_object:
            self.fields['slug'].initial = slugify(parent_object.username)


class ProfileAdminFormset(forms.BaseInlineFormSet):
    def get_form_kwargs(self, obj):
        kwargs = super().get_form_kwargs(obj)
        kwargs['parent_object'] = self.instance
        return kwargs
# Admin #
