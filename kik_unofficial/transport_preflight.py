"""Opt-in DNS/TLS evidence only: no credentials, XMPP, login or messages."""
import argparse
from datetime import datetime, timezone
import json
import multiprocessing
import socket
import ssl

from kik_unofficial.connection_policy import validate_endpoint
from kik_unofficial.device_configuration import kik_version_info


def probe(host, report):
    """Emit only fixed categories; never serialize exception text or payloads."""
    stage = "dns"
    try:
        addresses = socket.getaddrinfo(host, 5223, type=socket.SOCK_STREAM)
        if not addresses:
            report({"stage": stage, "status": "failed", "category": "empty_dns"})
            return
        report({"stage": stage, "status": "passed"})
        # One address, one attempt. No scan, fallback hostname or automatic retry.
        family, socktype, protocol, _, address = addresses[0]
        stage = "tcp"
        with socket.socket(family, socktype, protocol) as raw:
            raw.settimeout(10)
            raw.connect(address)
            report({"stage": stage, "status": "passed"})
            stage = "tls"
            with ssl.create_default_context().wrap_socket(raw, server_hostname=host) as tls:
                report({"stage": stage, "status": "passed", "protocol": tls.version()})
    except socket.gaierror:
        report({"stage": stage, "status": "failed", "category": "dns"})
    except ssl.SSLCertVerificationError:
        report({"stage": stage, "status": "failed", "category": "certificate"})
    except ssl.SSLError:
        report({"stage": stage, "status": "failed", "category": "tls"})
    except TimeoutError:
        report({"stage": stage, "status": "failed", "category": "timeout"})
    except OSError:
        report({"stage": stage, "status": "failed", "category": "network"})


def _worker(host, pipe):
    try:
        probe(host, pipe.send)
    finally:
        pipe.close()


def run(host, timeout=30):
    host, _ = validate_endpoint(host)
    if isinstance(timeout, bool) or not 1 <= timeout <= 60:
        raise ValueError("timeout must be between 1 and 60 seconds")
    ctx = multiprocessing.get_context("spawn")
    receiver, sender = ctx.Pipe(duplex=False)
    child = ctx.Process(target=_worker, args=(host, sender))
    events = []
    child.start()
    sender.close()
    child.join(timeout)
    timed_out = child.is_alive()
    if timed_out:
        child.terminate()
        child.join(2)
        if child.is_alive():
            child.kill()
            child.join(2)
    while receiver.poll():
        try:
            events.append(receiver.recv())
        except EOFError:
            break
    receiver.close()
    if timed_out or child.exitcode != 0:
        events.append({"stage": "preflight", "status": "failed",
                       "category": "deadline" if timed_out else "worker_failure"})
    return {"schema_version": 1, "utc": datetime.now(timezone.utc).isoformat(),
            "host": host, "port": 5223, "events": events,
            "authentication": "NOT_ATTEMPTED", "group_roundtrip": "NOT_ATTEMPTED"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-network", action="store_true", required=True,
                        help="Explicitly allow one DNS/TCP/TLS attempt")
    parser.add_argument("--host", help="Independently established Kik-owned endpoint only")
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()
    major, minor, *_ = kik_version_info["kik_version"].split(".")
    host = args.host or f"talk{major}{minor}0an.kik.com"
    try:
        result = run(host, args.timeout)
    except ValueError:
        parser.error("invalid host or timeout; require *.kik.com and 1–60 seconds")
    print(json.dumps(result, indent=2))
    return 0 if any(e["stage"] == "tls" and e["status"] == "passed"
                    for e in result["events"]) and not any(
                        e["status"] == "failed" for e in result["events"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
