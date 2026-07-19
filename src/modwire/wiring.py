from modwire_hex import DjangoApplication

from .languages.wiring import languages
from .plans.wiring import plans
from .records.wiring import records
from .scaffoldings.wiring import scaffoldings
from .tokens.wiring import tokens


application = DjangoApplication(modules=(languages, tokens, scaffoldings, records, plans))
