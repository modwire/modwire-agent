from eventsourcing.system import System

from .application import RecordsApplication
from .projections import RecordsProjection

records_system = System([[RecordsApplication, RecordsProjection]])
