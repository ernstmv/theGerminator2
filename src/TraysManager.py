class TraysManager:
    def __init__(self):
        self.trays_path = '/home/leviathan/theGerminator2/.data/trays.txt'
        self.coordinates_path = '/home/leviathan/theGerminator2/.data/'
        self.areas_path = '/home/leviathan/theGerminator2/.data/'

    def add_tray(self, content):
        with open(self.trays_path, 'a') as file:
            file.write(','.join(map(str, content)))
            file.write('\n')

    def add_coordinates(self, tray_id, plant_coordinates):
        coordinates = [(x, y, 0) for x, y in plant_coordinates]

        with open(self.coordinates_path + tray_id + '_coord.txt', 'w') as file:
            file.write(str(coordinates))

    def add_areas(self, tray_id, plant_areas):
        with open(self.areas_path + tray_id + '_areas.txt', 'w') as file:
            file.write(str(plant_areas))
