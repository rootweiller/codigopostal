from django.urls import path, include
from rest_framework import routers

from postcodes.codes import PostCodeAPIView
from postcodes.file_upload import FileUploaderAPIView

router = routers.DefaultRouter()

router.register('upload', FileUploaderAPIView)
router.register('search/postcode', PostCodeAPIView)

urlpatterns = [
    path('', include(router.urls))
]