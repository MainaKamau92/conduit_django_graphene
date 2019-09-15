from django.db.models.signals import post_save
from django.dispatch import receiver
from conduit.apps.authentication.models import User
from conduit.apps.profiles.models import Profile


@receiver(signal=post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    email = instance.email
    at_index = email.find("@")
    Profile.objects.create(name=email[:at_index], user=instance)
    post_save.disconnect(create_profile, sender=User)
