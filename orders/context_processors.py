from .models import Order

def cart_unseen_count(request):
    if request.user.is_authenticated:
        count = Order.objects.filter(user=request.user, is_seen=False).count()
        return {'unseen_orders_count': count}
    return {'unseen_orders_count': 0}