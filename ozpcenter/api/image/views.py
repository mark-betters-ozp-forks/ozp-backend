"""
Views

TODO: POST on api/image (create/edit listing) w/ contentType and id fields
"""
import logging

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

import ozpcenter.access_control as access_control
import ozpcenter.permissions as permissions
import ozpcenter.model_access as generic_model_access
import ozpcenter.api.image.model_access as model_access
import ozpcenter.api.image.serializers as serializers
import ozpcenter.models as models


# Get an instance of a logger
logger = logging.getLogger('ozp-center')

class ImageTypeViewSet(viewsets.ModelViewSet):
    queryset = models.ImageType.objects.all()
    serializer_class = serializers.ImageTypeSerializer
    fields = ('name',)


class ImageViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return  models.Image.objects.for_user(self.request.user.username).all()

    serializer_class = serializers.ImageSerializer
    permission_classes = (permissions.IsUser,)

    def create(self, request):
        pass

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.ImageSerializer(queryset,
            many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Return an image, enforcing access control
        """
        queryset = self.get_queryset()
        image = get_object_or_404(queryset, pk=pk)
        image_path = model_access.get_image_path(pk)
        # TODO: enforce access control
        user = generic_model_access.get_profile(self.request.user.username)
        if not access_control.has_access(user.access_control.title,
            image.access_control.title):
            return Response(status=403)
        content_type = 'image/' + image.file_extension
        try:
            with open(image_path, "rb") as f:
                return HttpResponse(f.read(), content_type=content_type)
        except IOError:
            logger.error('No image found for pk %d' % pk)
            return Response(status=404)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        image = get_object_or_404(queryset, pk=pk)
        # TODO: remove from file system
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)