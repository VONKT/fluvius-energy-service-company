

from fluvius_energy_service_company.data_objects.FluviusMeasurement import FluviusMeasurement


class FluviusQuarterHourlyEnergy:
    def __init__(self, timestamp_start: str, timestamp_end: str, measurement: FluviusMeasurement):
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end
        self.measurement: FluviusMeasurement = measurement

    def __repr__(self):
        return (f"FluviusQuarterHourlyEnergy(timestamp_start={self.timestamp_start!r}, "
                f"timestamp_end={self.timestamp_end!r}, measurement={self.measurement!r})")

    def __str__(self):
        return f"Start: {self.timestamp_start}, End: {self.timestamp_end}, Measurement: {self.measurement}"

    def get_offtake_array(self):
        return [self.timestamp_start] + self.measurement.get_offtake_array()

    def get_injection_array(self):
        return [self.timestamp_start] + self.measurement.get_injection_array()
