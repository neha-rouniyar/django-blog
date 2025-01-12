from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields = '__all__' 

    def validate_title(self,value):
        if len(value)<5:
            raise serializers.ValidationError("Title must be atleast 5 characters long")
        return value
    
    def validate_description(self,value):
        if len(value)>500:
            raise serializers.ValidationError("Description must not exceed 500 characters")
        return value