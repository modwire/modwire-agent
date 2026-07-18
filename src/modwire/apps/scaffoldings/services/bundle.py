from wireup import injectable

from .scaffolding import ScaffoldingService


@injectable
class ScaffoldingBundleService:
    def __init__(self, scaffoldings: ScaffoldingService):
        self.scaffoldings = scaffoldings

    def get(self, scaffolding_id: str):
        return self.scaffoldings.get(scaffolding_id)
