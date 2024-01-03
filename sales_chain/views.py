from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from sales_chain.models import Supplier, Contacts, Product
from sales_chain.serializers import ProductSerializer, CreateSupplierSerializer, SupplierSerializer, ContactsSerializer


class SupplierView(APIView):

    def post(self, request: Request):
        """Создать нового поставщика"""
        serializer = CreateSupplierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        contacts = Contacts(**serializer.validated_data["contacts"])
        contacts.save()
        supplier = Supplier(contacts_id=contacts.pk, **serializer.validated_data["supplier"])
        supplier.save()

        response_data = {
            'id': supplier.pk
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def get(self, request: Request, *args, **kwargs):
        """Получить список всех поставщиков по типу"""
        suppliers = Supplier.objects.filter(supplier_type=request.data["detail"]).values(
            'supplier_type', 'title', 'parent', 'contacts__email', 'contacts__city'
        )

        return Response(data=suppliers, status=status.HTTP_200_OK)


class SupplierEditView(APIView):

    def delete(self, request: Request, supplier_id: int):
        """Удалить поставщика"""
        supplier: Supplier = get_object_or_404(Supplier, pk=supplier_id)
        supplier.contacts.delete()
        supplier.delete()
        return Response(data='Успешно удалено', status=status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, supplier_id: int):
        """Редактировать поставщика"""
        supplier = get_object_or_404(Supplier, pk=supplier_id)
        contacts = supplier.contacts
        serializer = CreateSupplierSerializer(supplier, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        supplier_serializer = SupplierSerializer(supplier, data=serializer.validated_data['supplier'], partial=True)
        supplier_serializer.is_valid(raise_exception=True)
        supplier_serializer.save()
        contacts_serializer = ContactsSerializer(contacts, data=serializer.validated_data['contacts'], partial=True)
        contacts_serializer.is_valid(raise_exception=True)
        contacts_serializer.save()

        return Response(data='Успешно отредактировано', status=status.HTTP_200_OK)


class ProductView(APIView):

    def post(self, request: Request):
        """Создать продукт"""
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product(**serializer.validated_data)
        supplier_id = Supplier.objects.filter(title=request.data["supplier_title"]).values('pk')
        product.supplier_id = supplier_id
        product.save()

        response_data = {
            'id': product.pk
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def get(self, request: Request, *args, **kwargs):
        """Получить список всех продуктов поставщика"""
        products = Product.objects.filter(supplier__title=request.data["detail"]).values(
            'title', 'model', 'supplier__title', 'market_launch_date', 'create_date'
        )

        return Response(data=products, status=status.HTTP_200_OK)


class ProductEditView(APIView):

    def delete(self, request: Request, product_id: int):
        """Удалить продукт"""
        product: Product = get_object_or_404(Product, pk=product_id)
        product.delete()
        return Response(data='Успешно удалено', status=status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, product_id: int):
        """Редактировать продукт"""
        product = get_object_or_404(Product, pk=product_id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data='Успешно отредактировано', status=status.HTTP_200_OK)
