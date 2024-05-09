import paramiko
import datetime


# see https://rajansahu713.medium.com/sftp-files-transfer-using-python-59b4cead090a


def send_file_via_sftp(filename, server_address, username, password):
    now = datetime.datetime.now()
    try:
        port = 2022
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            hostname=server_address, port=port, username=username, password=password
        )
        sftp = ssh_client.open_sftp()
        sftp.put(localpath=filename, remotepath=filename)
        sftp.close()
        ssh_client.close()
        print("File successfully sent via SFTP.", now)
    except:
        print("There was a problem sending the datafile via SFTP!", now)
