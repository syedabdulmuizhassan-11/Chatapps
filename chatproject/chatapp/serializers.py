from rest_framework import serializers
from .models import Room ,Message

class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model=Room
        fields="__all__"
        

class MessageSerializer(serializers.ModelSerializer):
    sender_username=serializers.CharField(source='sender.username' , read_only=True )
    class Meta:
        model=Message
        fields=["id" ,"room" , "sender" , "text" ,"timestamp" ,"sender_username"]
        
        
