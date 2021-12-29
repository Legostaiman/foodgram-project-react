from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user and request.user.is_authenticated


class SubscribePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated or (view.action == 'list' and (
                    obj.user == request.user or request.user.is_staff))
