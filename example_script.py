# Authenticate

from fluvius_energy_service_company.fluvius_authentication import FluviusAuthentication
from fluvius_energy_service_company.fluvius_config import FluviusConfig
from fluvius_energy_service_company.v2.energy_service_company import EnergyServiceCompany

authentication = FluviusAuthentication(fluvius_config=FluviusConfig())

print(authentication.get_token().access_token)

# API
energy_service_company = EnergyServiceCompany()

energy_service_company.get_health()

energy_service_company.create_short_url('123456789')

energy_service_company.get_mandate()

energy_service_company.get_mandate_energy(123456789, '2020-11-17T23:00:00Z', '2020-11-18T23:00:00Z')