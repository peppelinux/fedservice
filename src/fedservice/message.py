import logging

from oidcmsg.exception import MissingRequiredAttribute
from oidcmsg.message import Message
from oidcmsg.message import OPTIONAL_LIST_OF_SP_SEP_STRINGS
from oidcmsg.message import OPTIONAL_LIST_OF_STRINGS
from oidcmsg.message import REQUIRED_LIST_OF_STRINGS
from oidcmsg.message import SINGLE_OPTIONAL_ANY
from oidcmsg.message import SINGLE_OPTIONAL_INT
from oidcmsg.message import SINGLE_OPTIONAL_JSON
from oidcmsg.message import SINGLE_OPTIONAL_STRING
from oidcmsg.message import SINGLE_REQUIRED_INT
from oidcmsg.message import SINGLE_REQUIRED_STRING
from oidcmsg.message import msg_ser
from oidcmsg.oidc import JsonWebToken
from oidcmsg.oidc import ProviderConfigurationResponse
from oidcmsg.oidc import RegistrationResponse
from oidcmsg.oidc import SINGLE_OPTIONAL_BOOLEAN
from oidcmsg.oidc import SINGLE_OPTIONAL_DICT
from oidcmsg.oidc import deserialize_from_one_of
from oidcmsg.oidc import dict_deser
from oidcmsg.oidc import msg_ser_json

SINGLE_REQUIRED_DICT = (dict, True, msg_ser_json, dict_deser, False)


logger = logging.getLogger(__name__)


def registration_response_deser(val, sformat="json"):
    return deserialize_from_one_of(val, RegistrationResponse, sformat)


def provider_info_deser(val, sformat="json"):
    return deserialize_from_one_of(val, ProviderConfigurationResponse, sformat)


OPTIONAL_CLIENT_METADATA = (Message, False, msg_ser,
                            registration_response_deser, False)
OPTIONAL_PROVIDER_METADATA = (Message, False, msg_ser,
                              provider_info_deser, False)


class AuthorizationServerMetadata(Message):
    c_param = {
        "issuer": SINGLE_REQUIRED_STRING,
        "authorization_endpoint": SINGLE_OPTIONAL_STRING,
        "token_endpoint": SINGLE_OPTIONAL_STRING,
        "jwks_uri": SINGLE_OPTIONAL_STRING,
        "registration_endpoint": SINGLE_OPTIONAL_STRING,
        "scopes_supported": SINGLE_OPTIONAL_JSON,
        "response_types_supported": SINGLE_OPTIONAL_JSON,
        "response_modes_supported": SINGLE_OPTIONAL_JSON,
        "grant_types_supported": SINGLE_OPTIONAL_JSON,
        "token_endpoint_auth_methods_supported": SINGLE_OPTIONAL_JSON,
        "token_endpoint_auth_signing_alg_values_supported": SINGLE_OPTIONAL_JSON,
        "service_documentation": SINGLE_OPTIONAL_STRING,
        "ui_locales_supported": SINGLE_OPTIONAL_JSON,
        "op_policy_uri": SINGLE_OPTIONAL_STRING,
        "revocation_endpoint": SINGLE_OPTIONAL_STRING,
        "revocation_endpoint_auth_methods_supported": SINGLE_OPTIONAL_JSON,
        "revocation_endpoint_auth_signing_alg_values_supported": SINGLE_OPTIONAL_JSON,
        "introspection_endpoint": SINGLE_OPTIONAL_STRING,
        "introspection_endpoint_auth_methods_supported": SINGLE_OPTIONAL_JSON,
        "introspection_endpoint_auth_signing_alg_values_supported": SINGLE_OPTIONAL_JSON,
        "code_challenge_methods_supported": SINGLE_OPTIONAL_JSON
    }


def auth_server_info_deser(val, sformat="json"):
    return deserialize_from_one_of(val, AuthorizationServerMetadata, sformat)


OPTIONAL_AUTH_SERVER_METADATA = (Message, False, msg_ser,
                                 auth_server_info_deser, False)


class FederationEntity(Message):
    c_param = {
        "federation_api_endpoint": SINGLE_OPTIONAL_STRING,
        "name": SINGLE_OPTIONAL_STRING,
        "contacts": OPTIONAL_LIST_OF_STRINGS,
        "policy_url": SINGLE_OPTIONAL_STRING,
        "homepage_uri": SINGLE_OPTIONAL_STRING,
        "trust_anchor_id": SINGLE_OPTIONAL_STRING
    }


def federation_entity_deser(val, sformat="json"):
    return deserialize_from_one_of(val, FederationEntity, sformat)


OPTIONAL_FEDERATION_ENTITY_METADATA = (Message, False, msg_ser,
                                       federation_entity_deser, False)


class OauthClientMetadata(Message):
    c_param = {
        "redirect_uris": OPTIONAL_LIST_OF_STRINGS,
        "token_endpoint_auth_method": SINGLE_OPTIONAL_STRING,
        "grant_type": OPTIONAL_LIST_OF_STRINGS,
        "response_types": OPTIONAL_LIST_OF_STRINGS,
        "client_name": SINGLE_OPTIONAL_STRING,
        "client_uri": SINGLE_OPTIONAL_STRING,
        "logo_uri": SINGLE_OPTIONAL_STRING,
        "scope": OPTIONAL_LIST_OF_SP_SEP_STRINGS,
        "contacts": OPTIONAL_LIST_OF_STRINGS,
        "tos_uri": SINGLE_OPTIONAL_STRING,
        "policy_uri": SINGLE_OPTIONAL_STRING,
        "jwks_uri": SINGLE_OPTIONAL_STRING,
        "jwks": SINGLE_OPTIONAL_JSON,
        "software_id": SINGLE_OPTIONAL_STRING,
        "software_version": SINGLE_OPTIONAL_STRING
    }


def oauth_client_metadata_deser(val, sformat="json"):
    return deserialize_from_one_of(val, OauthClientMetadata, sformat)


OPTIONAL_OAUTH_CLIENT_METADATA = (Message, False, msg_ser,
                                  oauth_client_metadata_deser, False)


class OauthClientInformationResponse(OauthClientMetadata):
    c_param = OauthClientMetadata.c_param.copy()
    c_param.update({
        "client_id": SINGLE_REQUIRED_STRING,
        "client_secret": SINGLE_OPTIONAL_STRING,
        "client_id_issued_at": SINGLE_OPTIONAL_INT,
        "client_secret_expires_at": SINGLE_OPTIONAL_INT
    })

    def verify(self, **kwargs):
        if "client_secret" in self:
            if "client_secret_expires_at" not in self:
                raise MissingRequiredAttribute(
                    "client_secret_expires_at is a MUST if client_secret is present")


class Metadata(Message):
    c_param = {
        'openid_relying_party': OPTIONAL_CLIENT_METADATA,
        'openid_provider': OPTIONAL_PROVIDER_METADATA,
        "oauth_authorization_server": OPTIONAL_AUTH_SERVER_METADATA,
        "oauth_client": OPTIONAL_OAUTH_CLIENT_METADATA,
        "federation_entity": OPTIONAL_FEDERATION_ENTITY_METADATA
    }


def provider_info_deser(val, sformat="json"):
    return deserialize_from_one_of(val, Metadata, sformat)


SINGLE_REQUIRED_METADATA = (Message, True, msg_ser, provider_info_deser, False)
SINGLE_OPTIONAL_METADATA = (Message, False, msg_ser, provider_info_deser, False)


class MetadataPolicy(Message):
    c_param = {
        "subset_of": OPTIONAL_LIST_OF_STRINGS,
        "one_of": OPTIONAL_LIST_OF_STRINGS,
        "superset_of": OPTIONAL_LIST_OF_STRINGS,
        "add": OPTIONAL_LIST_OF_STRINGS,
        "value": SINGLE_OPTIONAL_ANY
    }


def metadata_policy_deser(val, sformat="json"):
    return deserialize_from_one_of(val, MetadataPolicy, sformat)


SINGLE_REQUIRED_METADATA_POLICY = (Message, True, msg_ser, metadata_policy_deser, False)
SINGLE_OPTIONAL_METADATA_POLICY = (Message, False, msg_ser, metadata_policy_deser, False)


class EntityStatement(JsonWebToken):
    c_param = JsonWebToken.c_param.copy()
    c_param.update({
        "sub": SINGLE_REQUIRED_STRING,
        'iss': SINGLE_REQUIRED_STRING,
        'exp': SINGLE_REQUIRED_INT,
        'iat': SINGLE_REQUIRED_INT,
        'authority_hints': REQUIRED_LIST_OF_STRINGS,
        'metadata': SINGLE_OPTIONAL_METADATA,
        'metadata_policy': SINGLE_OPTIONAL_METADATA_POLICY,
        'sub_meta': SINGLE_OPTIONAL_DICT,
        'sub_is_leaf': SINGLE_OPTIONAL_BOOLEAN,
        'jwks': SINGLE_OPTIONAL_DICT,
        'signing_keys': SINGLE_OPTIONAL_DICT
    })
