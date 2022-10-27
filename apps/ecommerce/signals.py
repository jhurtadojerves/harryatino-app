def reserve_stock(sender, instance, created, **kwargs):
    """Signal to reserve stock"""
    if created:
        instance.product.reserved_stock += 1
        instance.product.save(update_fields=["reserved_stock"])


def cancel_reserve_stock(sender, instance, **kwargs):
    instance.product.reserved_stock -= 1
    instance.product.save(update_fields=["reserved_stock"])
