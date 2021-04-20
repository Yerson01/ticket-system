from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.tickets.models import Employee
from apps.tickets.serializers import ManageEmployeeSerializer


class ManageEmployeeView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = ManageEmployeeSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ManageEmployeeSerializer
        return super().get_serializer_class()


manage_employee = ManageEmployeeView.as_view()


