# Local Apps
from .models import AbstractStaticPage

# Third Party Packages
from rest_framework import serializers


class BaseStaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractStaticPage
        fields = ('content',)
