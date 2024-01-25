from common_volatile_database import CommonVolatileDatabase
from key_value_database import KeyValueDatabase

class KeyValueVolatileDatabase(CommonVolatileDatabase, KeyValueDatabase):
    pass
