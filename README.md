# fluvius-energy-service-company
Wrapper for the Fluvius energy service company API that you can use as an "Energie dienstverlener".

![Overview](Overview.png)

## Goal and purpose
This packages wraps the apis that are available for `Energiedienstverleners`.
`Energiedienstverleners` are companies that have a contract with the Flemish DSO Fluvius and allows them to retrieve energy data from their users.
To become a `Energiedienstverlener` you have to have a `data access contract`.
More information can be found here: https://partner.fluvius.be/nl/energiedienstverleners.

The purpose of this package is to make the use of the `fluvius-energy-service-company` API easier. The package wraps arround the API operation so that they can be natively used in python code.

## Example usage
```python
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
```