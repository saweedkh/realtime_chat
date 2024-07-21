from django.forms import ModelForm, ModelChoiceField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# local import
from .models import Link, Group, GroupMember


class LinkAdminForm(ModelForm):
    class Meta:
        model = Link
        fields = '__all__'

    group = ModelChoiceField(queryset=Group.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            user_id = kwargs['instance'].user_id
            self.fields['group'].queryset = Group.objects.filter(groupmember__user_id=user_id)






class GroupMemberForm(ModelForm):
    class Meta:
        model = GroupMember
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        admin_permissions = cleaned_data.get('admin_permissions')
        user_limited = cleaned_data.get('user_limited')
        
        print(admin_permissions)
        
        if self.has_changed():
            changed_fields = self.changed_data
            if admin_permissions and 'user_limited' in changed_fields:
                raise ValidationError(_('کاربر ادمین را نمی توانید محدود کنید.'))
            
            if admin_permissions and user_limited and 'admin_permissions' in changed_fields:
                cleaned_data['user_limited'] = []
                self.data = self.data.copy()
                self.data['user_limited'] = [] 
                
        return cleaned_data
