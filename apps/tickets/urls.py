from django.urls import path, include

from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token

from apps.tickets.views import TicketViewSet, ticket_time_entry_detail

app_name = 'tickets'
router = SimpleRouter(trailing_slash=False)
router.register('tickets', TicketViewSet)

urlpatterns = [
    path('token', obtain_jwt_token, name='login'),
    path('', include(router.urls)),
    path('time-entries/<int:pk>', ticket_time_entry_detail, name='ticket-time-entry-detail')
]
