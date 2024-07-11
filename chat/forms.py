from django.forms import ModelForm, ModelChoiceField

# local import
from .models import Link, Group


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
