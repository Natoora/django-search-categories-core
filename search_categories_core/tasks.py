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
                products = pb.product_set.filter(trade__configuration__natoora_pro="WHOLESALE")
                sc.products.add(products)
            if sc.app_type == "HD":
                products = pb.product_set.filter(trade__configuration__natoora_app="HOME_DELIVERY")
                sc.products.add(products)
