from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

NULLABLE = {'blank': True, 'null': True}


class Contacts(models.Model):

    email = models.EmailField(unique=True, verbose_name='email')
    country = models.CharField(max_length=300, verbose_name='страна')
    city = models.CharField(max_length=200, verbose_name='город')
    street = models.CharField(max_length=250, verbose_name='улица')
    house_number = models.PositiveIntegerField(verbose_name='номер дома')

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f'{self.email} - {self.city}'

    def __repr__(self):
        return f'{self.email} - {self.city}'


class Supplier(MPTTModel):

    class SUPPLIER(models.TextChoices):
        FACTORY = ('завод', 'завод')
        RETAILER = ('розничная сеть', 'розничная сеть')
        SOLE_PROPRIETOR = ('индивидуальный предприниматель', 'индивидуальный предприниматель')

    parent = TreeForeignKey('self', on_delete=models.PROTECT, related_name='заказчик', db_index=True,
                            verbose_name='поставщик', **NULLABLE)
    supplier_type = models.CharField(max_length=50, choices=SUPPLIER.choices, verbose_name='поставщик')
    title = models.CharField(max_length=300, verbose_name='название')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')
    contacts = models.OneToOneField(Contacts, on_delete=models.CASCADE, verbose_name='контакты', related_name='supplier')

    class MPTTMeta:
        order_insertion_by = ['supplier_type']

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return f'{self.title} - {self.contacts}'

    def __repr__(self):
        return f'{self.title} - {self.contacts}'


class Product(models.Model):

    title = models.CharField(max_length=300, verbose_name='название')
    model = models.CharField(max_length=100, verbose_name='модель')
    market_launch_date = models.DateField(verbose_name='дата выхода на рынок')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='поставщик', related_name='products')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.title} {self.model} - {self.supplier}'

    def __repr__(self):
        return f'{self.title} {self.model} - {self.supplier}'


class Debt(models.Model):

    debtor = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='должник', related_name='creditors')
    creditor = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='кредитор', related_name='debtors')
    value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='долг', **NULLABLE)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')

    class Meta:
        verbose_name = 'Задолженность'
        verbose_name_plural = 'Задолженности'

    def __str__(self):
        return f'{self.debtor.title} - {self.creditor.title} - сумма: {self.value}'

    def __repr__(self):
        return f'{self.debtor} - {self.creditor} - сумма: {self.value}'
