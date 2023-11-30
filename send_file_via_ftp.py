import ftplib
import datetime


def send_file_via_ftp(filename, server_address, username, password):
    now = datetime.datetime.now()
    try:
        session = ftplib.FTP(server_address, username, password)
        file = open(filename, 'rb')                  # file to send
        session.storbinary(f"STOR {filename}", file)     # send the file
        file.close()                                    # close file and FTP
        session.quit()
        print("File successfully sent via FTP.", now)
    except:
        print("There was a problem sending the datafile via FTP!", now)
