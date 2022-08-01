"""Constants used by HelloSign integration."""
DOMAIN = "hellosign"

CONF_ENV = "env"
ENV_PRODUCTION = "production"
ENV_STAGING = "staging"
ENV_DEV = "dev"
ALLOWED_ENVS = [ENV_PRODUCTION, ENV_STAGING, ENV_DEV]
DEFAULT_ENV = ENV_PRODUCTION

CONF_TEST_MODE = "test_mode"
DEFAULT_TEST_MODE = False
