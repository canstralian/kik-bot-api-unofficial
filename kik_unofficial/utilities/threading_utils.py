"""Bounded, ordered callback execution to avoid unbounded thread creation."""
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from threading import BoundedSemaphore

_LOG = logging.getLogger(__name__)
_POOL = ThreadPoolExecutor(max_workers=1, thread_name_prefix="KikCallback")
_SLOTS = BoundedSemaphore(64)


def run_in_new_thread(fn):
    """Queue callbacks in submission order, returning a concurrent.futures.Future.

    Compatibility note: legacy callers received threading.Thread. Call
    Future.result() if completion or error reporting is needed.
    """
    @wraps(fn)
    def run(*args, **kwargs):
        if not _SLOTS.acquire(blocking=False):
            raise RuntimeError("Kik callback queue saturated")

        def invoke():
            try:
                return fn(*args, **kwargs)
            finally:
                _SLOTS.release()

        try:
            future = _POOL.submit(invoke)
        except Exception:
            _SLOTS.release()
            raise

        def report_failure(done):
            if done.cancelled():
                _SLOTS.release()
                return
            failure = done.exception()
            if failure is not None:
                _LOG.error("Callback failed: %s", type(failure).__name__)

        future.add_done_callback(report_failure)
        return future

    run.thread_decorated = True
    return run
