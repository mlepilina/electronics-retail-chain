from rest_framework import serializers

from sales_chain.models import Supplier, Contacts, Product


class ContactsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contacts
        fields = [
            'email',
            'country',
            'city',
            'street',
            'house_number',
        ]


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = [
            'supplier_type',
            'title',
            'parent',
        ]


class CreateSupplierSerializer(serializers.Serializer):

    supplier = SupplierSerializer()
    contacts = ContactsSerializer()


class ProductSerializer(serializers.ModelSerializer):
    supplier_title = SupplierSerializer(source='title', read_only=True)

    class Meta:
        model = Product
        fields = [
            'title',
            'model',
            'market_launch_date',
            'supplier_title',
        ]
