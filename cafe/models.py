from django.db import models
from django_jalali.db import models as jmodels
from django.utils.translation import gettext_lazy as _

class MenuCategory(models.Model):
    name = models.CharField(_("Category Name"), max_length=100)
    order = models.PositiveIntegerField(_("Display Order"), default=0)

    class Meta:
        verbose_name = _("Menu Category")
        verbose_name_plural = _("Menu Categories")
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(_("Item Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    category = models.ForeignKey(MenuCategory, related_name='items', on_delete=models.CASCADE, verbose_name=_("Category"))
    price = models.DecimalField(_("Price (Toman)"), max_digits=12, decimal_places=0)
    image = models.ImageField(_("Image"), upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(_("Is Available"), default=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Menu Item")
        verbose_name_plural = _("Menu Items")

    def __str__(self):
        return self.name

class CafeOrder(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        PREPARING = 'PREPARING', _('Preparing')
        READY = 'READY', _('Ready to Pickup')
        DELIVERED = 'DELIVERED', _('Delivered')
        CANCELLED = 'CANCELLED', _('Cancelled')

    user = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Customer"))
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.PENDING)
    is_paid = models.BooleanField(_("Is Paid"), default=False)
    settled_at = jmodels.jDateTimeField(_("Settled At"), null=True, blank=True)
    notes = models.TextField(_("Notes/Table Number"), blank=True, help_text=_("e.g. Table 5 or Specific delivery instructions"))
    
    total_price = models.DecimalField(_("Total Price"), max_digits=12, decimal_places=0, default=0)
    
    # Payment Tracking
    payment_token = models.CharField(_("Payment Token"), max_length=100, blank=True, null=True)
    transaction_id = models.CharField(_("Transaction ID"), max_length=100, blank=True, null=True)
    
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Cafe Order")
        verbose_name_plural = _("Cafe Orders")
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.get_status_display()}"

    def update_total_price(self):
        # We use a aggregate for efficiency
        total = self.items.aggregate(
            total=models.Sum(models.F('unit_price') * models.F('quantity'))
        )['total'] or 0
        self.total_price = total
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(CafeOrder, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT, verbose_name=_("Menu Item"))
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    unit_price = models.DecimalField(_("Unit Price"), max_digits=12, decimal_places=0) # Price at the time of order

    def get_subtotal(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.menu_item.price
        super().save(*args, **kwargs)
        self.order.update_total_price()

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"
