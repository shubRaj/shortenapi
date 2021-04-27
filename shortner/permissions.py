from rest_framework import permissions
class IsCreatedByOrReadOnly(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or obj.created_by == request.user:
            return True
        return False
class IsCreatedBy(permissions.BasePermission):
    def has_permission(self,request,view):
        setattr(view,"short_id",view.kwargs.get("short_id"))
        #can use reverse query too
        obj = view.get_queryset().first().short_id
        if request.user == obj.created_by:
            return True
        return False