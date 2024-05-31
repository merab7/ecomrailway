from store.models import Product

class Cart():
    def __init__(self, request) -> None:
        self.session = request.session
        #if user exists and session_key exists get this key 
        cart = self.session.get('session_key')

        #if user is new
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart 

    def add(self, product=None, size=int(), quantity=int()):
        product_id = int(product.id)
        name = str(product.name)
        price = int(product.price)
        size = str(size)
        quantity = quantity
        
        # Generate a unique key for the product and size combination
        cart_key = f"{product_id}_{size}"

        # Check if the product and size combination is already in the cart
        if cart_key in self.cart:
           pass
        else:
            # If it doesn't exist, add it to the cart
            self.cart[cart_key] = {'id': int(product_id), 'name': name, 'price': price, 'size': size, 'quantity': quantity}

        self.session.modified = True

    def update(self, cart_key=None, product=None, size=int(), quantity=int()):
        product_id = int(product.id)
        name = str(product.name)
        price = int(product.price)
        size = str(size)
        quantity = quantity
        cart_key = cart_key
        new_cart_key = f"{product_id}_{size}"
        
        #delete existing item
        self.cart.pop(cart_key)
        #adding_new 
        self.cart[new_cart_key] = {'id': int(product_id), 'name': name, 'price': price, 'size': size, 'quantity': quantity}
        self.session.modified = True

    def delete(self, cart_key=None):
        cart_key=cart_key

        #delete selected item from the cart
        self.cart.pop(cart_key)

        self.session.modified = True




    def __len__(self):
        return len(self.cart)

    def get_products(self):
        # Extract product IDs from the keys in the cart
        product_ids = [key.split('_')[0] for key in self.cart.keys()]
        
        # Retrieve products from the database based on the extracted product IDs
        products = Product.objects.filter(id__in=product_ids)
    
        return products

    def get_quantities(self):
        quantities = self.cart
        return quantities        