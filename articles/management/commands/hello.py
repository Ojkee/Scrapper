from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help: str = "Greats"

    def handle(self, *args, **options):
        _ = args
        _ = options
        print("Hello, World")
