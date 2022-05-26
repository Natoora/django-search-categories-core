def search_categories_deployment_tasks():
    """
    Run these tasks BEEFORE any db sync occurs.
    These tasks populate the new search category format with the old data,
    also separating out any sc that are applied across both apps.
    """
    populate_search_category_app_type()
    populate_search_category_products()
    populate_search_category_hierarchy()


def populate_search_category_products():
    """
    On deployment, sync the old product_bases data into the new products field
    """
    print('Starting product population')
    errors = []
    from products.models import SearchCategory
    scs = SearchCategory.objects.all()
    for sc in scs:
        try:
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
        except Exception as e:
            errors.append(e)
    print('Finished product population')
    if errors:
        print('ERRORS:')
        for e in errors:
            print(e)


def populate_search_category_app_type():
    """
    On deployment, update the new app_type field with the old SC's hd_app or pro_app,
    If both 'hd' and 'pro' are selected make a new SC
    If neither are selected - select 'hd'
    """
    from products.models import SearchCategory
    scs = SearchCategory.objects.all()
    errors = []
    print('Starting app type population')
    for sc in scs:
        try:
            if (sc.hd_app and sc.pro_app):
                print(f'Create a new one: {sc.name}')
                sc.app_type = sc.HD
                sc.save()
                new_sc = SearchCategory.objects.create()
                new_sc.name = sc.name
                new_sc.background_image = sc.background_image
                new_sc.tile_dimensions = sc.tile_dimensions
                new_sc.enabled = sc.enabled
                new_sc.app_type = sc.PRO
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
                sc.save()
                continue
            elif sc.pro_app and not sc.hd_app:
                print(f'PRO app {sc.name}')
                sc.app_type = sc.PRO
                sc.save()
                continue
            print(f'Neither selected {sc.name}')
            sc.app_type = sc.HD
            sc.save()
        except Exception as e:
            errors.append(e)
    print('Finished app type population')
    if errors:
        print('ERRORS:')
        for e in errors:
            print(e)


def populate_search_category_hierarchy():
    """
    On deployment, reset hierarchies for SC
    """
    print('Starting hierarchy task')
    errors = []
    from products.models import SearchCategory
    types = ['HD', 'PRO']
    for t in types:
        try:
            scs = SearchCategory.objects.filter(app_type=t).order_by('hierarchy')
            counter = 0
            for index, sc in enumerate(scs):
                print(sc, index)
                counter += 1
                sc.hierarchy = counter
            # Bulk update so not to trigger save method and move other hierarchies...
            SearchCategory.objects.bulk_update(scs, ['hierarchy'])
        except Exception as e:
            errors.append(e)
    print('Finished hierarchy task')
    if errors:
        print('ERRORS:')
        for e in errors:
            print(e)
