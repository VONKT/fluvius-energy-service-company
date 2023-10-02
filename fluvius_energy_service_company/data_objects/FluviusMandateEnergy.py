from typing import Any

from fluvius_energy_service_company.data_objects.FluviusData import FluviusData
from fluvius_energy_service_company.data_objects.FluviusDataResponse import FluviusDataResponse
from fluvius_energy_service_company.data_objects.FluviusElectricityMeter import FluviusElectricityMeter


class FluviusMandateEnergyData(FluviusData):
    def __init__(self, fetch_time: str, gas_meters: list[Any], electricity_meters: list[FluviusElectricityMeter]):
        super().__init__(fetch_time)
        self.gas_meters = gas_meters
        self.electricity_meters = electricity_meters

    def __str__(self):
        meters_str = ''
        for meter in self.electricity_meters:
            meters_str += meter.__str__() + '\n'
        return meters_str


class FluviusMandateEnergyDataResponse(FluviusDataResponse):
    def __init__(self, fetch_time: str, electricity_meters: list[FluviusElectricityMeter]):
        data = FluviusMandateEnergyData(fetch_time, [], electricity_meters)
        super().__init__(data)
