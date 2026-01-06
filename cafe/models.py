from django.db import models
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Menu Item")
        verbose_name_plural = _("Menu Items")

    def __str__(self):
        return self.name