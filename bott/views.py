import logging
import asyncio
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .bot import bot_tele
from .models import User, Post
from .serializers import UserSerializer, PostSerializer
from rest_framework import viewsets

logger = logging.getLogger(__name__)

@csrf_exempt
def index(request):
    if request.method == 'POST':
        data = request.body
        res = json.loads(data.decode('utf-8'))

        # Log the JSON data to avoid print issues
        logger.info(json.dumps(res, ensure_ascii=False, indent=4))

        asyncio.run(bot_tele(res))
        return HttpResponse("ok")
    else:
        return render(request, 'index.html')
    


# APIs will follow here

# ViewSets
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

