import pytest
from unittest import mock

from yosai.core import (
    AccountStoreRealm,
    Credential,
    DefaultAuthenticator,
    DefaultEventBus,
    DefaultSessionContext,
    DefaultSubjectContext,
    FirstRealmSuccessfulStrategy,
    ModularRealmAuthorizer,
    PasswordVerifier,
    SimpleIdentifierCollection,
)

from .doubles import (
    MockAccount,
    MockAccountStore,
    MockPubSub,
    MockSecurityManager,
    MockSecUtil,
    MockSession,
    MockSubject,
    MockSubjectBuilder,
    MockThreadContext,
    MockToken,
)

from .session.doubles import (
    MockDefaultNativeSessionManager,
)

from .authz.doubles import (
    MockAuthzAccountStoreRealm,
)

@pytest.fixture(scope='function')
def mock_account_state():
    return {'account_id': 'identifier',
            'creds': Credential('$bcrypt-sha256$2a,12$xVPxYhwlLOgStpiHCJNJ9u$wM.B.VVoJ1Lv0WeT4cRFY1PqYWH37WO'),
            'attributes': {'attribute1': 'attribute1'}}


@pytest.fixture(scope='function')
def full_mock_account(mock_account_state):
    mas = mock_account_state
    return MockAccount(account_id=mas['account_id'],
                       credentials=mas['creds'],
                       attributes=mas['attributes'])


@pytest.fixture(scope='function')
def return_true(**kwargs):
    return True


@pytest.fixture(scope='function')
def default_accountstorerealm(monkeypatch, core_settings):
    asr = AccountStoreRealm(core_settings, name='AccountStoreRealm')

    account_store = type('AccountStore', (object,), {})()
    cache_handler = type('CacheHandler', (object,), {})()
    mock_account = type('Account', (object,), {})()
    mock_account.identifier = 'identifier'
    mock_account.credentials = 'stored_creds'
    mock_account.authz_info = 'stored_authzinfo'

    monkeypatch.setattr(account_store, 'get_credentials',
                        lambda x: mock_account, raising=False)
    monkeypatch.setattr(account_store, 'get_authz_info',
                        lambda x: mock_account, raising=False)
    monkeypatch.setattr(cache_handler, 'get_or_create',
                        lambda domain, identifier, creator_func, creator:
                        creator_func(creator), raising=False)
    monkeypatch.setattr(asr, 'account_store', account_store)
    monkeypatch.setattr(asr, 'cache_handler', cache_handler)

    return asr


@pytest.fixture(scope='function')
def mock_account_store():
    return MockAccountStore()


@pytest.fixture(scope='function')
def mock_token():
    return MockToken()


@pytest.fixture(scope='function')
def default_password_matcher(core_settings):
    return PasswordVerifier(core_settings)

@pytest.fixture(scope='function')
def mock_pubsub():
    return MockPubSub()

@pytest.fixture(scope='function')
def patched_event_bus(mock_pubsub, monkeypatch):
    eb = DefaultEventBus()
    monkeypatch.setattr(eb, '_event_bus', mock_pubsub)
    return eb


@pytest.fixture(scope="function")
def first_realm_successful_strategy():
    return FirstRealmSuccessfulStrategy()


@pytest.fixture(scope='function')
def default_authenticator(
        first_realm_successful_strategy, monkeypatch, default_accountstorerealm, event_bus):
    da = DefaultAuthenticator(first_realm_successful_strategy)
    da.event_bus = event_bus
    da.realms = (default_accountstorerealm,)
    return da


@pytest.fixture(scope='function')
def mock_default_session_manager(attributes_schema, core_settings):
    return MockDefaultNativeSessionManager(attributes_schema, core_settings)


@pytest.fixture(scope='function')
def mock_subject_context():
    return mock.create_autospec(DefaultSubjectContext)


@pytest.fixture(scope='function')
def mock_subject():
    return MockSubject()


@pytest.fixture(scope='function')
def mock_session():
    return MockSession()


@pytest.fixture(scope='function')
def mock_security_manager():
    return MockSecurityManager()


@pytest.fixture(scope='function')
def default_session_context():
    return DefaultSessionContext(context_map={'attr1': 'attributeOne',
                                              'attr2': 'attributeTwo',
                                              'attr3': 'attributeThree'})


@pytest.fixture(scope='function')
def mock_thread_context():
    return MockThreadContext()


@pytest.fixture(scope='function')
def mock_subject_builder(mock_security_manager, yosai):
    csu = yosai
    return MockSubjectBuilder(security_utils=csu, 
                              security_manager=mock_security_manager)


@pytest.fixture(scope='function')
def simple_identifier_collection():
    return SimpleIdentifierCollection(source_name='AccountStoreRealm',
                                      identifier='identifier')

@pytest.fixture(scope='function')
def authz_realms_collection():
    """
    three authorizing realms
    """
    return (MockAuthzAccountStoreRealm(),
            MockAuthzAccountStoreRealm(),
            MockAuthzAccountStoreRealm())


@pytest.fixture(scope='function')
def modular_realm_authorizer_patched(
        monkeypatch, authz_realms_collection, event_bus):
    a = ModularRealmAuthorizer()
    monkeypatch.setattr(a, '_realms', authz_realms_collection)
    monkeypatch.setattr(a, '_event_bus', event_bus)
    return a


@pytest.fixture(scope='function')
def mock_secutil():
    return MockSecUtil()

