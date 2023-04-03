from django.contrib.auth.mixins import PermissionRequiredMixin


class ObjectPermissionRequiredMixin(PermissionRequiredMixin):
    def has_permission(self):
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms, self.get_object())
