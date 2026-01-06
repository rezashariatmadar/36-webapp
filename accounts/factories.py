import factory
from factory.django import DjangoModelFactory
from accounts.models import CustomUser

class UserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    phone_number = factory.Sequence(lambda n: f'0912345{n:03d}0')
    # 1234567891 is valid. Let's use a pattern that produces valid ones.
    # Sum for 123456789 = 210. 210 % 11 = 1. check = 1.
    # To keep it simple, I'll just use a fixed valid one for now, or a few.
    national_id = factory.Iterator(['1234567891', '0010532412', '0047247736'])
    full_name = factory.Faker('name')
    is_active = True
    is_staff = False
    password = 'password123'

    @factory.post_generation
    def set_password(self, create, extracted, **kwargs):
        password = extracted or 'password123'
        self.set_password(password)
        if create:
            self.save()
