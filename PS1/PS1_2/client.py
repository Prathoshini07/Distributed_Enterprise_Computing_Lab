import ftplib
HOSTNAME = "10.1.66.240"  #system's ip address
USERNAME = "user"
PASSWORD = "pwd"


ftp_server = ftplib.FTP()
ftp_server.connect(HOSTNAME, 8087)
ftp_server.login(USERNAME, PASSWORD)
ftp_server.encoding = "utf-8"
filename = "client.txt" 


with open("/home/cslinux/Documents/client.txt", "rb") as file:
   ftp_server.storbinary(f"STOR {filename}", file)


ftp_server.dir()
ftp_server.quit()

