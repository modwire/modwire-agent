from modwire_agent.autowiring import _injectables


def test_discovers_shared_and_app_service_packages() -> None:
    packages = {package.__name__ for package in _injectables}

    assert packages == {
        "modwire_agent.records.services",
        "modwire_agent.projects.services",
        "modwire_agent.scaffoldings.services",
        "modwire_agent.shared",
    }
