from paydunya import InvoiceItem, Store, Invoice


def get_store():
    infos = {
        "name": "Xarala",  # Seul le nom est requis
        "tagline": "Xarala Academy",
        "postal_address": "Sicap Mbao, Extension",
        "phone_number": "763772260",
        "website_url": "https://www.xarala.co",
        "logo_url": "https://www.xarala.co/static/images/logo.32b513268679.png",
    }
    store = Store(**infos)
    return store


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


def get_user_and_course(course_id, user_id):
    user_and_course = [
        ("course_id", course_id),
        ("user_id", user_id),
    ]
    return user_and_course


def get_invoice(items, total_cost, host, custom_data=None):
    store = get_store()
    invoice = Invoice(store)
    invoice.add_items(items)
    invoice.add_custom_data(custom_data)
    invoice.total_amount = int(total_cost)
    invoice.cancel_url = f"{host}/payment/cancel/"
    invoice.return_url = f"{host}/payment/done/"
    return invoice.create()


def invoice_confirmation(token):
    store = get_store()
    invoice = Invoice(store)
    return invoice.confirm(token)
