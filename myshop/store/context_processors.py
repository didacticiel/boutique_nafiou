from .models import Customer
def cart_context(request):
    return {'cart': request.session.get('cart', {})}

def customer_context(request):
    customer_id = request.session.get('customer')
    customer = Customer.objects.get(id=customer_id) if customer_id else None
    return {'customer': customer}