from django.db import models
import datetime
from django.db import models
from django.utils import timezone

class Category(models.Model): 
    name = models.CharField(max_length=50) 
  
    @staticmethod
    def get_all_categories(): 
        return Category.objects.all() 
  
    def __str__(self): 
        return self.name


class Customer(models.Model): 
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50) 
    phone = models.CharField(max_length=10) 
    email = models.EmailField(unique=True)  # Ajout d'unicité
    password = models.CharField(max_length=100) 
  
    def register(self): 
        self.save() 
  
    @staticmethod
    def get_customer_by_email(email): 
        try: 
            return Customer.objects.get(email=email) 
        except Customer.DoesNotExist: 
            return None
  
    def is_exists(self):  # Renommage pour respecter les conventions Python
        return Customer.objects.filter(email=self.email).exists()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Products(models.Model):  # Renommé pour suivre les conventions Django
    SECTION = (
        ('Bazin', 'Bazin'),
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
        ('Enfant', 'Enfant'),
        ('Populaire', 'Populaire'),
    )

    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1) 
    description = models.TextField(default='', blank=True, null=True) 
    image = models.ImageField(upload_to='uploads/products/')
    section = models.CharField(choices=SECTION, max_length=20) 

    @staticmethod
    def get_products_by_id(ids): 
        return Products.objects.filter(id__in=ids) 

    @staticmethod
    def get_all_products(): 
        return Products.objects.all() 

    @staticmethod
    def get_all_products_by_categoryid(category_id): 
        if category_id: 
            return Products.objects.filter(category=category_id) 
        return Products.get_all_products()

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Client
    address = models.CharField(max_length=255, default='', blank=True)  # Adresse de livraison
    phone = models.CharField(max_length=15, default='', blank=True)  # Numéro de téléphone
    date = models.DateTimeField(default=timezone.now)  # Date de la commande
    status = models.BooleanField(default=False)  # Statut de la commande

    def __str__(self):
        return f"Commande {self.id} - {self.customer.first_name} {self.customer.last_name}"

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')

# class Order(models.Model):
#     product = models.ForeignKey(Products, on_delete=models.CASCADE)  # Produit commandé
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Client
#     quantity = models.IntegerField(default=1)  # Quantité commandée
#     price = models.DecimalField(max_digits=10, decimal_places=2)  # Prix unitaire (utiliser DecimalField pour la précision)
#     address = models.CharField(max_length=255, default='', blank=True)  # Adresse de livraison
#     phone = models.CharField(max_length=15, default='', blank=True)  # Numéro de téléphone
#     date = models.DateTimeField(default=timezone.now)  # Date de la commande (utiliser DateTimeField pour plus de flexibilité)
#     status = models.BooleanField(default=False)  # Statut de la commande (ex: False = en attente, True = livrée)

#     def __str__(self):
#         return f"Commande {self.id} - {self.customer.first_name} {self.customer.last_name}"

#     @staticmethod
#     def get_orders_by_customer(customer_id):
#         return Order.objects.filter(customer=customer_id).order_by('-date')

#     @property
#     def total_price(self):
#         return self.quantity * self.price  # Calcul du prix total pour cette commande

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) - {self.total_price} Fcfa"