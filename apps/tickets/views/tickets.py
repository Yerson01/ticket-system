from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.tickets.models import Ticket, TicketTimeEntry
from apps.tickets.serializers import TicketSerializer, TicketTimeEntrySerializer


class TicketViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action == 'time_entries':
            return TicketTimeEntrySerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()

        if self.action == 'time_entries':
            ticket = self.get_object()
            context.update(ticket=ticket, employee=self.request.user)

        return context

    @action(
        methods=['GET', 'POST'],
        detail=True,
        url_path='time-entries',
        url_name='time-entry-list'
    )
    def time_entries(self, request, *args, **kwargs):
        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            queryset = self.get_object().time_entries.all()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)


class TicketTimeEntryDetail(DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = TicketTimeEntry.objects.all()
    serializer_class = TicketTimeEntrySerializer

    def check_object_permissions(self, request, obj):
        if obj.employee.id != request.user.id:
            raise PermissionDenied('Only the owner of time entry can edit it')

        super().check_object_permissions(request, obj)


ticket_time_entry_detail = TicketTimeEntryDetail.as_view({
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})
