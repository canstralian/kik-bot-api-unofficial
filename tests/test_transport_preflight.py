import socket
import ssl
import unittest
from unittest.mock import Mock, patch

from kik_unofficial.transport_preflight import probe, run


class PreflightTests(unittest.TestCase):
    def test_invalid_host_never_starts_network(self):
        with patch("kik_unofficial.transport_preflight.multiprocessing.get_context") as ctx:
            with self.assertRaises(ValueError):
                run("kik.com.attacker.test")
            ctx.assert_not_called()

    def test_dns_failure_has_no_tls_or_exception_text(self):
        events = []
        with patch("socket.getaddrinfo", side_effect=socket.gaierror("PRIVATE")), \
                patch("ssl.create_default_context") as tls:
            probe("talk1700an.kik.com", events.append)
        self.assertEqual(events, [{"stage": "dns", "status": "failed", "category": "dns"}])
        tls.assert_not_called()

    def test_certificate_failure_is_not_success(self):
        events = []
        raw = Mock()
        raw.__enter__ = Mock(return_value=raw)
        raw.__exit__ = Mock(return_value=False)
        context = Mock()
        context.wrap_socket.side_effect = ssl.SSLCertVerificationError("PRIVATE")
        with patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("192.0.2.1", 5223))]), \
                patch("socket.socket", return_value=raw), \
                patch("ssl.create_default_context", return_value=context):
            probe("talk1700an.kik.com", events.append)
        self.assertEqual(events[-1], {"stage": "tls", "status": "failed", "category": "certificate"})
        context.wrap_socket.assert_called_once_with(raw, server_hostname="talk1700an.kik.com")
        raw.connect.assert_called_once()

    def test_tls_success_sends_no_application_data(self):
        events = []
        raw = Mock()
        raw.__enter__ = Mock(return_value=raw)
        raw.__exit__ = Mock(return_value=False)
        tls = Mock()
        tls.version.return_value = "TLSv1.3"
        tls.__enter__ = Mock(return_value=tls)
        tls.__exit__ = Mock(return_value=False)
        context = Mock()
        context.wrap_socket.return_value = tls
        with patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("192.0.2.1", 5223))]), \
                patch("socket.socket", return_value=raw), \
                patch("ssl.create_default_context", return_value=context):
            probe("talk1700an.kik.com", events.append)
        self.assertEqual([e["stage"] for e in events], ["dns", "tcp", "tls"])
        self.assertTrue(all(e["status"] == "passed" for e in events))
        tls.send.assert_not_called()
        tls.sendall.assert_not_called()
