from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

CustomUser = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not CustomUser.objects.filter(account_id=settings.SUPERUSER_ACCOUNT_ID).exists():
            CustomUser.objects.create_superuser(
                account_id=settings.SUPERUSER_ACCOUNT_ID,
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD
            )
            print("スーパーユーザー作成に成功しました")
