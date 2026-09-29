import socket
import unittest
from threading import Event
from types import SimpleNamespace
from unittest.mock import Mock, patch

from bs4 import BeautifulSoup
from kik_unofficial.client import KikClient, KikConnection
from kik_unofficial.connection_policy import KikDisconnectedError, ConnectionState


class SupervisorTests(unittest.TestCase):
    @staticmethod
    def make_client():
        client = object.__new__(KikClient)
        client.kik_connection_thread = Mock()
        client.is_permanent_disconnection = False
        client._shutdown_event = Mock()
        client._shutdown_event.wait.return_value = False
        client._shutdown_event.is_set.return_value = False
        client._server_backoff_seconds = 0
        client._last_connection_failure = "dns"
        client._reached_auth = False
        client._planned_turnover = False
        client.connection_state = ConnectionState.STOPPED
        client.log = Mock()
        client._connect = Mock()
        return client

    def test_exact_retry_budget_without_recursive_spawn(self):
        client = self.make_client()
        client.wait_for_messages(max_retries=2)
        self.assertEqual(client.kik_connection_thread.join.call_count, 3)
        self.assertEqual(client._connect.call_count, 2)
        self.assertTrue(client.is_permanent_disconnection)
        client._shutdown_event.set.assert_called_once()

    def test_planned_authentication_turnover_does_not_consume_retry(self):
        client = self.make_client()

        def complete_attempt():
            if client.kik_connection_thread.join.call_count == 1:
                client._planned_turnover = True
            else:
                client.is_permanent_disconnection = True

        client.kik_connection_thread.join.side_effect = complete_attempt
        client.wait_for_messages(max_retries=0)
        client._connect.assert_called_once()
        client._shutdown_event.wait.assert_not_called()

    def test_authenticated_session_resets_failure_budget(self):
        client = self.make_client()
        # A successful authenticated session between failed attempts resets
        # consecutive failures; a cumulative exit counter would terminate sooner.
        def complete_attempt():
            n = client.kik_connection_thread.join.call_count
            client._reached_auth = n == 2

        client.kik_connection_thread.join.side_effect = complete_attempt
        client.wait_for_messages(max_retries=1)
        self.assertEqual(client.kik_connection_thread.join.call_count, 4)
        self.assertEqual(client._connect.call_count, 3)
        self.assertTrue(client.is_permanent_disconnection)

    def test_server_backoff_is_honoured(self):
        client = self.make_client()
        client._server_backoff_seconds = 67
        client.wait_for_messages(max_retries=1)
        client._shutdown_event.wait.assert_called_once_with(67)

    def test_permanent_rejection_never_retries(self):
        client = self.make_client()
        client.is_permanent_disconnection = True
        client.wait_for_messages(max_retries=5)
        client._connect.assert_not_called()

    def test_outbound_wait_terminates_after_shutdown(self):
        client = self.make_client()
        client.connected = False
        client.is_permanent_disconnection = True
        client.message_wait_timeout = 1
        with self.assertRaises(KikDisconnectedError):
            client._send_xmpp_element(Mock())

    def test_bad_version_is_terminal(self):
        client = self.make_client()
        client.connected = False
        client.callback = Mock()
        client.kik_node = "sample"
        client.should_login_on_connection = False
        reply = BeautifulSoup('<k ok="0"><badver><msg>unsupported</msg></badver></k>', "xml").k
        client._handle_received_k_element(reply)
        self.assertTrue(client.is_permanent_disconnection)
        self.assertEqual(client._last_connection_failure, "bad_version")
        client._shutdown_event.set.assert_called_once()


class TransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_dns_error_is_classified_not_recursively_retried(self):
        api = SimpleNamespace(host="talk170an.kik.com", port=5223,
                              connect_timeout=1, connected=False, authenticated=False,
                              _auth_deadline=None, _last_connection_failure=None,
                              is_permanent_disconnection=False, log=Mock())
        connection = KikConnection(api)
        with patch("kik_unofficial.client.asyncio.open_connection", side_effect=socket.gaierror(-2, "name lookup")):
            await connection.read_loop()
        self.assertEqual(api._last_connection_failure, "dns")
        self.assertTrue(connection.is_closed)
        self.assertIsNone(connection.writer)

    async def test_no_raw_packet_in_diagnostic_logs(self):
        api = SimpleNamespace(log=Mock())
        connection = KikConnection(api)
        connection.writer = Mock()
        connection.writer.is_closing.return_value = False
        secret = b'<iq><passkey-u>SECRET-DERIVED-VALUE</passkey-u></iq>'
        connection.send_raw_data(secret)
        args = str(api.log.debug.call_args)
        self.assertNotIn("SECRET-DERIVED-VALUE", args)
        connection.writer.write.assert_called_once_with(secret)


if __name__ == "__main__":
    unittest.main()
