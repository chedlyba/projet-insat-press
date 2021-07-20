import paramiko 

DESTINATION_FOLDER='/home/nov/python/downloaded_files'

ssh_client= paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname="192.168.56.102", username="nov", password="120100")

ftp_client=ssh_client.open_sftp()
ftp_client.put(input(),input())
#test comment
ftp_client.close()
