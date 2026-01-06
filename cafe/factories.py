import factory
from factory.django import DjangoModelFactory
from cafe.models import MenuCategory, MenuItem

class MenuCategoryFactory(DjangoModelFactory):
    class Meta:
        model = MenuCategory

    name = factory.Sequence(lambda n: f'Category {n}')
    order = factory.Sequence(lambda n: n)

class MenuItemFactory(DjangoModelFactory):
    class Meta:
        model = MenuItem

    category = factory.SubFactory(MenuCategoryFactory)
    name = factory.Sequence(lambda n: f'Item {n}')
    price = factory.Faker('pydecimal', left_digits=5, right_digits=0, positive=True)
    is_available = True
