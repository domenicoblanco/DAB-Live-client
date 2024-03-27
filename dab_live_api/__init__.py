import aiohttp
from json import dumps, loads, JSONDecodeError
from asyncio import get_event_loop, create_task, new_event_loop
from datetime import datetime
from .const import *
import logging

class DAB():
    def __init__(self, email: str, psw: str, session: aiohttp.ClientSession|None = None, should_save_token: bool = True) -> None:
        self.token = None
        self.email = None
        self.psw = None
        self.save_token = should_save_token
        self.session = session
        self.should_close_session = session is None
        self.set_credentials(email, psw)
        self.__check_token__()


    def __del__(self) -> None:
        if self.session and self.should_close_session:
            try:
                loop = get_event_loop()
                create_task(self.session.close())
            except RuntimeError:
                loop = new_event_loop()
                loop.run_until_complete(self.session.close())


    def set_credentials(self, email: str|None = None, psw: str|None = None) -> None:
        self.email = email
        self.psw = psw


    def __check_token__(self) -> None:
        if self.save_token:
            with open('.dab_token', 'w+') as saved_data:
                try:
                    token_data = loads(saved_data)
                    if 'expire' in token_data and datetime.now() < token_data['expire']:
                        logging.info('Using stored token')
                        self.token = token_data['token']
                        return
                except (JSONDecodeError, TypeError) as e:
                    logging.error('__check_token__', e)
                    return


    async def __authenticate__(self) -> bool:
        if self.email is None or self.psw is None:
            logging.warning('Credentials not set!')
            return False

        if self.session is None:
            self.session = aiohttp.ClientSession(headers=const.DEFAULT_HEADER)

        auth_payload = {
            'email': self.email,
            'password': self.psw
        }

        async with self.session.post(f'{const.BASE_URL}{const.AUTH}', json=auth_payload) as auth_response:
            current_time = datetime.now().timestamp()

            try:
                auth_response = await auth_response.json()
            except Exception as e:
                logging.error('Something went wrong during authentication', e)
                return False

            if 'code' in auth_response:
                logging.warning(auth_response['code'], auth_response['msg'])
                return False
            else:
                logging.info('Login succeeded')
                self.token = auth_response['access_token']

                if self.save_token:
                    with open('.dab_token', 'w') as save_data:
                        save_data.write(dumps({
                            'token': self.token,
                            'expire': current_time + float(auth_response['expires_in'])
                        }))

                return True    


    async def discover_installation_by_id(self, id: str, name: str) -> list[str]:
        installation_pumps = []
        header = const.DEFAULT_HEADER.copy()
        header['authorization'] += self.token

        async with self.session.get(f'{const.BASE_URL}{const.INSTALLATION}/{id}', headers=header) as installation_response:
            installation_data = await installation_response.json()

            if installation_data['res'] != 'OK':
                logging.warning(f'Something went wrong with installation {name} ({id}) ', installation_data)

            dum_list = loads(installation_data['data'])['dumlist']
            for dum in dum_list:
                installation_pumps.append(dum['serial'])
    
        return installation_pumps


    async def discover_installations(self) -> list[dict[str, any]]:
        if self.token is None and not await self.__authenticate__():
            return []

        installations = []
        request_header = const.DEFAULT_HEADER.copy()
        request_header['authorization'] += self.token

        async with self.session.get(f'{const.BASE_URL}{const.INSTALLATION_LIST}', headers=request_header) as discovery_response:
            discovery_res = await discovery_response.json()

            if discovery_res['res'] != 'OK':
                logging.warning('Something went wrong during discovery: ', discovery_res)
                return []

            for installation in discovery_res['rows']:
                pumps_data = {}

                for pump_id in await self.discover_installation_by_id(installation['installation_id'], installation['name']):
                    pumps_data[pump_id] = await self.request_pump_data(pump_id)

                installation_details = {
                    'id': installation['installation_id'],
                    'name': installation['name'],
                    'description': installation['description'],
                    'company': installation['company'] if type(installation['company']) == str else ', '.join(installation['company']),
                    'status': installation['status'],
                    'pumps': pumps_data
                }

                installations.insert(0, installation_details)

        return installations


    async def request_pump_data(self, pump_serial: str|None = None) -> list[dict[str, any]]:
        header = const.DEFAULT_HEADER.copy()
        header['authorization'] += self.token

        async with self.session.get(f'{const.BASE_URL}{const.DUMSTATE}{pump_serial}', headers=header) as pump_data_response:
            pump_data = await pump_data_response.json()

            if pump_data['res'] == 'ERROR':
                logging.error(f'{pump_data['code']}: {pump_data['msg']}')

        return loads(pump_data['status'])


    async def request_installation_data(self, installation_id: str|None = None) -> list[dict[str,any]]:
        pumps = []
        pumps_data = []

        if installation_id is None:
            installations = await self.discover_installations()

            for installation in installations:
                if 'pumps' in installation:
                    pumps += installation['pumps']
        else:
            pumps = await self.discover_installation_by_id(installation_id, 'provided')
        
        for pump_id in pumps:
            pumps_data.insert(0, await self.request_pump_data(pump_id))

        return pumps_data


    async def handle_power_shower(self, pump_id: str, op: str) -> bool:
        endpoint = f'{const.BASE_URL}dum/{pump_id}{const.POWER_SHOWER}{op}'
        
        request_header = const.DEFAULT_HEADER.copy()
        request_header['authorization'] += self.token

        async with self.session.post(endpoint, headers=request_header) as power_shower_response:
            power_shower_res = await power_shower_response.json()

        if power_shower_res.get('res') == 'OK':
            return True
        else:
            logging.error(f'There was an error while setting power shower {op}\n{power_shower_res['code']}: {power_shower_res['msg']}')
            return False

