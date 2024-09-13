from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden

class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role_id == 1 or not request.user.is_superuser:
            # Optionally redirect to login or show a permission denied page
            # return HttpResponseForbidden("You don't have permission to access this page.")
            raise PermissionDenied("You don't have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)