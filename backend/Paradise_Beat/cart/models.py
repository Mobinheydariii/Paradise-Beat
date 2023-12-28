from django.db import models
from account.models import User
from beats.models import Beat, BeatLicence



class Cart(models.Model):
    user = models.ForeignKey(
        User,
        related_name='carts',
        on_delete=models.CASCADE
    )
    total_price = models.BigIntegerField()

    def __str__(self):
        return f'This user: {self.user.username} has cart value:{self.total_price}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    licence = models.ForeignKey(BeatLicence, on_delete=models.CASCADE)
    price = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.beat.title}-{self.licence.price}"