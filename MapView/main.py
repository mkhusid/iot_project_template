import asyncio
from kivy.app import App
from kivy_garden.mapview import MapMarker, MapView
from kivy.clock import Clock
from lineMapLayer import LineMapLayer
from datasource import Datasource


class MapViewApp(App):
    def __init__(self, **kwargs):
        super().__init__()
        self.datasource = Datasource()
        self.car_marker = None

    def on_start(self):
        """
        Встановлює необхідні маркери, викликає функцію для оновлення мапи
        """
        Clock.schedule_interval(self.update, 1 / 100.0)

    def update(self, *args):
        """
        Викликається регулярно для оновлення мапи
        """
        new_data, last_gps = self.datasource.get_new_data()

        if last_gps:
            print("Updating")
            self.update_car_marker(last_gps)

        for data in new_data:
            if data.road_state == "bump":
                self.set_bump_marker(data.agent_data.gps)
            if data.road_state == "pothole":
                self.set_pothole_marker(data.agent_data.gps)

    def update_car_marker(self, point):
        """
        Оновлює відображення маркера машини на мапі
        :param point: GPS координати
        """
        if self.car_marker:
            self.car_marker.detach()

        print(point.latitude, point.longitude)
        self.car_marker = MapMarker(lat=point.latitude, lon=point.longitude, source='images/car.png')
        self.mapview.add_marker(self.car_marker)
        self.mapview.center_on(point.latitude, point.longitude)

    def set_pothole_marker(self, point):
        """
        Встановлює маркер для ями
        :param point: GPS координати
        """
        self.mapview.add_marker(
            MapMarker(lat=point.latitude, lon=point.longitude, source='images/pothole.png')
        )

    def set_bump_marker(self, point):
        """
        Встановлює маркер для лежачого поліцейського
        :param point: GPS координати
        """
        self.mapview.add_marker(
            MapMarker(lat=point.latitude, lon=point.longitude, source='images/bump.png')
        )

    def build(self):
        """
        Ініціалізує мапу MapView(zoom, lat, lon)
        :return: мапу
        """
        self.mapview = MapView(zoom=12, lat=50.4501, lon=30.5234)
        self.mapview.add_layer(LineMapLayer())
        return self.mapview


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(MapViewApp().async_run(async_lib="asyncio"))
    loop.close()
