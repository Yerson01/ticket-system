from django.urls import path, include

from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token

from apps.tickets import views

app_name = 'tickets'
router = SimpleRouter(trailing_slash=False)
router.register('tickets', views.TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('employees', views.manage_employee, name='manage-employees'),
    path('reports', views.ticket_report_list, name='report-list'),
    path('time-entries/<int:pk>', views.ticket_time_entry_detail, name='ticket-time-entry-detail'),
    path('token', obtain_jwt_token, name='login'),
]
