from rest_framework import serializers
from users.models import MyUser, Patient, Facility
from gestion.models import Order
import uuid


class PatientRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['email', 'first_name', 'last_name', 'password', 'address',
                  'phone', 'id', 'age', 'isFacility', 'latitude', 'longitude']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = Patient(email=self.validated_data['email'], first_name=self.validated_data['first_name'],
                       last_name=self.validated_data['last_name'], age=self.validated_data['age'],
                       address=self.validated_data['address'], phone=self.validated_data['phone'], isFacility=self.validated_data['isFacility'], latitude=self.validated_data['latitude'], longitude=self.validated_data['longitude'], id=uuid.uuid4())
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class FacilityRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['email', 'name', 'Description', 'password', 'address', 'phone', 'id', 'price', 'ratting', 'latitude', 'longitude'
                  ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = Facility(email=self.validated_data['email'], name=self.validated_data['name'],
                        Description=self.validated_data['Description'], price=self.validated_data['price'],
                        ratting=self.validated_data['ratting'],
                        address=self.validated_data['address'], phone=self.validated_data['phone'],
                        latitude=self.validated_data['latitude'], longitude=self.validated_data['longitude'],
                        id=uuid.uuid4())
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class OrderRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'date', 'Description', 'patient', 'facility']

    def save(self):
        order = Order(date=self.validated_data['date'], patient=self.validated_data['patient'],
                      facility=self.validated_data['facility'],
                      Description=self.validated_data['Description'], id=uuid.uuid4())
        order.save()
        return order


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(
        style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError(
                {'current_password': 'Does not match'})
        return value


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'date']


class PatientSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['id', 'address', 'phone', 'age', 'email', 'latitude', 'longitude',
                  'first_name', 'last_name', 'orders']

    def get_orders(self, instance):
        orders = instance.order_set.all()
        serialize = OrdersSerializer(orders, many=True)
        return (serialize.data)


class PatientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'email']


class FacilitySerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField()

    class Meta:
        model = Facility
        fields = ['id', 'address', 'phone', 'email', 'name', 'Patients', 'orders', 'Description',
                  'price',
                  'ratting',
                  'latitude', 'longitude']

    def get_orders(self, instance):
        orders = instance.order_set.all()
        serialize = OrdersSerializer(orders, many=True)
        return (serialize.data)


class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id', 'name', 'address', 'latitude', 'longitude']
