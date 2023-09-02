from rest_framework import serializers
from app.models import *

class TODOSerializer(serializers.ModelSerializer):

    def validate(self, data):         
        if self.instance==None and TODO.objects.filter(title = data['title'],user = data['user'], is_active__in=[True], is_deleted__in=[False]).exists():
            raise serializers.ValidationError("Record already exists")
        elif self.instance!=None:
            if self.instance.id and TODO.objects.filter(title = data['title'],user = data['user'], is_active__in=[True], is_deleted__in=[False]).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Record already exists")
        return data

    class Meta:
        model = TODO
        fields = '__all__'


    
