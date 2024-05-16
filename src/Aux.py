import cv2
import paramiko
import numpy as np


class Aux:

    def __init__(self):
        self.ip_server_address = 'IP PENDIENTE'
        self.username = 'unknown'
        self.password = 'unknown'
        self.local_path = '../.imgs/img.jpg'
        self.remote_path = '/etc/httpd/data'

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

    def launch_data(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(
                    self.ip_server_address,
                    username=self.username,
                    password=self.password)

            sftp = ssh.open_sftp()

            sftp.put(self.local_path, self.remote_path)

            sftp.close()

            mssg = "El archivo se ha enviado con éxito."
        except Exception as e:
            mssg = "Error al enviar el archivo:" + e
        finally:
            ssh.close()
            return mssg
