from fluvius_energy_service_company.v2.energy_service_company import EnergyServiceCompany

# All the necessary envrionment variables should be set or given as an argument.
# Authentication is done automatically.
energy_service_company = EnergyServiceCompany()
# Get the health of the API
energy_service_company.get_health()
# Create a short URL
energy_service_company.create_short_url('123456789')
# Retrieve all mandates
energy_service_company.get_mandate()
# Retrieve the energy data for a given mandate
energy_service_company.get_mandate_energy(123456789, '2020-11-17T23:00:00Z', '2020-11-18T23:00:00Z')