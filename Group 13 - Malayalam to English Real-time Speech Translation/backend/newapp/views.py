from django.http import JsonResponse, StreamingHttpResponse
from django.views.generic.list import ListView
# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView, status
from .serializers import UserSerializer, ChatSerializer, FavouriteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .models import Chat, Favourite
from rest_framework.decorators import api_view, renderer_classes
from m2e.settings import MEDIA_ROOT
from mal2eng import final

translated_audio_received = {}
translated_text = {}
polling = {}


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(self, user):
        data = super().get_token(user)
        data['id'] = user.id
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class InitChatView(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):

        receiver = User.objects.get(id = request.data['receiver'])
        chat_object = Chat.objects.filter(sender = self.request.user, receiver = receiver)
        if chat_object.exists():
            return Response({"id" : chat_object[0].id}, status=status.HTTP_200_OK)

        serializer = ChatSerializer(data = request.data)
        if serializer.is_valid():
            o = serializer.save(sender = self.request.user)
            return Response({"id" : o.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetChatView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sender_id = dict(self.request.GET).get('sender', "")[0]

        sender = User.objects.get(id = sender_id)
        receiver = self.request.user

        chat_object = Chat.objects.filter(sender = sender, receiver = receiver)

        return chat_object


class GetUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        search_key = dict(self.request.GET).get('key', "")[0]
       
        if search_key:
            queryset = User.objects.filter(id__regex = f'[^{self.request.user.id}]').filter(username__iregex = f'{search_key}')
        else:
            queryset = User.objects.filter(id__regex = f'[^{self.request.user.id}]')
        return queryset

class GetUserInfoView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class GetOnlineStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sender_chat_id = request.GET['sender_chat_id']
        return Response({"status" : polling.get(sender_chat_id, False)}, status = status.HTTP_200_OK)

class SetOnlineStatus(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver_chat_id = request.data['receiver_chat_id']
        polling[receiver_chat_id] = False
        return Response({"status" : "SUCCESS"}, status = status.HTTP_200_OK)
    
class SetFavouriteUser(generics.CreateAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        
        serializer.save(user = self.request.user)

        return Response(serializer.data, status = status.HTTP_201_CREATED)

class GetFavouriteUsers(generics.ListAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        print(self.request.GET)
        id = self.request.GET.get('id', "")
        if id:
            check_user = User.objects.get(id = int(id))
            return self.request.user.favourites.filter(favourite_user = check_user)

        return self.request.user.favourites.all()
    
class RemoveFavouriteUser(generics.DestroyAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]


import asyncio
import json
async def sse_stream(request):
   
    receiver_chat_id = request.GET['receiver_chat_id']
    polling[receiver_chat_id] = True

    print('sse stream init point', receiver_chat_id)
 
    async def event_stream():
      
        while True:
            polling[receiver_chat_id] = True

            print('polling',receiver_chat_id)
            
            if os.path.exists(f'{MEDIA_ROOT}{receiver_chat_id}_eng.wav') and not translated_audio_received.get(receiver_chat_id, True):
                event_data = { "audio_uri" : f'{receiver_chat_id}_eng.wav', "text" : f'{translated_text[receiver_chat_id]}' }
                yield f'data: {json.dumps(event_data)}\n\n'
                translated_audio_received[receiver_chat_id] = True
                translated_text[receiver_chat_id] = ""
                #os.remove(f'{MEDIA_ROOT}{chat_id}_mal.wav')
                break
            await asyncio.sleep(1)
        
        polling[receiver_chat_id] = False
       
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
   
    return response

def mal_text_to_eng_speech(mal_text, file_id, self_receive = False):
            #final.mal_to_eng_speech(f'{MEDIA_ROOT}{chat_id}_mal.wav')
            #final.mal_text_to_english_speech(mal_text, f'{MEDIA_ROOT}{chat_id}_eng.wav')
            eng_text = final.translate_mal_to_eng(mal_text)
            print('translated')
            final.english_text_to_speech(eng_text, f'{MEDIA_ROOT}{file_id}_eng.wav')
            print('speeched')

            if self_receive:
                return {"english_text" : eng_text, "file_name" : f'{file_id}_eng.wav'}

            chat_id = file_id

            translated_text[chat_id] = eng_text
            translated_audio_received[chat_id] = False


import os
import threading 
import random
import string

class Translate(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        mal_text = request.GET['mal_text']
        file_id = "".join(random.choices(string.ascii_letters+string.digits, k = 15))
        result = mal_text_to_eng_speech(mal_text, file_id, True)
        return Response({"status" : "SUCCESS", "eng_text" : result["english_text"], "uri" : result["file_name"] }, status = status.HTTP_200_OK)


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def send_audio(request):
    try:        
        self_receive = False
        if request.method == 'POST':
            audio_file = request.FILES.get('audio')
            file_id = request.POST.get('chat_id', "")
            
            print(file_id)
            if not file_id:
                file_id = "".join(random.choices(string.ascii_letters+string.digits, k = 15))
                self_receive = True
            
            with open(f'{MEDIA_ROOT}{file_id}_mal.3gp', 'wb+') as file:
                for chunk in audio_file.chunks():
                    file.write(chunk)

            if os.path.exists(f'{MEDIA_ROOT}{file_id}_mal.wav'):    
                os.remove(f'{MEDIA_ROOT}{file_id}_mal.wav')

            os.system(f'ffmpeg -i {MEDIA_ROOT}{file_id}_mal.3gp {MEDIA_ROOT}{file_id}_mal.wav')
            mal_text =  final.malayalam_speech_to_text(f'{MEDIA_ROOT}{file_id}_mal.wav')
            
            if self_receive:
                result = mal_text_to_eng_speech(mal_text, file_id, True)
                english_text = result['english_text']
                uri = result['file_name']
                return Response({"status" : "SUCCESS", "mal_text" : mal_text, "eng_text" : english_text, "uri" : uri }, status = status.HTTP_200_OK)


            x = threading.Thread(target = mal_text_to_eng_speech, args = (mal_text, file_id))
            x.start()

            #final.mal_speech_to_english_speech(f'{MEDIA_ROOT}{chat_id}_mal.wav', f'{MEDIA_ROOT}{chat_id}_eng.wav')
            #data[chat_id] = True
            return Response({"status" : "SUCCESS", "text" : mal_text}, status = status.HTTP_200_OK)
            


    except Exception as e:
            print(e)
            return Response({"status" : "FAILURE"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
