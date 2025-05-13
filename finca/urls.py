from django.urls import path
from .views import MyFincaViewSet, PostViewSet

finca_view = MyFincaViewSet.as_view(
    {"get": "list", "put": "update", "post": "create"}
)

post_view = PostViewSet.as_view(
    {
        "get"   : "list",      # /posts/
        "post"  : "create",
    }
)
post_detail = PostViewSet.as_view(
    {
        "patch" : "partial_update",
        "delete": "destroy",
    }
)

urlpatterns = [
    path("",              finca_view,         name="mi-finca"),          # /api/finca/
    path("posts/",        post_view,          name="finca-posts"),       # /api/finca/posts/
    path("posts/<int:pk>/", post_detail,      name="finca-post-detail"), # /api/finca/posts/<id>/
]
