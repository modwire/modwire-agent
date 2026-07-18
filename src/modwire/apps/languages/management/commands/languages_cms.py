from typing import Annotated

from django.core.management.base import BaseCommand, CommandError
from wireup import Inject
from wireup.integration.django import inject_app

from modwire.shared.languages.base import LanguageVersionError

from ...services.catalog import LanguageCatalogService


class Command(BaseCommand):
    help = "Synchronize the language catalog and current stable versions."

    def add_arguments(self, parser):
        parser.add_argument("--timeout", type=float, default=10, help="Network timeout per language in seconds.")

    @inject_app
    def handle(
        self,
        *args,
        service: Annotated[LanguageCatalogService, Inject()],
        **options,
    ):
        try:
            result = service.sync(timeout=options["timeout"])
        except LanguageVersionError as error:
            raise CommandError(str(error)) from error

        self.stdout.write(
            self.style.SUCCESS(
                f"Synchronized {result.languages} languages, "
                f"{result.package_managers} package managers, {result.commands} package-manager commands, "
                f"{result.tools} tools, and {result.tool_commands} tool commands."
            )
        )
