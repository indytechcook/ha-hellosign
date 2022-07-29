"""Constants used by HelloSign integration."""
DOMAIN = "hellosign"

CONF_ENV = "env"
ENV_PRODUCTION = "production"
ENV_STAGING = "staging"
ENV_DEV = "dev"
ALLOWED_ENVS = [ENV_PRODUCTION, ENV_STAGING, ENV_DEV]
DEFAULT_ENV = ENV_PRODUCTION

API_PRODUCTION_URL = "https://api.hellosign.com"
API_DEV_URL = "https://api.dev-hellosign.com"
API_STAGING_URL = "https://api.staging-hellosign.com"

WEB_PRODUCTION_URL = "https://app.hellosign.com"
WEB_DEV_URL = "https://app.dev-hellosign.com"
WEB_STAGING_URL = "https://app.staging-hellosign.com"

CONF_TEST_MODE = "test_mode"
DEFAULT_TEST_MODE = False
