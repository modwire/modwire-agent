from django.core.management.base import BaseCommand
from django.db import connection, transaction


class Command(BaseCommand):
    help = "Prepare deployed scaffoldings data for shared.languages."

    table_name = "scaffoldings_scaffolding"
    column_name = "language_id"
    target_max_length = 64
    lock_timeout = "5s"

    def handle(self, *args, **options):
        if connection.vendor != "postgresql":
            self.stdout.write(self.style.WARNING("release_shared_languages only targets PostgreSQL; no changes made."))
            return

        with connection.cursor() as cursor:
            if self.table_name not in connection.introspection.table_names(cursor):
                self.stdout.write(self.style.WARNING(f"{self.table_name} does not exist; no changes made."))
                return
            if self.column_name not in self._column_names(cursor):
                self.stdout.write(
                    self.style.WARNING(f"{self.table_name}.{self.column_name} does not exist; no changes made.")
                )
                return

            foreign_keys = self._foreign_keys(cursor)
            max_length, is_nullable = self._column_state(cursor)
            row_count, null_count = self._row_counts(cursor)
            self.stdout.write(f"Found {row_count} scaffoldings, {null_count} with null language_id.")
            if null_count:
                self.stderr.write(self.style.ERROR("Aborting: scaffoldings with null language_id must be fixed first."))
                return

            with transaction.atomic():
                cursor.execute("SET LOCAL lock_timeout = %s", [self.lock_timeout])
                for name in foreign_keys:
                    cursor.execute(
                        f"ALTER TABLE {self._quote(self.table_name)} DROP CONSTRAINT {self._quote(name)}"
                    )
                    self.stdout.write(f"Dropped foreign key constraint {name}.")

                if max_length is not None and max_length < self.target_max_length:
                    cursor.execute(
                        f"ALTER TABLE {self._quote(self.table_name)} "
                        f"ALTER COLUMN {self._quote(self.column_name)} TYPE varchar({self.target_max_length})"
                    )
                    self.stdout.write(
                        f"Changed {self.table_name}.{self.column_name} to varchar({self.target_max_length})."
                    )

                if is_nullable:
                    cursor.execute(
                        f"ALTER TABLE {self._quote(self.table_name)} "
                        f"ALTER COLUMN {self._quote(self.column_name)} SET NOT NULL"
                    )
                    self.stdout.write(f"Set {self.table_name}.{self.column_name} NOT NULL.")

        self.stdout.write(self.style.SUCCESS("shared.languages release preparation complete."))

    def _column_names(self, cursor) -> set[str]:
        return {column.name for column in connection.introspection.get_table_description(cursor, self.table_name)}

    def _foreign_keys(self, cursor) -> list[str]:
        constraints = connection.introspection.get_constraints(cursor, self.table_name)
        return [
            name
            for name, details in constraints.items()
            if details.get("foreign_key") and details.get("columns") == [self.column_name]
        ]

    def _column_state(self, cursor) -> tuple[int | None, bool]:
        cursor.execute(
            """
            SELECT character_maximum_length, is_nullable
            FROM information_schema.columns
            WHERE table_schema = current_schema()
              AND table_name = %s
              AND column_name = %s
            """,
            [self.table_name, self.column_name],
        )
        max_length, is_nullable = cursor.fetchone()
        return max_length, is_nullable == "YES"

    def _row_counts(self, cursor) -> tuple[int, int]:
        cursor.execute(
            f"""
            SELECT COUNT(*), COUNT(*) FILTER (WHERE {self._quote(self.column_name)} IS NULL)
            FROM {self._quote(self.table_name)}
            """
        )
        row_count, null_count = cursor.fetchone()
        return row_count, null_count

    @staticmethod
    def _quote(identifier: str) -> str:
        return connection.ops.quote_name(identifier)
