from django.urls import path,re_path
from . import APIViews
app_name = "app_shortner"
urlpatterns = [
    re_path("^g/(?P<pk>\w{12})/$",APIViews.DetailView.as_view(),name="get_short"),
    re_path("^t/(?P<short_id>\w{12})/$",APIViews.TrackerView.as_view(),name="tracker_log"),
    path("create/",APIViews.CreateView.as_view(),name="create_short"),
]