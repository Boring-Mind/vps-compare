import os
from unittest import TestCase
from unittest.mock import patch

from commons.environment_variables import get_env_variable


class GetEnvVariableTestCase(TestCase):
    @patch.dict(os.environ, {"SECRET_ENV_VARIABLE": "secret_key"})
    def test_get_env_variable_default(self):
        actual_result = get_env_variable("SECRET_ENV_VARIABLE")

        self.assertEqual(actual_result, "secret_key")

    @patch.dict(os.environ, {})
    def test_get_env_variable_env_variable_is_missing(self):
        with self.assertRaisesRegex(
            ValueError, "Environment variable SECRET_ENV_VARIABLE is missing."
        ):
            get_env_variable("SECRET_ENV_VARIABLE")

    @patch.dict(os.environ, {"ANOTHER_VARIABLE": "secret_key"})
    def test_get_env_variable_other_env_variable_is_present(self):
        with self.assertRaisesRegex(
            ValueError, "Environment variable SECRET_ENV_VARIABLE is missing."
        ):
            get_env_variable("SECRET_ENV_VARIABLE")
