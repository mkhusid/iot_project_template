'''
This module is responsible for reading data from GPS and accelerometer files.
TODO:  Refactor according to the SOLID principles and GoF design patterns.
'''
import typing
from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
import config


class FileDatasource:
    """
    This class is responsible for reading data from GPS and accelerometer files.

    Example of usage:
    acc_fname, gps_fname = 'agent/src/data/accelerometer.csv', 'agent/src/data/gps.csv'

    with open(acc_fname, 'r', encoding='utf-8') as accelerometer_file,\
            open(gps_fname, 'r', encoding='utf-8') as gps_file:
        for i in range(100):
            f_reader = FileDatasource(accelerometer_file, gps_file)
            data = f_reader.read()
"""
    def __init__(
        self,
        accelerometer_file_: typing.TextIO,
        gps_file_: typing.TextIO,
    ) -> None:
        self.accelerometer_file = accelerometer_file_
        self.gps_file = gps_file_
        try:
            self.accelerometer_reader = reader(accelerometer_file_)
            self.gps_reader = reader(gps_file_)
            next(self.accelerometer_reader, None)
            next(self.gps_reader, None)
        except FileNotFoundError as error:
            print(f"The file was not found: {error}")
        except TypeError as error:
            print(f"An error occurred: {error}")


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
        '''Метод повертає дані отримані з акселерометра'''
        if self.accelerometer_reader is None:
            raise TypeError("The reader was not initialized")
        try:
            row = next(self.accelerometer_reader, None)
            if row is None:
                raise StopIteration
            x, y, z = map(int, row)
            return Accelerometer(x, y, z)
        except StopIteration:
            print(
                "End of file with data for accelerometer, going back to beginning of file")
            self.accelerometer_file.seek(0)
            self.accelerometer_reader = reader(self.accelerometer_file)
            next(self.accelerometer_reader, None)  # Skip the header
            return self._read_accelerometer_data()

    def _read_gps_data(self) -> Gps:
        '''Метод повертає дані отримані з GPS'''
        if self.gps_reader is None:
            raise TypeError("The reader was not initialized")
        try:
            row = next(self.gps_reader, None)
            if row is None:
                raise StopIteration
            latitude, longitude = map(float, row)

            return Gps(latitude, longitude)
        except StopIteration:
            print(
                "End of file with data for GPS, going back to the beginning of the file")
            self.gps_file.seek(0)
            self.gps_reader = reader(self.gps_file)
            next(self.gps_reader, None)  # Skip the header
            return self._read_gps_data()
