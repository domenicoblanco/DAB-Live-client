from requests import Session
from json import load, loads, dump, dumps, JSONDecodeError
from datetime import datetime

import const
import logging

class DAB():
    def __init__(self, email: str, psw: str, should_save_token: bool = True) -> None:
        self.token = None
        self.email = None
        self.psw = None
        self.save_token = should_save_token
        self.session = Session()
        self.set_credentials(email, psw)
        self.__check_token()
    

    def __del__(self) -> None:
        self.session.close()


    def set_credentials(self, email: str|None = None, psw: str|None = None) -> None:
        self.email = email
        self.psw = psw

    
    def __check_token(self) -> None:
        if self.save_token:
            with open('.dab_token', 'w+') as j:
                try:
                    token_data = load(j)

                    if 'expire' in token_data and datetime.now() < token_data['expire']:
                        logging.warning('Using stored token')
                        self.token = token_data['token']
                except JSONDecodeError:
                    return


    def __authenticate(self) -> bool:
        if self.email is None or self.psw is None:
            logging.warning("Credentials not set!")
            return False

        auth_header = {
            'host': 'dconnect.dabpumps.com',
            'content-type': 'application/json',
            'connection': 'keep-alive',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'DabAppFreemium/1 CFNetwork/1406.0.4 Darwin/22.4.0',
            'content-length': '48',
            'accept-language': 'en-GB,en;q=0.9',
            'accept-encoding': 'gzip, deflate, br'
        }

        auth_payload = dumps({
            "email": self.email,
            "password": self.psw
        })

        auth_response = self.session.post(f'{const.BASE_URL}{const.AUTH}', headers=auth_header, data=auth_payload)
        current_time = datetime.now().timestamp()

        try:
            auth_response = auth_response.json()
        except Exception as e:
            logging.error('Something went wrong during authentication', e)
        
        if 'code' in auth_response:
            logging.warning(auth_response['code'], auth_response['msg'])
            return False
        else:
            logging.info('Login succeeded')
            self.token = auth_response['access_token']

            if self.save_token:
                with open('.dab_token', 'w') as j:
                    dump({
                        'token': self.token,
                        'expire': current_time + float(auth_response['expires_in'])
                    }, j)

            return True    
    

    def discover_installation_by_id(self, id: str, name: str) -> list[str]:
        installation_pumps = []
        header = const.DEFAULT_HEADER.copy()
        header['authorization'] += self.token

        installation_data = self.session.get(f'{const.BASE_URL}{const.INSTALLATION}/{id}', headers=header).json()

        if installation_data['res'] != 'OK':
            logging.warning(f'Something went wrong with installation {name} ({id}) ', installation_data)
        
        dum_list = loads(installation_data['data'])['dumlist']
        for dum in dum_list:
            installation_pumps.append(dum['serial'])
    
        return installation_pumps


    def discover_installations(self) -> list[dict[str, any]]:
        if self.token is None and not self.__authenticate():
            return []

        installations = []
        request_header = const.DEFAULT_HEADER.copy()
        request_header['authorization'] += self.token

        discovery_res = self.session.get(f'{const.BASE_URL}{const.INSTALLATION_LIST}', headers=request_header).json()

        if discovery_res['res'] != 'OK':
            logging.warning('Something went wrong: ', discovery_res)
            return []
        
        for installation in discovery_res['rows']:
            installation_details = {
                'id': installation['installation_id'],
                'name': installation['name'],
                'description': installation['description'],
                'company': installation['company'],
                'status': installation['status'],
                'pumps': self.discover_installation_by_id(installation['installation_id'], installation['name'])
            }
            
            installations.insert(0, installation_details)

        return installations
    

    def request_pump_data(self, pump_serial: str|None = None) -> list[dict[str, any]]:
        header = const.DEFAULT_HEADER.copy()
        header['authorization'] += self.token

        pump_data = self.session.get(f'{const.BASE_URL}{const.DUMSTATE}{pump_serial}', headers=header).json()

        if pump_data['res'] == 'ERROR':
            logging.error(f'{pump_data["code"]}: {pump_data["msg"]}')

        return loads(pump_data['status'])
    

    def request_installation_data(self, installation_id: str|None = None) -> list[dict[str,any]]:
        pumps = []
        pumps_data = []
        if installation_id is None:
            installations = self.discover_installations()

            for installation in installations:
                if 'pumps' in installation:
                    pumps += installation['pumps']
        else:
            pumps = self.discover_installation_by_id(installation_id, 'provided')
        
        for pump_id in pumps:
            pumps_data.append(self.request_pump_data(pump_id))
        
        return pumps_data
    
    def enable_power_shower(self, pump_id: str) -> bool:
        endpoint = f'{const.BASE_URL}dum/{pump_id}{const.ENABLE_POWER_SHOWER}'
        
        request_header = const.DEFAULT_HEADER.copy()
        request_header['authorization'] += self.token

        power_shower_res = self.session.post(endpoint, headers=request_header).json()

        if 'res' in power_shower_res and power_shower_res['res'] == 'OK':
            return True
        else:
            logging.error(f'There was an error while enabling power shower\n{power_shower_res["code"]}: {power_shower_res["msg"]}')
            return False