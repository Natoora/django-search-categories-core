def populate_search_category_products():
    """
    On deployment, sync the old product_bases data into the new products field
    """
    from products.models import SearchCategory
    scs = SearchCategory.objects.all()
    for sc in scs:
        pbs = sc.product_bases.all()
        for pb in pbs:
            if sc.app_type == "PRO":
                products = pb.product_set.filter(trade__configuration__natoora_pro=True)
                for p in products:
                    sc.products.add(p)
                    sc.save()
            if sc.app_type == "HD":
                products = pb.product_set.filter(trade__configuration__natoora_app=True)
                for p in products:
                    sc.products.add(p)
                    sc.save()


# def populate_search_category_hierarchy():
#     """
#     On deployment, update the new app specific hierarchies with the old generic one
#     """
#     pass
#     # from products.models import SearchCategory
#     # scs = SearchCategory.objects.all()


def populate_search_category_app_type():
    """
    On deployment, update the new app_type field with the old SC's hd_app or pro_app,
    If both 'hd' and 'pro' are selected make a new SC
    If neither are selected - select 'hd'
    """
    from products.models import SearchCategory
    scs = SearchCategory.objects.all()

    for sc in scs:
        print(sc.hd_app, sc.pro_app)
        if (sc.hd_app and sc.pro_app) or (sc.name == 'Melilot' or sc.name == 'Melilot Farm'):
            print(f'Create a new one: {sc.name}')
            sc.app_type = sc.HD
            # sc.hierarchy_hd = sc.hierarchy
            sc.save()
            new_sc = SearchCategory.objects.create()
            new_sc.name = sc.name
            new_sc.hierarchy = sc.hierarchy
            # new_sc.hierarchy_pro = sc.hierarchy
            new_sc.background_image = sc.background_image
            new_sc.tile_dimensions = sc.tile_dimensions
            new_sc.enabled = sc.enabled
            new_sc.app_type = sc.PRO
            new_sc.save()
            product_bases = sc.product_bases.all()
            for p in product_bases:
                new_sc.product_bases.add(p)
            products = sc.products.all()
            for p in products:
                new_sc.products.add(p)
            new_sc.save()
            continue
        elif sc.hd_app and not sc.pro_app:
            print(f'HD app {sc.name}')
            sc.app_type = sc.HD
            # sc.hierarchy_hd = sc.hierarchy
            sc.save()
            continue
        elif sc.pro_app and not sc.hd_app:
            print(f'PRO app {sc.name}')
            sc.app_type = sc.PRO
            # sc.hierarchy_pro = sc.hierarchy
            sc.save()
            continue

        print(f'Neither selected {sc.name}')
        sc.app_type = sc.HD
        # sc.hierarchy_hd = sc.hierarchy
        sc.save()





