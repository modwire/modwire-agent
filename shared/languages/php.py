import json
from urllib.request import Request

from wireup import injectable

from .base import LanguageDefinition, PackageManagerDefinition, ToolDefinition


@injectable(as_type=LanguageDefinition, qualifier="php")
class PHP(LanguageDefinition):
    name = "PHP"
    executable = "php"
    source_extensions = (".php",)
    package_managers = (
        PackageManagerDefinition(
            name="Composer",
            executable="composer",
            manifest_paths=("composer.json",),
            lockfile_paths=("composer.lock",),
            registry_url="https://repo.packagist.org",
            package_url_type="composer",
            version_constraint="composer",
            supports_workspaces=False,
            commit_lockfiles=True,
            commands={
                "init": "composer init",
                "install": "composer install",
                "add_runtime": "composer require {package}",
                "add_development": "composer require --dev {package}",
                "remove": "composer remove {package}",
                "update": "composer update",
                "lock": "composer update --lock",
                "run": "composer run {command}",
                "audit": "composer audit",
            },
        ),
    )
    tools = (
        ToolDefinition(
            "PHP-CS-Fixer",
            ("formatter",),
            "php-cs-fixer",
            "friendsofphp/php-cs-fixer",
            "https://cs.symfony.com/",
            (".php-cs-fixer.php",),
            True,
            {"check": "php-cs-fixer fix --dry-run --diff", "fix": "php-cs-fixer fix"},
        ),
        ToolDefinition(
            "PHPStan",
            ("type_checker",),
            "phpstan",
            "phpstan/phpstan",
            "https://phpstan.org/",
            ("phpstan.neon",),
            True,
            {"check": "phpstan analyse"},
        ),
        ToolDefinition(
            "PHPUnit",
            ("test_runner",),
            "phpunit",
            "phpunit/phpunit",
            "https://phpunit.de/",
            ("phpunit.xml",),
            True,
            {"test": "phpunit"},
        ),
        ToolDefinition(
            "Xdebug",
            ("coverage",),
            "php",
            "ext-xdebug",
            "https://xdebug.org/",
            ("phpunit.xml",),
            False,
            {"coverage": "XDEBUG_MODE=coverage phpunit --coverage-text"},
        ),
        ToolDefinition(
            "Composer Audit",
            ("security",),
            "composer",
            "composer",
            "https://getcomposer.org/doc/03-cli.md#audit",
            (),
            True,
            {"audit": "composer audit"},
        ),
    )

    @property
    def version_request(self) -> Request:
        return Request(
            "https://endoflife.date/api/php.json",
            headers={"Accept": "application/json", "User-Agent": "modwire-languages-cms/1.0"},
        )

    def on_version_response(self, response) -> str:
        return json.load(response)[0]["latest"]
