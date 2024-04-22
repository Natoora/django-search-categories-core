import blurhash
import logging
from io import BytesIO

logger = logging.getLogger(__name__)


class SearchCategorySyncService:
    """Logic to create/update WS search categories and add/remove products to the defined app"""

    def __init__(self, WsProdModel, WsCatModel, AppProdModel, AppCatModel, image_destination, destination_app):
        """Setup service with objects to sync.

        :param WsProdModel: Class, WS Product model.
        :param WsCatModel: Class, WS SearchCategory model.
        :param AppProdModel: Class, App Product model.
        :param AppCatModel: Class, App SearchCategory model.
        :param image_destination: Str, path to SCP images to.
        :param destination_app: Str, which app to sync (e.g. hd or pro).
        """
        self.WsProdModel = WsProdModel
        self.WsCatModel = WsCatModel
        self.AppProdModel = AppProdModel
        self.AppCatModel = AppCatModel
        self.image_destination = image_destination
        self.destination_app = destination_app

    def sync(self):
        """Update/create App search categories for
        any WS ones which are not synchronised.
        """
        categories = self.categories_to_sync()
        for ws_sc in categories:
            try:
                app_sc = self.update_app_search_category(ws_sc=ws_sc)
                self.add_products(ws_sc=ws_sc, app_sc=app_sc)
                self.remove_products(ws_sc=ws_sc, app_sc=app_sc)
                self.set_category_to_synchronised(ws_sc)
            except Exception as e:
                logger.exception(f"Exception syncing search category to app - category id: {ws_sc.id}: {e}")
                continue

    def set_category_to_synchronised(self, category):
        """Set WS Search Categories to synchronised as TRUE"""
        self.WsCatModel.objects.filter(id=category.id).update(synchronised=True)

    def update_app_search_category(self, ws_sc):
        """Update/create app search category to reflect the WS one.

        :param ws_sc: WsSearchCategory.
        :return: app_sc: AppSearchCategory.
        """
        try:
            app_c = self.AppCatModel.objects.get(code=ws_sc.code)
        except self.AppCatModel.DoesNotExist:
            app_c = self.AppCatModel()
            app_c.code = ws_sc.code
        app_c.name = ws_sc.name
        app_c.app_type = ws_sc.app_type
        app_c.hierarchy = ws_sc.hierarchy
        app_c.tile_dimensions = ws_sc.tile_dimensions
        app_c.background_image = ws_sc.background_image
        app_c.image_cdn = ws_sc.image_cdn
        app_c.image_blurred_hash = ws_sc.image_blurred_hash
        app_c.enabled = ws_sc.enabled
        app_c.deleted = ws_sc.deleted
        if hasattr(ws_sc, "parent") and ws_sc.parent:
            try:
                app_parent_cat = self.AppCatModel.objects.get(code=ws_sc.parent.code)
                app_c.parent = app_parent_cat
            except self.AppCatModel.DoesNotExist:
                pass
        app_c.save()
        return app_c

    def add_products(self, ws_sc, app_sc):
        """Add the HD products for the WS Search Category's
        product bases to the app Search Category.

        :param ws_sc: WsSearchCategory.
        :param app_sc: AppSearchCategory.
        """
        ws_sc_products = ws_sc.products.all()
        if ws_sc_products:
            for ws_p in ws_sc_products:
                app_p = self.AppProdModel.objects.filter(code=ws_p.code).first()
                if app_p:  # The product may not have been synchronised yet
                    app_sc.products.add(app_p)

    def remove_products(self, ws_sc, app_sc):
        """Remove any products from the app search category
        which are no longer in the WS search category.

        :param ws_sc: WsSearchCategory.
        :param app_sc: AppSearchCategory.
        """
        for app_p in app_sc.products.all():
            try:
                ws_p = self.WsProdModel.objects.get(code=app_p.code)
                if not ws_sc.products.filter(code=ws_p.code):
                    app_sc.products.remove(app_p)
            except WsProdModel.DoesNotExist:
                # Product does not exist on WS
                app_sc.products.remove(app_p)
                continue

    def categories_to_sync(self):
        """Return a queryset of SearchCategories to sync depending on the app destination.
        :return: QuerySet, SearchCategory.
        """
        categories = self.WsCatModel.objects.filter(synchronised=False)
        if self.destination_app == "HD":
            categories = categories.filter(app_type="HD")
        elif self.destination_app == "PRO":
            categories = categories.filter(app_type="PRO")
        else:
            raise RuntimeError(
                f"The given app=({self.destination_app}) does not match HD or PRO in the category sync service."
            )
        return categories


def update_image_blurred_hash(category):
    """This method updates the input category's image_blurred_hash_field

    It is used in the pre_save, so only need to 'set' the field"""

    if category.background_image:
        image_content = category.background_image.read()
        hash_value = blurhash.encode(
            BytesIO(image_content), x_components=6, y_components=6
        )
        category.image_blurred_hash = hash_value
