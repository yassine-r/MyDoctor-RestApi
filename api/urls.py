from django.urls import path
from .views import FacilitiesView, FacilityView, PatientView, PatientsView, OrderssView, OrderView, \
    FacilityRegistrationView, PatientRegistrationView,PopularFacilitiesView, OrderRegistrationView, LoginView, LogoutView, OrderDeleteView,FindFacilitiesCategoryView,FindFacilitiesView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('patients/', PatientsView.as_view()),
    path('patients/register/', PatientRegistrationView.as_view(), name='register'),
    path('patients/<slug>/', PatientView.as_view()),

    path('facilities/', FacilitiesView.as_view()),
    path('facilities/popular/', PopularFacilitiesView.as_view()),
    path('facilities/find/<slug>/', FindFacilitiesView.as_view()),
    path('facilities/category/<slug>/', FindFacilitiesCategoryView.as_view()),
    path('facilities/register/', FacilityRegistrationView.as_view()),
    path('facilities/<slug>/', FacilityView.as_view()),

    path('orders/', OrderssView.as_view()),
    path('orders/register/', OrderRegistrationView.as_view()),
    path('orders/delete/', OrderDeleteView.as_view()),
    path('orders/<slug>/', OrderView.as_view()),

]
