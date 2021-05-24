import os


class SearchCategorySyncService:
    """
    Logic to create/update WS search categories and add/remove products to the defined app.
    """

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
            app_sc = self.update_app_search_category(ws_sc=ws_sc)
            self.add_products(ws_sc=ws_sc, app_sc=app_sc)
            self.remove_products(ws_sc=ws_sc, app_sc=app_sc)
        self.set_sync_flags(categories=categories)

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
        app_c.enabled = ws_sc.enabled
        app_c.hierarchy = ws_sc.hierarchy
        app_c.tile_dimensions = ws_sc.tile_dimensions
        app_c.background_image.name = ws_sc.background_image.name
        app_c.save()
        if ws_sc.background_image.name:
            os.system(f"scp {ws_sc.background_image.path} {self.image_destination}")
        return app_c

    def add_products(self, ws_sc, app_sc):
        """Add the HD products for the WS Search Category's
        product bases to the app Search Category.

        :param ws_sc: WsSearchCategory.
        :param app_sc: AppSearchCategory.
        """
        for pb in ws_sc.product_bases.all():
            products = self.products_to_sync(product_base=pb)
            for ws_p in products:
                app_p = self.AppProdModel.objects.filter(code=ws_p.code).first()
                if app_p:  # The product may not have been syncrhonised yet
                    app_sc.products.add(app_p)

    def remove_products(self, ws_sc, app_sc):
        """Remove any products from the app search category
        which are no longer in the WS search category.

        :param ws_sc: WsSearchCategory.
        :param app_sc: AppSearchCategory.
        """
        for app_p in app_sc.products.all():
            ws_p = self.WsProdModel.objects.get(code=app_p.code)
            if not ws_sc.product_bases.filter(code=ws_p.product_base.code):
                app_sc.products.remove(app_p)

    def categories_to_sync(self):
        """Return a queryset of SearchCategories to sync depending on the app destination.

        :return: QuerySet, SearchCategory.
        """
        if self.destination_app == "HD":
            categories = self.WsCatModel.objects.filter(hd_synchronised=False)
        elif self.destination_app == "PRO":
            categories = self.WsCatModel.objects.filter(pro_synchronised=False)
        else:
            raise RuntimeError(
                f"The given app=({self.destination_app}) does not match HD or PRO in the category sync service."
            )
        return categories

    def products_to_sync(self, product_base):
        """Return a queryset of products to sync depending on the app destination.

        :param product_base: ProductBase model instance.
        :return: QuerySet, Products.
        """
        if self.destination_app == "HD":
            products = product_base.product_set.filter(trade__configuration__natoora_app=True)
        elif self.destination_app == "PRO":
            products = product_base.product_set.filter(trade__configuration__natoora_pro=True)
        else:
            raise RuntimeError(
                f"The given app=({self.destination_app}) does not match HD or PRO in the category sync service."
            )
        return products

    def set_sync_flags(self, categories):
        """Set sync flags depending on the app destination.

        :param categories: QuerySet, SearchCategory.
        """
        if self.destination_app == "HD":
            categories.update(hd_synchronised=True)
        elif self.destination_app == "PRO":
            categories.update(pro_synchronised=True)
        else:
            raise RuntimeError(
                f"The given app=({self.destination_app}) does not match HD or PRO in the category sync service."
            )
