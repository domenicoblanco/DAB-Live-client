from dab_live_api import DAB
from getpass import getpass
from asyncio import run

async def main() -> None:
    email = input("Insert your email: ")
    psw = getpass("Insert your password: ")

    # The auth will be handled automatically
    dab = DAB(email, psw)

    # Obtains your installation(s) data, there could be multiple installations with many pumps
    installation_data = await dab.discover_installations()
    print(installation_data)

    # Asks for the firsts pump in your first installation
    print(await dab.request_pump_data(installation_data[0]['pumps'][0]))

    # Handles power shower activation
    # Tested on Esybox Mini 2, could be different with other devices
    if input('Would you like to enable Power Shower? (Y/N):') == 'Y':
        dab.handle_power_shower(installation_data[0]['pumps'][0], 'ON')

        if input('Would you like to disable Power Shower? (Y/N):') == 'Y':
            dab.handle_power_shower(installation_data[0]['pumps'][0], 'OFF')


if __name__ == '__main__':
    run(main())