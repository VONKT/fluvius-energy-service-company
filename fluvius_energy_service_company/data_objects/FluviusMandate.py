

from fluvius_energy_service_company.data_objects.FluviusData import FluviusData
from fluvius_energy_service_company.data_objects.FluviusDataResponse import FluviusDataResponse


class FluviusMandate:
    def __init__(self, reference_number: str, status: str, ean_number: int, energy_type: str, date_period_from: str,
                 data_service_type: str):
        self.reference_number = reference_number
        self.status = status
        self.ean_number = ean_number
        self.energy_type = energy_type
        self.date_period_from = date_period_from
        self.data_service_type = data_service_type


class FluviusMandateData(FluviusData):
    def __init__(self, fetch_time: str, mandates: list[FluviusMandate]):
        super().__init__(fetch_time)
        self.mandates = mandates

    def __str__(self):
        mandates_str = ''
        for mandate in self.mandates:
            mandates_str += mandate.__str__() + '\n'
        return mandates_str


class FluviusMandateDataResponse(FluviusDataResponse):
    def __init__(self, fetch_time: str, mandates: list[FluviusMandate]):
        data = FluviusMandateData(fetch_time, mandates)
        super().__init__(data)
