from DAB import DAB
from getpass import getpass

if __name__ == '__main__':
    email = input("Insert your email: ")
    psw = getpass("Insert your password: ")

    dab = DAB(email, psw)
    print(dab.request_installation_data())
    