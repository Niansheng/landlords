from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from properties.models import Estate, Contract


class EstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estate
        fields = ('id', 'name', 'address', 'postcode', 'owner')


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('id', 'estate', 'tenant', 'start_date', 'end_date')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'groups', 'password')


class EstateViewSet(viewsets.ModelViewSet):
    queryset = Estate.objects.all()
    serializer_class = EstateSerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'api/users', UserViewSet)
router.register(r'api/estates', EstateViewSet)
router.register(r'api/contracts', ContractViewSet)
