import unittest

from kik_unofficial.connection_policy import validate_endpoint, retry_delay
from kik_unofficial.device_configuration import (
    kik_version_info, validate_kik_version_info
)


class EndpointTests(unittest.TestCase):
    def test_endpoint(self):
        self.assertEqual(validate_endpoint("TaLk170an.Kik.Com"), ("talk170an.kik.com", 5223))
        for host in ("localhost", "talk.kik.com.evil.test", "https://talk.kik.com",
                     "127.0.0.1", "", "talk.kik.com/path"):
            with self.subTest(host=host), self.assertRaises(ValueError):
                validate_endpoint(host)
        with self.assertRaises(ValueError):
            validate_endpoint("talk.kik.com", True)

    def test_retry_and_server_backoff(self):
        self.assertEqual([retry_delay(n) for n in range(1, 6)], [2, 4, 8, 16, 30])
        self.assertEqual(retry_delay(1, server_backoff=120), 120)
        with self.assertRaises(ValueError):
            retry_delay(0)

    def test_profile_is_well_formed_but_not_attested(self):
        self.assertEqual(validate_kik_version_info(kik_version_info)["kik_version"], "17.0.0.31357")
        with self.assertRaises(ValueError):
            validate_kik_version_info({
                "kik_version": "17.10.2.33986",
                "classes_dex_sha1_digest": "CX8tWbokXf1qnltjpuNcHCE7NYUgb0BZjNmJrAWWE7o="
            })
        with self.assertRaises(TypeError):
            kik_version_info["kik_version"] = "17.10.2.33986"


if __name__ == "__main__":
    unittest.main()
