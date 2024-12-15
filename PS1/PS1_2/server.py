from pyftpdlib.authorizers import DummyAuthorizer # type: ignore
from pyftpdlib.handlers import FTPHandler # type: ignore
from pyftpdlib.servers import FTPServer # type: ignore
FTP_PORT = 8087
FTP_USER = "user"
FTP_PASSWORD = "pwd"
FTP_DIRECTORY = "/home/cslinux/Desktop/PS1"


def main():
   authorizer = DummyAuthorizer()
   authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmw')
   handler = FTPHandler
   handler.authorizer = authorizer
   handler.banner = "pyftpdlib based ftpd ready."
   address = ('10.1.66.240', FTP_PORT)
   server = FTPServer(address, handler)
   server.max_cons = 256
   server.max_cons_per_ip = 5
   server.serve_forever()
if __name__ == '__main__':
   main()




