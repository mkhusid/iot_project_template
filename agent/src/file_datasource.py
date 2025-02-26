from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
import config


class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        accelerometer_data = self._read_accelerometer_data()
        gps_data = self._read_gps_data()
        return AggregatedData(
            accelerometer_data,
            gps_data,
            datetime.now(),
            config.USER_ID
        )

    def _read_accelerometer_data(self) -> Accelerometer:
        if self.accelerometer_reader_ is not None:
            try:
                
                row = next(self.accelerometer_reader_, None)
                if row:
                    x, y, z = map(int, row)
                    return Accelerometer(x, y, z)
                else:
                    raise StopIteration
            except StopIteration:
                print(
                    "Кінець файлу із даними для акселерометру, повертаємось до початку файлу")
                self.accelerometer_file_.seek(0)
                self.accelerometer_reader_ = reader(self.accelerometer_file_)
                next(self.accelerometer_reader_, None)  # Пропускаємо заголовок
                return self._read_accelerometer_data()
        else:
            raise Exception("Читач не був ініціалізований")

    def _read_gps_data(self) -> Gps:
        if self.gps_reader_ is not None:
            try:
                row = next(self.gps_reader_, None)
                if row:
                    longitude, latitude = map(float, row)
                    return Gps(longitude, latitude)
                else:
                    raise StopIteration
            except StopIteration:
                print(
                    "Кінець файлу із даними для GPS, повертаємось до початку файлу")
                self.gps_file_.seek(0)
                self.gps_reader_ = reader(self.gps_file_)
                next(self.gps_reader_, None)  # Пропускаємо заголовок
                return self._read_gps_data()
        else:
            raise Exception("Читач не був ініціалізований")

    def startReading(self, *args, **kwargs) -> None:
        """Метод повинен викликатись перед початком читання даних"""
        try:
            self.accelerometer_file_ = open(self.accelerometer_filename, 'r')
            self.gps_file_ = open(self.gps_filename, 'r')
            self.accelerometer_reader_ = reader(self.accelerometer_file_)
            self.gps_reader_ = reader(self.gps_file_)
            # Пропускаємо перший рядок - заголовок
            next(self.accelerometer_reader_, None)
            next(self.gps_reader_, None)
        except FileNotFoundError as error:
            print(f"Файл не був знайдений: {error}")
        except Exception as error:
            print(f"Error: {error}")

    def stopReading(self, *args, **kwargs) -> None:
        """Метод повинен викликатись для закінчення читання даних"""
        if self.accelerometer_file_:
            self.accelerometer_file_.close()
        if self.gps_file_:
            self.gps_file_.close()
