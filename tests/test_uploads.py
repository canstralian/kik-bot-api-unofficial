import unittest
from types import SimpleNamespace
from unittest.mock import patch

from kik_unofficial.datatypes.exceptions import KikUploadError
from kik_unofficial.http_requests import profile_pictures, content


class UploadTests(unittest.TestCase):
    def test_profile_http_200_is_success_without_retry(self):
        response = SimpleNamespace(status_code=200, reason="OK")
        with patch.object(profile_pictures, "get_file_bytes", return_value=b"picture"), \
             patch.object(profile_pictures.requests, "post", return_value=response) as post:
            profile_pictures.picture_upload_thread("https://profilepicsup.kik.com/profilepics", b"picture", {})
            post.assert_called_once()
            self.assertEqual(post.call_args.kwargs["timeout"], profile_pictures.HTTP_TIMEOUT)

    def test_profile_http_error_is_not_success(self):
        response = SimpleNamespace(status_code=503, reason="Unavailable")
        with patch.object(profile_pictures, "get_file_bytes", return_value=b"picture"), \
             patch.object(profile_pictures.requests, "post", return_value=response) as post:
            with self.assertRaises(KikUploadError):
                profile_pictures.picture_upload_thread("https://profilepicsup.kik.com/profilepics", b"picture", {})
            self.assertEqual(post.call_count, 3)

    def test_gallery_rejects_failure_with_timeout(self):
        response = SimpleNamespace(status_code=503, reason="Unavailable")
        with patch.object(content.requests, "put", return_value=response) as put:
            with self.assertRaises(KikUploadError):
                content.content_upload_thread("https://platform.kik.com/content/files/id", b"x", {})
            self.assertEqual(put.call_args.kwargs["timeout"], content.HTTP_TIMEOUT)


if __name__ == "__main__":
    unittest.main()
