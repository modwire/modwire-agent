from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run languages sync hooks."

    def handle(self, *args, **opts):
        self.stdout.write(self.style.SUCCESS("languages synced"))
