from django.contrib.auth import get_user_model

User = get_user_model()

User.objects.filter(email="superuser@superuser.tst").exists() or \
    User.objects.create_superuser(
        username="superuser",
        email="superuser@superuser.tst", password="very_secure_password")
