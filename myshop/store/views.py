from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from store.models import Customer, Products, Category, Order,OrderItem
from django.core.paginator import Paginator

from django.shortcuts import render
from django.http import JsonResponse
from .models import Products
from django.shortcuts import render, get_object_or_404
from .models import Products



# Classe Index : Gestion de la page d'accueil et du panier
class Index(View):
    def post(self, request):
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity', 1))  # Quantité ajoutée au panier
        remove = request.POST.get('remove')
        cart = request.session.get('cart', {})

        if product_id:
            if remove:
                if product_id in cart:
                    if cart[product_id] > 1:
                        cart[product_id] -= 1
                    else:
                        del cart[product_id]
            else:
                cart[product_id] = cart.get(product_id, 0) + quantity

        request.session['cart'] = cart
        return redirect('homepage')

    def get(self, request):
        # Récupérer le client à partir de la session
        customer_id = request.session.get('customer')
        customer = Customer.objects.get(id=customer_id) if customer_id else None

        # Ajouter le client au contexte
        context = {
            'customer': customer,
        }
        # return render(request, 'store/index.html', context)
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')
# Fonction store : Affiche les produits et catégories
def store(request):
    cart = request.session.get('cart', {})
    request.session['cart'] = cart  # Initialise un panier vide si inexistant

    # Récupérer le client à partir de la session
    customer_id = request.session.get('customer')
    customer = Customer.objects.get(id=customer_id) if customer_id else None

    categories = Category.get_all_categories()  # Récupère toutes les catégories
    category_id = request.GET.get('category')  # Récupère l'ID de la catégorie dans l'URL
    products = Products.get_all_products_by_categoryid(category_id) if category_id else Products.get_all_products()  # Récupère les produits filtrés par catégorie

    # Sections personnalisées : Bazin, Homme, Femme, Enfant, Populaire
    sections = ['Bazin', 'Homme', 'Femme', 'Enfant', 'Populaire']
    
    # On récupère les produits pour chaque section
    data = {section.lower(): Products.objects.filter(section=section).order_by('-id')[:4] for section in sections}

    # Ajoute les données des catégories et produits à envoyer au template
    data.update({
        'products': products,
        'categories': categories,
        'customer': customer,  # Ajouter le client au contexte
    })
    
    # Passe le nombre d'étoiles pour chaque produit (exemple avec 5 étoiles pour chaque)
    data['stars'] = [1, 2, 3, 4, 5]  # Vous pouvez ajuster cela selon le rating réel du produit

    return render(request, 'store/index.html', data)

def all_product(request):
    cart = request.session.get('cart', {})
    request.session['cart'] = cart  # Initialise un panier vide si inexistant

    categories = Category.get_all_categories()  # Récupère toutes les catégories
    category_id = request.GET.get('category')  # Récupère l'ID de la catégorie dans l'URL
    products = Products.get_all_products_by_categoryid(category_id) if category_id else Products.get_all_products()  # Récupère les produits filtrés par catégorie

    # Pagination
    paginator = Paginator(products, 12)  # 10 produits par page
    page_number = request.GET.get('page')  # Numéro de la page dans l'URL
    page_obj = paginator.get_page(page_number)

    # Ajoute les données des catégories, produits, et pagination au template
    data = {
        'products': page_obj,  # Les produits de la page actuelle
        'categories': categories,
        'stars': [1, 2, 3, 4, 5],  # Exemple de rating
    }

    return render(request, 'store/products.html', data)

def bazin(request):
    cart = request.session.get('cart', {})
    request.session['cart'] = cart  # Initialise un panier vide si inexistant

    categories = Category.get_all_categories()  # Récupère toutes les catégories
    category_id = request.GET.get('category')  # Récupère l'ID de la catégorie dans l'URL
    
    # Récupère tous les produits Bazin
    bazins = Products.objects.filter(section='Bazin').order_by('-id')

    # Pagination
    paginator = Paginator(bazins, 6)  
    page_number = request.GET.get('page')  # Numéro de la page dans l'URL
    page_obj = paginator.get_page(page_number)

    # Ajoute les données des catégories, produits, et pagination au template
    data = {
        'bazins': page_obj,  # Les produits de la page actuelle
        'categories': categories,
    }

    return render(request, 'store/bazins.html', data)


def homme(request):
    cart = request.session.get('cart', {})
    request.session['cart'] = cart  # Initialise un panier vide si inexistant

    categories = Category.get_all_categories()  # Récupère toutes les catégories
    category_id = request.GET.get('category')  # Récupère l'ID de la catégorie dans l'URL
    
    # Récupère tous les produits pour hommes
    hommes = Products.objects.filter(section='Homme').order_by('-id')

    # Pagination
    paginator = Paginator(hommes, 6)  
    page_number = request.GET.get('page')  # Numéro de la page dans l'URL
    page_obj = paginator.get_page(page_number)

    # Ajoute les données des catégories, produits, et pagination au template
    data = {
        'hommes': page_obj,  # Les produits de la page actuelle
        'categories': categories,
    }

    return render(request, 'store/homme.html', data)

def femme(request):
    cart = request.session.get('cart', {})
    request.session['cart'] = cart  # Initialise un panier vide si inexistant

    categories = Category.get_all_categories()  # Récupère toutes les catégories
    category_id = request.GET.get('category')  # Récupère l'ID de la catégorie dans l'URL
    
    # Récupère tous les produits pour femmes
    femmes = Products.objects.filter(section='Femme').order_by('-id')

    # Pagination
    paginator = Paginator(femmes, 6)  
    page_number = request.GET.get('page')  # Numéro de la page dans l'URL
    page_obj = paginator.get_page(page_number)

    # Ajoute les données des catégories, produits, et pagination au template
    data = {
        'femmes': page_obj,  # Les produits de la page actuelle
        'categories': categories,
    }

    return render(request, 'store/femme.html', data)

def enfant(request):
    cart = request.session.get('cart', {})
    request.session['cart'] = cart  # Initialise un panier vide si inexistant

    categories = Category.get_all_categories()  # Récupère toutes les catégories
    category_id = request.GET.get('category')  # Récupère l'ID de la catégorie dans l'URL
    
    # Récupère tous les produits pour enfants
    enfants = Products.objects.filter(section='Enfant').order_by('-id')

    # Pagination
    paginator = Paginator(enfants, 6)  
    page_number = request.GET.get('page')  # Numéro de la page dans l'URL
    page_obj = paginator.get_page(page_number)

    # Ajoute les données des catégories, produits, et pagination au template
    data = {
        'enfants': page_obj,  # Les produits de la page actuelle
        'categories': categories,
    }

    return render(request, 'store/enfant.html', data)

# Fonction utilitaire pour calculer le total du panier
def get_cart_total(cart):
    total = 0
    for product_id, quantity in cart.items():
        try:
            product = Products.objects.get(id=int(product_id))
            total += product.price * quantity
        except Products.DoesNotExist:
            continue  # Ignore les produits inexistants
    return total

# Vue pour afficher le détail d'un produit
def detail(request, my_id):
    cart = request.session.get('cart', {})

    try:
        product = Products.objects.get(id=my_id)
    except Products.DoesNotExist:
        return render(request, 'store/404.html', status=404)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                # Supprimer l'article si la quantité est inférieure à 1
                cart.pop(str(product.id), None)
            else:
                cart[str(product.id)] = quantity
        except ValueError:
            return JsonResponse({'error': 'Quantité invalide.'}, status=400)

        request.session['cart'] = cart

        # Calculer le total du panier
        cart_total = get_cart_total(cart)

        # Réponse JSON pour AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'quantity': cart.get(str(product.id), 0),
                'cart_total': cart_total,
            })

    cart_total = get_cart_total(cart)

    data = {
        'product': product,
        'cart_total': cart_total,
        'cart': cart,
    }
    return render(request, 'store/detail.html', data)



# Classe Login : Gestion de la connexion utilisateur
class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'store/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        customer = Customer.objects.filter(email=email).first()
        error_message = None

        if customer and check_password(password, customer.password):
            request.session['customer'] = customer.id  # Stocker l'ID du client dans la session
            return HttpResponseRedirect(Login.return_url or '/')
        else:
            error_message = "Email ou mot de passe invalide !!"

        return render(request, 'store/login.html', {'error': error_message})

# Fonction logout : Déconnexion utilisateur
def logout(request):
    request.session.clear()
    return redirect('login')


# Classe Signup : Inscription utilisateur
class Signup(View):
    def get(self, request):
        return render(request, 'store/signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        customer = Customer(
            first_name=first_name, last_name=last_name, phone=phone, email=email, password=password
        )
        error_message = self.validate_customer(customer)

        if not error_message:
            customer.password = make_password(password)
            customer.save()
            return redirect('login')

        return render(request, 'store/signup.html', {
            'error': error_message,
            'values': postData,
        })

    def validate_customer(self, customer):
        if not customer.first_name or len(customer.first_name) < 3:
            return "Le prénom doit comporter au moins 3 caractères"
        if not customer.last_name or len(customer.last_name) < 3:
            return "Le nom doit comporter au moins 3 caractères"
        if not customer.phone or len(customer.phone) < 10:
            return "Le numéro de téléphone doit comporter au moins 10 chiffres"
        if not customer.email or len(customer.email) < 5:
            return "L'email doit comporter au moins 5 caractères"
        if Customer.objects.filter(email=customer.email).exists():
            return "Adresse email déjà enregistrée."
        return None


class CheckOut(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        products = Products.objects.filter(id__in=cart.keys())
        cart_items = [
            {
                'product': product,
                'quantity': cart.get(str(product.id), 0),
                'total_price': product.price * cart.get(str(product.id), 0),
            }
            for product in products
        ]
        cart_total = sum(item['total_price'] for item in cart_items)
        return render(request, 'store/checkout.html', {
            'cart': cart_items,
            'cart_total': cart_total,
        })

    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer_id = request.session.get('customer')

        # Vérifier si le client est connecté
        if not customer_id:
            return redirect('login')

        cart = request.session.get('cart', {})
        products = Products.objects.filter(id__in=cart.keys())

        # Créer une nouvelle commande
        order = Order.objects.create(
            customer_id=customer_id,
            address=address,
            phone=phone,
        )

        # Ajouter les produits à la commande
        for product in products:
            quantity = cart.get(str(product.id), 0)
            if quantity > 0:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=quantity,
                )

        # Vider le panier
        request.session['cart'] = {}
        return redirect('success')
        # Rediriger vers la page de confirmation
        # return redirect('order_confirmation')




# Classe OrderView : Historique des commandes
class OrderView(View):
    def get(self, request):
        customer_id = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer_id)
        return render(request, 'store/orders.html', {'orders': orders})



class OrderConfirmation(View):
    def get(self, request):
        customer_id = request.session.get('customer')
        if not customer_id:
            return redirect('login')  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté

        # Récupérer la dernière commande de l'utilisateur
        orders = Order.objects.filter(customer_id=customer_id).order_by('-date')[:1]

        if orders:
            order = orders[0]
            order_items = order.order_items.all()  # Récupérer les articles associés à la commande
            total_price = sum(item.total_price for item in order_items)
        else:
            order = None
            order_items = []
            total_price = 0

        context = {
            'order': order,
            'order_items': order_items,
            'total_price': total_price,
        }
        return render(request, 'store/order_confirmation.html', context)

class SuccessView(View):
    def get(self, request):
        return render(request, 'store/success.html')
# Fonction about : Page à propos
def about(request):
    return render(request, "store/about.html")


# Fonction contact : Page de contact
def contact(request):
    return render(request, "store/contact.html")


# 2624003096773d13d097be4.45956912/API_KEY
# 105884700/SITE_ID
# 14742853296773da219d1c10.10571516/Secret Key