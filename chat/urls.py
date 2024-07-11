from django.urls import  path

# local import 
from . import views

app_name = 'chat'

urlpatterns = [
    path('api/user-groups/<int:user_id>/', views.UserGroupsAPI.as_view(), name='user_groups_api'),

]
