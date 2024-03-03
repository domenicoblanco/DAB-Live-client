from DAB import DAB
from getpass import getpass

if __name__ == '__main__':
    email = input("Insert your email: ")
    psw = getpass("Insert your password: ")

    dab = DAB(email, psw)
    installation_data = dab.discover_installations()
    print(installation_data)
    print(dab.enable_power_shower(installation_data[0]['pumps'][0]))
    