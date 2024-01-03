from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from sales_chain.models import Supplier, Contacts, Product, Debt

admin.site.register(
    Supplier,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
    list_filter=(
        'contacts__country',
        'contacts__city',
    )
)

admin.site.register(Contacts)
admin.site.register(Product)
admin.site.register(Debt)
