import os
import unittest
from types import SimpleNamespace
from unittest import mock

import downloader


class FakeTqdm:
    def __init__(self, total=0, unit=None, unit_scale=None):
        self.total = total
        self.n = 0

    def update(self, amount):
        self.n += amount

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class DownloaderTests(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        self.temp_dir = os.path.join(self.cwd, "test_tmp")
        os.makedirs(self.temp_dir, exist_ok=True)
        os.chdir(self.temp_dir)

    def tearDown(self):
        os.chdir(self.cwd)
        for root, _, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def test_download_writes_file_and_returns_path(self):
        response = SimpleNamespace(
            headers={"content-length": "6"},
            iter_content=lambda block_size: [b"abc", b"def"],
        )

        with mock.patch("downloader.requests.get", return_value=response), mock.patch(
            "downloader.tqdm", FakeTqdm
        ):
            filepath = downloader.download("https://example.com/file.txt")

        self.assertTrue(os.path.exists(filepath))
        with open(filepath, "rb") as handle:
            self.assertEqual(handle.read(), b"abcdef")

    def test_download_handles_missing_content_length(self):
        response = SimpleNamespace(
            headers={},
            iter_content=lambda block_size: [b"chunk"],
        )

        with mock.patch("downloader.requests.get", return_value=response), mock.patch(
            "downloader.tqdm", FakeTqdm
        ):
            filepath = downloader.download("https://example.com/asset.bin")

        self.assertTrue(os.path.exists(filepath))
