# Django Built-in modules
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password, mobile_number=None):
        if not username:
            raise ValueError(_('کاربر باید نام کاربری داشته باشد.'))
        if not first_name:
            raise ValueError(_('کاربر باید نام داشته باشد.'))
        if not last_name:
            raise ValueError(_('کاربر باید نام خانوادگی داشته باشد.'))
        user = self.model(username=username, first_name=first_name, last_name=last_name, mobile_number=mobile_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, password):
        user = self.create_user(username, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
