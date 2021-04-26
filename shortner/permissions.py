from rest_framework import permissions
from rest_framework.authtoken.models import Token
class IsCreatedBy(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        my_token = request.META.get("HTTP_AUTHORIZATION")
        if my_token:
            tokens = Token.objects.filter(key=my_token.split()[-1])
            if tokens.exists() and (tokens.first().user == obj.created_by):
                return True
        elif request.user == obj.created_by:
            return True
        return False
    # def has_permission(self,request,view):
    #     return False
    