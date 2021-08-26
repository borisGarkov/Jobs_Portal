from django.views.generic import TemplateView


class PricingListView(TemplateView):
    template_name = 'pricing-list.html'
