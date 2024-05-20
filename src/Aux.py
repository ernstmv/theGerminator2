import cv2
from datetime import datetime
import paramiko
import numpy as np


class Aux:

    def __init__(self):
        self.ip_server_address = '192.168.1.1'
        self.username = 'kaibil'
        self.password = 'gafe'
        self.local_path = '/home/sword/theGerminator/.imgs/img.jpg'
        self.remote_path = '/srv/http/img'
        self.local_coordinates_file = '/home/sword/theGerminator/.data/coordinates.txt'
        self.remote_coordinates_file = '/home/kaibil/Documents/PROYECTOGERMINADOR/coordinates.txt'

    def write_data(self, img, n_p, ts, p):
        w, h = img.shape[1], img.shape[0]
        canvas = np.zeros((int(h/3), w, 3), np.uint8)
        self.img = cv2.vconcat([img, canvas])

        cv2.putText(
                self.img,
                f'Plants: {n_p}',
                (30, int(h * 1.07)),
                5,
                1,
                (255, 255, 255))

        cv2.putText(
                self.img,
                f'Tray size: {ts}',
                (30, int(h * 1.17)),
                5,
                1,
                (255, 255, 255))

        cv2.putText(
                self.img,
                f'Germination  percentage: {p}',
                (30, int(h * 1.27)),
                5,
                1,
                (255, 255, 255))

        cv2.imwrite(self.local_path, self.img)

    def send_data(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(
                    self.ip_server_address,
                    username=self.username,
                    password=self.password)

            sftp = ssh.open_sftp()

            now = datetime.now()
            seg = str(now.second)

            sftp.put(self.local_path, self.remote_path + seg + '.jpg')

            sftp.close()

            ssh.close()
            return "El archivo se ha enviado con éxito."
        except Exception as e:
            ssh.close()
            return "Error al enviar el archivo:" + str(e)

    def write_coordinates(self, coordinates_list):

        coordinates = [(x, y, 0) for x, y in coordinates_list]

        with open((self.local_coordinates_file), 'w') as file:
            file.write(str(coordinates))
        pass

    # PENDIENTE
    def send_coordinates(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        mssg = ''

        try:
            ssh.connect(
                    self.ip_server_address,
                    username=self.username,
                    password=self.password)

            sftp = ssh.open_sftp()

            sftp.put(self.local_coordinates_file, self.remote_coordinates_file)

            sftp.close()

            mssg = "El archivo se ha enviado con éxito."
        except Exception as e:
            mssg = "Error al enviar el archivo:" + e
        finally:
            ssh.close()
            return mssg
        pass
