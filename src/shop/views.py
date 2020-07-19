from django.views.generic import TemplateView


class ShopHomePage(TemplateView):
    template_name = "shop/product_list.html"
