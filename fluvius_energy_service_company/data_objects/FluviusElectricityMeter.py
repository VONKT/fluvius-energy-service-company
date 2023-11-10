from typing import Any
import logging

from fluvius_energy_service_company.data_objects.FluviusQuarterHourlyEnergy import FluviusQuarterHourlyEnergy


class FluviusElectricityMeter:
    def __init__(self,
                 seq_number: str,
                 meter_id: str,
                 daily_energy: list[Any],
                 quarter_hourly_energy: list[FluviusQuarterHourlyEnergy]):
        self.seq_number = seq_number
        self.meter_id = meter_id
        self.daily_energy = daily_energy
        self.quarter_hourly_energy = self.set_quarter_hourly_energy(quarter_hourly_energy)

    @staticmethod
    def set_quarter_hourly_energy(quarter_hourly_energy: list[FluviusQuarterHourlyEnergy]):
        # Validate wether the quarter_hourly_energy list does not contain any duplicates
        # if it does, log a warning
        # but do not return the duplicate values
        timestamps = []
        for quarter_hourly in quarter_hourly_energy:
            if quarter_hourly.timestamp_start in timestamps:
                logging.warning(f"Duplicate timestamp_start found: {quarter_hourly.timestamp_start}")
            else:
                timestamps.append(quarter_hourly.timestamp_start)

        return list(set(quarter_hourly_energy))

    def __str__(self):
        energy_str = ''
        for energy in self.quarter_hourly_energy:
            energy_str += energy.__str__() + '\n'
        return energy_str

    def get_quarter_hourly_offtake_arrays(self, ean: int):
        return [[ean, self.meter_id, 'offtake'] + quarter_hourly.get_offtake_array() for quarter_hourly in
                self.quarter_hourly_energy]

    def get_quarter_hourly_injection_arrays(self, ean: int):
        return [[ean, self.meter_id, 'injection'] + quarter_hourly.get_injection_array() for quarter_hourly in
                self.quarter_hourly_energy]

    def to_arrays(self, ean):
        return self.get_quarter_hourly_offtake_arrays(ean) + self.get_quarter_hourly_injection_arrays(ean)
