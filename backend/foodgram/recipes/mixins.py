from rest_framework import mixins, viewsets


class ReadOnlyViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    pass
