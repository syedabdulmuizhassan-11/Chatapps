from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from rest_framework.permissions import IsAuthenticated
from .models import Room  ,Message
from .serializers import RoomSerializers , MessageSerializer



class SignupApi(APIView):
    def post(self , request):
        username=request.data.get('username')
        email=request.data.get('email')
        password=request.data.get('password')
        
        if not username or not password:
            return Response({"ERROR" : "YOU NOT ADD USERNAME AND PASSWORD"} , status=400)
        
        
        if User.objects.filter(username=username).exists(): 
            return Response({"Message" : "ALREADY USERNAME  EXISTS"} , status=400)
        
        if User.objects.filter(email=email).exists():
            return Response({"Message" : "ALREADY EMAIl  EXISTS"} , status=400)
        
        user=User.objects.create_user(username=username , password=password, email=email)
        return Response({"Message" : "SUCCESSFULLY USER CREATED"} , status=201)
        
            

class LoginApi(APIView):
    def post(self, request):
        username_or_email=request.data.get('username')
        password=request.data.get('password')
        
        if not username_or_email or not password:
            return Response({"ERROR" : "YOU NOT ADD USERNAME AND PASSWORD"} , status=400)  
        
        if '@' in username_or_email:
            user_obj=User.objects.get(email=username_or_email)
            username=user_obj.username
        else:
            username=username_or_email
            
        user=authenticate(username=username , password=password)
        if user is not None :
            login(request ,user)
            return Response({"Message" : "SUCCESSFULLY USER LOGIN"} , status=200)
        return Response({"Error" : "INVALID CREDENTIAL"} , status=400)
    

class LogoutApi(APIView):
    permission_classes = [IsAuthenticated]
    def post (self ,request):
        logout(request)
        return Response ("Successfully logout" , status=200)
    

class CheckLogin(APIView):
    def get(self ,request):
        if request.user.is_authenticated:
            return Response({"Logged_in":True})
        return Response({"Logged_in":False})
    

class GetAllUsers(APIView):
    permission_classes = [IsAuthenticated]
    def get(self , request ):
        user=User.objects.exclude(id=request.user.id).exclude(is_superuser=True)
        data=[{"id":u.id , "username":u.username} for u in user]
        return Response(data)
    
class CreatePrivateRoom(APIView):
    permission_classes=[IsAuthenticated]
    def post(self , request):  
        other_user_id=request.data.get('user_id')
        if not other_user_id:
            return Response({"ERROR":"THE USER ID IS NOT FOUND"},status=400)
        users_id=sorted([request.user.id , other_user_id])
        room_name=f"{users_id[0]}_{users_id[1]}"
        
        room, created = Room.objects.get_or_create(
        name=room_name,
        defaults={'created_by': request.user}
        )
        return Response({"room":{"id" :room.id , "room_name":room.name}}, status=201)
        



class PostMessage(APIView):
    permission_classes =[IsAuthenticated]
    def post(self , request):
        room_id=request.data.get('room_id')
        text=request.data.get('text')
        
        if not room_id or not text :
            return Response({"Error": "The room or text is not available"} , status=400)
        
        room=Room.objects.get(id=room_id)
        data=Message.objects.create(room=room , sender=request.user , text=text)
        serializer=MessageSerializer(data)
        return Response(serializer.data)
    

class GetMessage(APIView):
    permission_classes = [IsAuthenticated]
    def get(self , request , roomid):
        if not roomid:
            return Response({"ERROR":"ID IS NOT GIVEN"},status=400)
        message=Message.objects.filter(room=roomid).order_by('timestamp')
        serializer=MessageSerializer(message , many=True)
        return Response(serializer.data)
        
        