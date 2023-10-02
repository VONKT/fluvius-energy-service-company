import time
import pytest
from unittest.mock import patch

from fluvius_energy_service_company.fluvius_authentication import (
    FluviusAuthentication, 
    FluviusAuthenticationToken, 
    FluviusConfig
)

@pytest.fixture
def fluvius_auth_instance():
    config = FluviusConfig(
        tenant_id='test_tenant_id',
        client_id='test_client_id',
        certificate_thumb_print='123ABC',
        certificate_key='test_certificate_key',
        live_scope='test_live_scope',
        subscription_key='test_subscription_key',
        data_access_contract_number='test_data_access_contract_number',
    )
    return FluviusAuthentication(config)

def test__encode_thumbprint(fluvius_auth_instance):
    thumbprint = '1234567890abcdef'
    expected_output = 'EjRWeJCrze8='
    assert fluvius_auth_instance._encode_thumbprint(thumbprint) == expected_output

def test__get_signed_jwt(fluvius_auth_instance):
    expected_output = ...  # the expected output from your original test
    with patch('jwt.encode', return_value=expected_output):
        assert fluvius_auth_instance._get_signed_jwt() == expected_output

def test__token_is_valid(fluvius_auth_instance):
    assert not fluvius_auth_instance._token_is_valid()
    fluvius_auth_instance.token = FluviusAuthenticationToken(
        token_type='Bearer',
        expires_in=3600,
        ext_expires_in=0,
        access_token='test_access_token'
    )
    fluvius_auth_instance.current_token_end_time = int(time.time()) + 3600
    assert fluvius_auth_instance._token_is_valid()
    fluvius_auth_instance.current_token_end_time = int(time.time()) - 3600
    assert not fluvius_auth_instance._token_is_valid()

def test_create_authorization_header(fluvius_auth_instance):
    expected_output = {
        'Authorization': 'Bearer test_access_token',
        'Ocp-Apim-Subscription-Key': 'test_subscription_key',
        'Content-Type': 'application/json',
    }
    with patch.object(FluviusAuthentication, 'get_token', return_value=FluviusAuthenticationToken(
        token_type='Bearer',
        expires_in=3600,
        ext_expires_in=0,
        access_token='test_access_token'
    )):
        assert fluvius_auth_instance.create_authorization_header() == expected_output

def test_get_token(fluvius_auth_instance):
    expected_output = FluviusAuthenticationToken(
        token_type='Bearer',
        expires_in=3600,
        ext_expires_in=0,
        access_token='test_access_token'
    )
    with patch.object(FluviusAuthentication, '_get_fluvius_token', return_value=expected_output):
        assert fluvius_auth_instance.get_token() == expected_output
        assert fluvius_auth_instance.token == expected_output
