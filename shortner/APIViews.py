from rest_framework import generics,permissions
from .models import Shorten,Tracker
from .serializers import ShortenSerializer,TrackerSerializer
from .permissions import IsCreatedBy
import re,string,random
from django.utils import timezone
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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
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
    
        
class TrackerView(generics.ListAPIView):
    permission_classes = (IsCreatedBy,)
    serializer_class = TrackerSerializer
    def get_queryset(self):
        return Tracker.objects.filter(short_id=self.short_id)
    def get(self,request,**kwargs):
        self.short_id = kwargs.get("short_id")
        
        return super().get(request,**kwargs)
