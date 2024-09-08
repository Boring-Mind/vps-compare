import os
from unittest import TestCase
from unittest.mock import patch

from commons.environment_variables import EnvVariable


class EnvVariableTestCase(TestCase):
    @patch.dict(os.environ, {"SECRET_ENV_VARIABLE": "secret_key"})
    def test_get_default(self):
        actual_result = EnvVariable.get("SECRET_ENV_VARIABLE")

        self.assertEqual(actual_result, "secret_key")

    @patch.dict(os.environ, {})
    def test_get__env_variable_is_missing(self):
        with self.assertRaisesRegex(
            ValueError, "Environment variable SECRET_ENV_VARIABLE is missing."
        ):
            EnvVariable.get("SECRET_ENV_VARIABLE")

    @patch.dict(os.environ, {"ANOTHER_VARIABLE": "secret_key"})
    def test_get__other_env_variable_is_present(self):
        with self.assertRaisesRegex(
            ValueError, "Environment variable SECRET_ENV_VARIABLE is missing."
        ):
            EnvVariable.get("SECRET_ENV_VARIABLE")

    @patch.dict(os.environ, {})
    def test_get__default_value_was_provided(self):
        actual_result = EnvVariable.get("SECRET_ENV_VARIABLE", default=["some_value"])

        self.assertEqual(actual_result, ["some_value"])

    @patch.dict(os.environ, {"SECRET_ENV_VARIABLE": "123456"})
    def test_get_cast_integer(self):
        actual_result = EnvVariable.get("SECRET_ENV_VARIABLE", cast=int)

        self.assertEqual(actual_result, 123456)

    @patch.dict(os.environ, {"SECRET_ENV_VARIABLE": "2623161.2511531"})
    def test_get_cast_integer__float_was_provided(self):
        with self.assertRaisesRegex(
            ValueError,
            (
                "Environment variable SECRET_ENV_VARIABLE is not a valid integer. "
                "Actual value was: 2623161.2511531"
            ),
        ):
            EnvVariable.get("SECRET_ENV_VARIABLE", cast=int)

    @patch.dict(os.environ, {"SECRET_ENV_VARIABLE": "2623161.2511531"})
    def test_get_cast_float(self):
        actual_result = EnvVariable.get("SECRET_ENV_VARIABLE", cast=float)

        self.assertEqual(actual_result, 2623161.2511531)

    @patch.dict(os.environ, {"SECRET_ENV_VARIABLE": "165626565"})
    def test_get_cast_float__int_was_provided(self):
        actual_result = EnvVariable.get("SECRET_ENV_VARIABLE", cast=float)

        self.assertEqual(actual_result, 165626565.0)

    @patch.dict(
        os.environ, {"SECRET_ENV_VARIABLE": '["some_key", "some_value", {"a": "b"}]'}
    )
    def test_get_cast_json(self):
        actual_result = EnvVariable.get("SECRET_ENV_VARIABLE", cast="json")

        self.assertEqual(actual_result, ["some_key", "some_value", {"a": "b"}])

    @patch.dict(os.environ, {"SECRET_ENV_VARIABLE": "1"})
    def test_get_cast_bool(self):
        actual_result = EnvVariable.get("SECRET_ENV_VARIABLE", cast=bool)

        self.assertEqual(actual_result, True)

    @patch.dict(os.environ, {"SECRET_ENV_VARIABLE": "TruE"})
    def test_get_cast_bool__another_true_value(self):
        actual_result = EnvVariable.get("SECRET_ENV_VARIABLE", cast=bool)

        self.assertEqual(actual_result, True)

    @patch.dict(os.environ, {"SECRET_ENV_VARIABLE": "FaLsE"})
    def test_get_cast_bool__false_value(self):
        actual_result = EnvVariable.get("SECRET_ENV_VARIABLE", cast=bool)

        self.assertEqual(actual_result, False)

    @patch.dict(os.environ, {"SECRET_ENV_VARIABLE": "0"})
    def test_get_cast_bool__another_false_value(self):
        actual_result = EnvVariable.get("SECRET_ENV_VARIABLE", cast=bool)

        self.assertEqual(actual_result, False)

    @patch.dict(os.environ, {"SECRET_ENV_VARIABLE": "35153351351"})
    def test_get_cast_bool__int_was_provided(self):
        with self.assertRaisesRegex(
            ValueError,
            (
                "Environment variable SECRET_ENV_VARIABLE is not a valid boolean string. "
                "Actual value was: 35153351351"
            ),
        ):
            EnvVariable.get("SECRET_ENV_VARIABLE", cast=bool)
