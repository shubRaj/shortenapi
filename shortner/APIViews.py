from rest_framework import generics,permissions
from .models import Shorten,Tracker
from django.urls import reverse_lazy
from .serializers import (
    ShortenSerializer,TrackerSerializer,CreateShortenSerializer
)
from .permissions import IsCreatedBy,IsCreatedByOrReadOnly
import re,string,random
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
def find_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
def find_device(ua):
    regex = re.compile(r'\(.*?\)')
    try:
        info = regex.findall(ua)[0].strip("()").split(";")
        return info[1]
    except:
        return ua
def generate_shorten_tracker():
    chars = string.ascii_letters+string.digits
    shorten = "".join([random.choice(chars) for _ in range(12)])
    return shorten
class DetailView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsCreatedByOrReadOnly,)
    queryset = Shorten.objects.all()
    serializer_class = ShortenSerializer
    def get(self,request,**kwargs):
        ua = request.META.get("HTTP_USER_AGENT","unknown")
        Tracker.objects.create(
            short_id=self.get_object(),
            ip = find_ip(request),
            device = find_device(ua),
            browser = ua.split("/")[0],
            logged_on = timezone.now()
        )
        return super().get(request,**kwargs)
    
class CreateView(generics.CreateAPIView):
    serializer_class = CreateShortenSerializer
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            while True:
                short_id = generate_shorten_tracker()
                if not Shorten.objects.filter(short_id=short_id).exists():
                    break
            print(request.user)
            serializer.save(short_id=short_id,created_by=request.user)
            return Response(
                {
                    "short_url":f"{request.scheme}://{request.get_host()}{reverse_lazy('shortner:get_short',args=(serializer.instance.short_id,))}"
                    },
                    status=status.HTTP_201_CREATED
                    )
class TrackerView(generics.ListAPIView):
    permission_classes = (IsCreatedBy,)
    serializer_class = TrackerSerializer
    def get_queryset(self):
        return Tracker.objects.filter(short_id=self.short_id)
    def get(self,request,**kwargs):
        self.short_id = kwargs.get("short_id")
        
        return super().get(request,**kwargs)
