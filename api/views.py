from api.serializers import PatientSerializer, FacilitySerializer, PatientsSerializer, FacilityRegistrationSerializer, \
    FacilitiesSerializer, PatientRegistrationSerializer, OrderSerializer, OrdersSerializer, OrderRegistrationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.contrib.auth import  login, logout
from .utils import get_tokens_for_user
from django.contrib.auth.hashers import check_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status

from gestion.models import Order
from users.models import Patient, Facility, MyUser



class PatientView(APIView):

    def get(self, request, slug, *args, **kwargs):
        patient = Patient.objects.get(id=slug)
        serialize = PatientSerializer(patient, many=False)
        return Response(serialize.data)


class PatientsView(APIView):
    def get(self, request, *args, **kwargs):
        patients = Patient.objects.all()
        serialize = PatientsSerializer(patients, many=True)
        return Response(serialize.data)


class PatientRegistrationView(APIView):
    def post(self, request):
        serializer = PatientRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FacilityView(APIView):
    def get(self, request, slug, *args, **kwargs):
        facility = Facility.objects.get(id=slug)
        serialize = FacilitySerializer(facility, many=False)
        return Response(serialize.data)
    

class FacilitiesView(APIView):
    def get(self, request, *args, **kwargs):
        facilities = Facility.objects.all()
        serialize = FacilitiesSerializer(facilities, many=True)
        return Response(serialize.data)

class PopularFacilitiesView(APIView):
    def get(self, request, *args, **kwargs):
        facilities = Facility.objects.filter(ratting__gte=8)
        serialize = FacilitiesSerializer(facilities, many=True)
        return Response(serialize.data)

class FindFacilitiesView(APIView):
    def get(self, request,slug, *args, **kwargs):
        facilities = Facility.objects.filter(name__icontains=slug)
        serialize = FacilitiesSerializer(facilities, many=True)
        return Response(serialize.data)

class FindFacilitiesCategoryView(APIView):
    def get(self, request,slug, *args, **kwargs):
        facilities = Facility.objects.filter(categories__icontains=slug)
        serialize = FacilitiesSerializer(facilities, many=True)
        return Response(serialize.data)
        


class FacilityRegistrationView(APIView):
    def post(self, request):
        serializer = FacilityRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderView(APIView):
    def get(self, request, slug, *args, **kwargs):
        order = Order.objects.get(id=slug)
        serialize = OrderSerializer(order, many=False)
        return Response(serialize.data)


class OrderssView(APIView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serialize = OrdersSerializer(orders, many=True)
        return Response(serialize.data)


class OrderRegistrationView(APIView):
    def post(self, request):
        serializer = OrderRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            facility = Facility.objects.get(id=request.data.get('facility'))
            patient= Patient.objects.get(id=request.data.get('patient'))
            if (facility is not None) and (patient is not None):
                if  patient not in facility.Patients.all():
                    
                    facility.Patients.add(patient)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDeleteView(APIView):
    def post(self, request):
        if 'id' not in request.data:
            return Response(
                {"msg": "Order does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        id = request.data.get('id')
        order = Order.objects.get(id=id)
        if order is not None:
            order.delete()
            return Response(
                {"msg": "Order deleted!"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"msg": "Order does not exists"},
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data.get('email')
        password = request.data.get('password')
        user = MyUser.objects.get(email=email)
        if check_password(password, user.password):
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data, 'isFacility':user.isFacility,'id': user.id}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)
