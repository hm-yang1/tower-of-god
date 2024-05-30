from rest_framework import serializers
from ..models.category import Category

class CatergorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'