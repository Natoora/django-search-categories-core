from django.contrib import admin


class _BaseAdmin(admin.ModelAdmin):
    """
    Sections that are common to admin pages on both WS and the apps.
    """
    fields = [
        "name",
        "code",
        "hierarchy",
        "hd_app",
        "pro_app",
        "app_type",
        "background_image",
        "sub_category"
    ]
    list_display = [
        "hierarchy",
        "name",
        "code",
        "hd_app",
        "pro_app",
        "app_type",
    ]
    search_fields = [
        "name",
        "code"
    ]
    list_filter = [
        "hd_app",
        "pro_app",
        "app_type"
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
        "products"
    ]
    readonly_fields = [
        "code",
        "app_type",
        "hd_synchronised",
        "pro_synchronised"
    ]
    list_display = _BaseAdmin.list_display + [
        "hd_synchronised",
        "pro_synchronised",
        "app_type",
    ]
    list_filter = _BaseAdmin.list_filter + [
        "hd_synchronised",
        "pro_synchronised"
    ]
    list_editable = [
        "hd_app",
        "pro_app"
    ]
    filter_horizontal = [
        "product_bases",
        "products"
    ]


class AppSearchCategoryAdmin(_BaseAdmin):
    """
    App SearchCategory Model admin page.
    """
    fields = _BaseAdmin.fields + ["products"]
    readonly_fields = fields

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
