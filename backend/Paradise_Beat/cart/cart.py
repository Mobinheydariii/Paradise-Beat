from django.conf import settings
from beats.models import Beat




class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty dictionary in the session so that it will exist for this user's session.
            cart = self.session[settings.CART_SESSION_ID] = {}
            # save an empty cart in the session
        self.cart = cart


    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True
    

    def add(self, beat, licence, price):
        """
        Add a beat with licence to the cart or update the licence type.
        """
        beat_id = str(beat['id'])
        if beat_id not in self.cart:
            self.cart[beat_id] = {
                'beat' : beat,
                'licence' : licence,
                'price' : price
            }
        # else:
            # self.cart[beat_id][licence] = licence
            # self.cart[beat_id][price] = price
            # print(self.cart[beat_id][licence])
        self.save()


    def remove(self, beat):
        try:
            del self.cart[str(beat.id)]
            self.save()
        except KeyError:
            pass
    

    def __iter__(self):
        """
        Iterate over the items in the cart and get the beats 
        and licence from the database.
        """
        beats_ids = self.cart.keys()
        beats = Beat.objects.filter(id__in=beats_ids)
        cart = self.cart.copy()
        for beat in beats:
            cart[str(beat.id)]['beat'] = beat
        for item in cart.values():
            item['price'] = int(item['price'])
            yield item
    

    def total_cost(self):
        return sum(int(item['price']) for item in self.cart.values())
    

    def __len__(self):
        return sum(item for item in self.cart.values())
    

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
        
