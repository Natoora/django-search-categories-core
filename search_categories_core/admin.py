from django.contrib import admin


class _BaseAdmin(admin.ModelAdmin):
    """
    Sections that are common to admin pages on both WS and the apps.
    """
    fields = [
        "name",
        "code",
        "hierarchy",
        "enabled",
        "background_image",
        "hd_synchronised",
        "pro_synchronised",
        "sub_category"
    ]
    readonly_fields = [
        "code"
    ]
    list_display = [
        "hierarchy",
        "name",
        "code",
        "enabled",
        "hd_synchronised",
        "pro_synchronised"
    ]
    search_fields = [
        "name",
        "code"
    ]
    list_filter = [
        "enabled",
        "hd_synchronised",
        "pro_synchronised"
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return super().has_view_permission(request)


class WsSearchCategoryAdmin(_BaseAdmin):
    """
    WS SearchCategory Model admin page.
    """
    fields = _BaseAdmin.fields + ["product_bases"]
    list_editable = [
        "enabled"
    ]
    filter_horizontal = [
        "product_bases"
    ]


class AppSearchCategoryAdmin(_BaseAdmin):
    """
    App SearchCategory Model admin page.
    """
    fields = _BaseAdmin.fields + ["products"]
    readonly_fields = fields
