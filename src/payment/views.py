import paydunya
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect, render

from django.conf import settings
from order.models import Order
from payment.services.paydunya import (
    get_invoice,
    get_items,
    get_user_and_course,
    invoice_confirmation,
)

# from .tasks import payment_completed

# Activer le mode 'test'. Le debug est à False par défaut
paydunya.debug = False

# Configurer les clés d'API
paydunya.api_keys = settings.PAYDUNYA_ACCESS_TOKENS


def payment_process(request):
    order_id = request.session.get("order_id")
    user = request.user
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    items = get_items(order.items.all())
    order_item_first = order.items.all()[0]
    custom_data = get_user_and_course(
        order_item_first.course.id,
        user.id,
    )
    try:
        successful, response = get_invoice(
            items,
            total_cost,
            request.get_host(),
            custom_data=custom_data,
        )
        if successful:
            # payment_completed.delay(order.id)
            return redirect(response.get("response_text"))
    except Exception:
        messages.error(request, "Une erreur s'est produit, veuillez ressayer")
    return redirect("cart:cart_detail")


def payment_done(request):
    token = request.GET.get("token")
    successful, response = invoice_confirmation(token)
    if successful:
        return render(request, "payment/done.html")
    messages.error(request, "Paiement non complete")
    return redirect("cart:cart_detail")


def payment_canceled(request):
    return render(request, "payment/canceled.html")
