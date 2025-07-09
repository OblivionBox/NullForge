import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core import shred_file, zip_and_shred_folder


def test_shred_file(tmp_path):
    tmp_file = tmp_path / "dummy.txt"
    tmp_file.write_text("secret")

    assert tmp_file.exists()
    shred_file(str(tmp_file), passes=2)

    assert not tmp_file.exists()


def test_zip_and_shred_folder(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()
    file1 = folder / "file.txt"
    file1.write_text("data")

    assert folder.exists()
    zip_and_shred_folder(str(folder), passes=1)

    # After shredding, the folder should no longer exist
    assert not folder.exists()
