from django.http import JsonResponse
from django.views import View


# local import
from .models import Group, GroupMember



class UserGroupsAPI(View):
    def get(self, request, user_id):
        groups_member = GroupMember.objects.filter(user_id=user_id)
        data = [{'uuid': group.group.uuid, 'name': group.group.name} for group in groups_member]
        return JsonResponse(data, safe=False)