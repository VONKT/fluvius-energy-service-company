import http.client
import json
from typing import Any, Optional
import urllib.parse

from fluvius_energy_service_company.data_objects.FluviusElectricityMeter import FluviusElectricityMeter
from fluvius_energy_service_company.data_objects.FluviusMeasurement import FluviusMeasurement
from fluvius_energy_service_company.data_objects.FluviusQuarterHourlyEnergy import FluviusQuarterHourlyEnergy
from fluvius_energy_service_company.data_objects.FluviusMandate import FluviusMandate, FluviusMandateDataResponse
from fluvius_energy_service_company.data_objects.FluviusMandateEnergy import FluviusMandateEnergyDataResponse
from fluvius_energy_service_company.fluvius_authentication import FluviusAuthentication
from fluvius_energy_service_company.fluvius_config import FluviusConfig


class EnergyServiceCompany:

    def __init__(self, fluvius_config: FluviusConfig = None) -> None:
        if fluvius_config is None:
            self.config = FluviusConfig()
        if fluvius_config is not None:
            self.config = fluvius_config
        self.fluvius_authentication = FluviusAuthentication(self.config)
        self.apihub_conn = http.client.HTTPSConnection("apihub.fluvius.be")
    
    def get_health(self) -> Any:
        endpoint_name = "/esco-live/api/v2.0/health"
        try:
            header = self.fluvius_authentication.create_authorization_header()
            self.apihub_conn.request("GET", endpoint_name, None, header)
            res = self.apihub_conn.getresponse()
            data = res.read()
            return data.decode("utf-8")
        except Exception as ex:
            print(f"Calling ${endpoint_name} failed with ${ex}", ex)
            return
        
    def create_short_url(self, reference_number, flow: str = 'B2C', number_of_eans: int = 1) -> Any:
        endpoint_name = "/esco-live/api/v2.0/shortUrlIdentifier"
        try:
            header = self.fluvius_authentication.create_authorization_header()
            payload = json.dumps({
                "dataAccessContractNumber": self.config.data_access_contract_number,
                "referenceNumber": reference_number,
                "flow": flow,
                "dataServices": [
                    {
                        "dataServiceType": "VH_kwartier_uur",
                    },
                    {
                        "dataServiceType": "VH_dag",
                    }
                ],
                "numberOfEans": number_of_eans
            })
            self.apihub_conn.request("POST", endpoint_name, payload, header)
            res = self.apihub_conn.getresponse()
            data = res.read()
            return json.loads(data.decode("utf-8"))

        except Exception as ex:
            print(f"Calling ${endpoint_name} failed with ${ex}", ex)
            return

    @staticmethod
    def _decode_fluvius_mandate(response: Any) -> FluviusMandateDataResponse:
        if not response['data'] or not response['data']['fetchTime'] or not response['data']['mandates']:
            raise ValueError('Invalid response, not able to map')
        mandates = []
        for raw_mandate in response['data']['mandates']:
            mandates.append(FluviusMandate(
                reference_number=raw_mandate['referenceNumber'],
                status=raw_mandate['status'],
                ean_number=raw_mandate['eanNumber'],
                energy_type=raw_mandate['energyType'],
                date_period_from=raw_mandate['dataPeriodFrom'],
                data_service_type=raw_mandate['dataServiceType']
            ))
        return FluviusMandateDataResponse(fetch_time=response['data']['fetchTime'], mandates=mandates)

    def get_mandate(self, ean: int = None, data_service_type: str = None,
                    energy_type: str = 'E', status: str = None) -> Optional[FluviusMandateDataResponse]:
        endpoint_name = "/esco-live/api/v2.0/mandate"
        try:
            header = self.fluvius_authentication.create_authorization_header()
            query = {
                'EnergyType': energy_type,
            }
            if ean:
                query['EanNumber'] = ean
            if data_service_type:
                query['DataServiceType'] = data_service_type
            if status:
                query['Status'] = status
            query_string = urllib.parse.urlencode(query)
            self.apihub_conn.request("GET", endpoint_name + '?' + query_string, None, header)
            res = self.apihub_conn.getresponse()
            data = res.read()
            return self._decode_fluvius_mandate(json.loads(data))

        except Exception as ex:
            print(f"Calling {endpoint_name} failed with {ex}", ex)
            return
        
    @staticmethod
    def _decode_fluvius_mandate_energy(response: Any) -> FluviusMandateEnergyDataResponse:
        if not response['data'] or not response['data']['fetchTime'] or not response['data']['electricityMeters']:
            raise ValueError('Invalid response, not able to map')
        electricity_meters = []
        for raw_electricity_meter in response['data']['electricityMeters']:
            quarter_hourly_energy = []
            for raw_quarter_hourly_energy in raw_electricity_meter['quarterHourlyEnergy']:
                if raw_quarter_hourly_energy['measurement'] is None:
                    break
                if len(raw_quarter_hourly_energy['measurement']) != 1:
                    raise ValueError('Multiple measurements, not supported')
                try:
                    unit = raw_quarter_hourly_energy['measurement'][0]['unit']
                    offtake_value = raw_quarter_hourly_energy['measurement'][0]['offtakeValue'] \
                        if 'offtakeValue' in raw_quarter_hourly_energy['measurement'][0] else 0
                    offtake_validation_state = raw_quarter_hourly_energy['measurement'][0]['offtakeValidationState'] \
                        if 'offtakeValidationState' in raw_quarter_hourly_energy['measurement'][0] else 'UNVAL'
                    injection_value = raw_quarter_hourly_energy['measurement'][0]['injectionValue'] \
                        if 'injectionValue' in raw_quarter_hourly_energy['measurement'][0] else 0
                    injection_validation_state = raw_quarter_hourly_energy['measurement'][0]['injectionValidationState'] \
                        if 'injectionValidationState' in raw_quarter_hourly_energy['measurement'][0] else 'UNVAL'
                    measurement = FluviusMeasurement(
                        unit=unit,
                        offtake_value=float(offtake_value),
                        offtake_validation_state=offtake_validation_state,
                        injection_value=float(injection_value),
                        injection_validation_state=injection_validation_state)
                    quarter_hourly_energy.append(FluviusQuarterHourlyEnergy(
                        timestamp_start=raw_quarter_hourly_energy['timestampStart'],
                        timestamp_end=raw_quarter_hourly_energy['timestampEnd'],
                        measurement=measurement
                    ))
                except Exception as e:
                    print(e)
            electricity_meters.append(FluviusElectricityMeter(
                seq_number=raw_electricity_meter['seqNumber'],
                meter_id=raw_electricity_meter['meterID'],
                daily_energy=[],
                quarter_hourly_energy=quarter_hourly_energy
            ))

        return FluviusMandateEnergyDataResponse(fetch_time=response['data']['fetchTime'],
                                                electricity_meters=electricity_meters)

    def get_mandate_energy(self,
                           ean: int,
                           from_time,
                           to_time: str,
                           reference_number: str = None,
                           data_service_type: str = 'VH_kwartier_uur',
                           energy_type: str = 'E',
                           period_type: str = 'readTime') -> Optional[FluviusMandateEnergyDataResponse]:
        endpoint_name = "/esco-live/api/v2.0/mandate/energy"
        try:
            header = self.fluvius_authentication.create_authorization_header()
            query = {
                'EanNumber': ean,
                'DataServiceType': data_service_type,
                'EnergyType': energy_type,
                'PeriodType': period_type,
                'From': from_time,
                'To': to_time,
            }
            if reference_number:
                query['ReferenceNumber'] = reference_number
            query_string = urllib.parse.urlencode(query)
            self.apihub_conn.request("GET", endpoint_name + '?' + query_string, None, header)
            res = self.apihub_conn.getresponse()
            data = res.read()
            return self._decode_fluvius_mandate_energy(json.loads(data))

        except Exception as ex:
            print(f"Calling {endpoint_name} failed with {ex}", ex)
            return