from rest_framework import serializers
from ..models.earbuds import Earbuds
from ..models.headphones import Headphones
from ..models.keyboard import Keyboard
from ..models.laptop import Laptop
from ..models.mouse import Mouse
from ..models.phone import Phone

class EarbudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Earbuds
        fields = '__all__'

class HeadphoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headphones
        fields = '__all__'

class KeyboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyboard
        fields = '__all__'
        
class LaptopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laptop
        fields = '__all__'

class MouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mouse
        fields = '__all__'

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = '__all__'