import os


class SearchCategorySyncService:
    """
    Methods to synchronise search categories between the given WS and app models.
    """

    def __init__(self, WsProduct, WsCategory, AppProduct, AppCategory, image_scp_destination):
        """Setup service with objects to sync.

        :param WsProduct: Class, WS Product model.
        :param WsCategory: Class, WS SearchCategory model.
        :param AppProduct: Class, App Product model.
        :param AppCategory: Class, App SearchCategory model.
        :param image_scp_destination: Str, path to SCP images to.
        """
        self.WsProduct = WsProduct
        self.WsCategory = WsCategory
        self.AppProduct = AppProduct
        self.AppCategory = AppCategory
        self.image_scp_destination = image_scp_destination

    def sync(self):
        """Update/create App search categories for
        any WS ones which are not synchronised.
        """
        ws_search_categories = self.WsCategory.objects.filter(synchronised=False)
        for ws_sc in ws_search_categories:
            app_sc = self.update_app_search_category(ws_sc=ws_sc)
            self.add_products(ws_sc=ws_sc, app_sc=app_sc)
            self.remove_products(ws_sc=ws_sc, app_sc=app_sc)
        ws_search_categories.update(synchronised=True)

    def update_app_search_category(self, ws_sc):
        """Update/create app search category to reflect the WS one.

        :param ws_sc: WsSearchCategory.
        :return: app_sc: AppSearchCategory.
        """
        app_sc, _ = self.AppCategory.objects.update_or_create(
            code=ws_sc.code,
            defaults={
                "name": ws_sc.name,
                "enabled": ws_sc.enabled,
                "hierarchy": ws_sc.hierarchy,
                "tile_dimensions": ws_sc.tile_dimensions,
                "background_image": ws_sc.background_image.name
            }
        )
        if ws_sc.background_image.name:
            os.system(f"scp {ws_sc.background_image.path} {self.image_scp_destination}")
        return app_sc

    def add_products(self, ws_sc, app_sc):
        """Add the HD products for the WS Search Category's
        product bases to the app Search Category.

        :param ws_sc: WsSearchCategory.
        :param app_sc: AppSearchCategory.
        """
        for pb in ws_sc.product_bases.all():
            for ws_p in pb.product_set.filter(trade__configuration__natoora_app=True):
                app_p = self.AppProduct.objects.filter(code=ws_p.code).first()
                if app_p:  # The product may not have been syncrhonised yet
                    app_sc.products.add(app_p)

    def remove_products(self, ws_sc, app_sc):
        """Remove any products from the app search category
        which are no longer in the WS search category.

        :param ws_sc: WsSearchCategory.
        :param app_sc: AppSearchCategory.
        """
        for app_p in app_sc.products.all():
            ws_p = self.WsProduct.objects.get(code=app_p.code)
            if not ws_sc.product_bases.filter(code=ws_p.product_base.code):
                app_sc.products.remove(app_p)
