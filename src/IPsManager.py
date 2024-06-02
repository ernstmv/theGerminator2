class IPsManager:
    def __init__(self):
        self.main_camera_ips = '/home/leviathan/theGerminator2/.ips/m_ips.txt'
        self.seco_camera_ips = '/home/leviathan/theGerminator2/.ips/s_ips.txt'

    def m_read_ip(self):
        with open(self.main_camera_ips, 'r') as file:
            ips = file.readlines()
        return [ip.strip() for ip in ips]

    def s_read_ip(self):
        with open(self.seco_camera_ips, 'r') as file:
            ips = file.readlines()
        return [ip.strip() for ip in ips]

    def m_write_ip(self, ip):
        with open(self.main_camera_ips, 'a') as file:
            file.write(ip + '\n')

    def s_write_ip(self, ip):
        with open(self.seco_camera_ips, 'a') as file:
            file.write(ip + '\n')

    def m_delete_ip(self, ip):
        ips = set(self.m_read_ip())
        try:
            ips.remove(ip)
        except Exception:
            pass
        with open(self.main_camera_ips, 'w') as file:
            for ip in ips:
                file.write(ip + '\n')

    def s_delete_ip(self, ip):
        ips = set(self.s_read_ip())
        try:
            ips.remove(ip)
        except Exception:
            pass
        with open(self.seco_camera_ips, 'w') as file:
            for ip in ips:
                file.write(ip + '\n')
