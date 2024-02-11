from base.ConnectionType import ConnectionType

REMOTE_USERNAME = "admin"
REMOTE_PASSWORD = "***REMOVED***"
REMOTE_HOST = "***REMOVED***"

SCHEMA = "DrinkDatabase"

# Will output active transactions being made to the database in console
VERBOSE_OUTPUT = False

# LOCAL_FILE, LOCAL_MEMORY, REMOTE_SERVER
CONNECTION_MODE = ConnectionType.REMOTE_SERVER
