import importlib
import os
import unittest
from unittest.mock import patch

import kik_unofficial.configuration as configuration


class ConfigurationTests(unittest.TestCase):
    def test_process_environment_overrides_local_dotenv(self):
        try:
            with patch.dict(os.environ, {"BOT_USERNAME": "process-authoritative"}), \
                 patch.object(configuration, "dotenv_values", return_value={"BOT_USERNAME": "file"}):
                importlib.reload(configuration)
                self.assertEqual(configuration.env["BOT_USERNAME"], "process-authoritative")
        finally:
            importlib.reload(configuration)


if __name__ == "__main__":
    unittest.main()
