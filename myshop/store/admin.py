from django.contrib import admin
from .models import Customer, Products, Category, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('first_name', 'last_name')
    ordering = ('id',)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    search_fields = ('name', 'category__name', 'description')
    list_filter = ('category',)
    ordering = ('id',)
    list_editable = ('price',)
    # prepopulated_fields = {'slug': ('name',)}  # Si un champ 'slug' est utilisé


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'address', 'phone', 'date', 'status')
    search_fields = ('customer__first_name', 'customer__last_name', 'product__name', 'phone', 'address')
    list_filter = ('status', 'date')
    ordering = ('-date',)
    list_editable = ('status',)
