from django.contrib import admin


class _BaseAdmin(admin.ModelAdmin):
    """
    Sections that are common to admin pages on both WS and the apps.
    """
    fields = [
        "name",
        "code",
        "hierarchy",
        "app_type",
        "background_image",
        "image_cdn",
        "image_blurred_hash",
        "sub_category",
        "enabled",
        "deleted",
    ]
    list_display = [
        "hierarchy",
        "name",
        "code",
        "enabled",
        "deleted"
    ]
    search_fields = [
        "name",
        "code"
    ]
    list_filter = [
        "app_type",
    ]

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return super().has_view_permission(request)


class WsSearchCategoryAdmin(_BaseAdmin):
    """
    WS SearchCategory Model admin page.
    """
    fields = _BaseAdmin.fields + [
        "product_bases",
        "products",
        "synchronised",
        "deleted_at"
    ]
    readonly_fields = [
        "code",
        "synchronised",
    ]
    list_display = _BaseAdmin.list_display + [
        "synchronised",
        "app_type",
    ]
    list_filter = _BaseAdmin.list_filter + [
        "synchronised",
    ]
    filter_horizontal = [
        "product_bases",
        "products"
    ]


class AppSearchCategoryAdmin(_BaseAdmin):
    """
    App SearchCategory Model admin page.
    """
    fields = _BaseAdmin.fields
    readonly_fields = fields

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
