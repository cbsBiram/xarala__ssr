from paydunya import InvoiceItem, Store, Invoice


# Configuration des informations de votre service/entreprise
infos = {
    "name": "Xarala Academy",  # Seul le nom est requis
    "tagline": "La technologie dans votre langue",
    "postal_address": "Sicap Mbao, Extension",
    "phone_number": "763772260",
    "website_url": "https://www.xarala.co",
    "logo_url": "https://www.xarala.co/static/images/logo.32b513268679.png",
}

store = Store(**infos)


def get_items(order_items):
    items = [
        InvoiceItem(
            name=item.course.title,
            quantity=item.quantity,
            unit_price=str(item.price),
            total_price=str(item.price * item.quantity),
            description=f"Cours {item.course.title}",
        )
        for item in order_items
    ]
    return items


def get_invoice(items, total_cost, host):
    invoice = Invoice(store)
    invoice.add_items(items)
    invoice.total_amount = int(total_cost)
    invoice.cancel_url = f"{host}/payment/cancel/"
    invoice.return_url = f"{host}/payment/done/"
    return invoice.create()


def invoice_confirmation(token):
    invoice = Invoice(store)
    return invoice.confirm(token)
