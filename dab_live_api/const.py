from typing import Final

BASE_URL: Final[str] = 'https://dconnect.dabpumps.com/'
AUTH: Final[str] = 'auth/token'
INSTALLATION_LIST: Final[str] = 'getInstallationList'
INSTALLATION: Final[str] = 'getInstallation'
DUMSTATE: Final[str] = 'dumstate/'
POWER_SHOWER: Final[str] = '/ccommands/power-shower/'

DEFAULT_HEADER = {
    'host': 'dconnect.dabpumps.com',
    'accept': 'application/json, text/plain, */*',
    'connection': 'keep-alive',
    'user-agent': 'DabAppFreemium/1 CFNetwork/1406.0.4 Darwin/22.4.0',
    'authorization': 'Bearer ',
    'accept-language': 'en-GB,en;q=0.9',
    'accept-encoding': 'gzip, deflate, br'
}