from unittest.mock import patch
import pytest
import sys

from ak_jiosaavn.slack import getpwd

@pytest.fixture()
def mock_keyring():
    with patch.object(sys, "platform", "win32"):
        with patch("keyring.get_password", return_value="test123"):
            with patch("keyring.set_password", return_value=None):
                yield

@pytest.fixture()
def mock_getpass():
    with patch.object(sys, "platform", "linux"):
        with patch("getpass.getpass", return_value="test123"):
            yield

def test_getpwd(mock_keyring, mock_getpass):
    # Test getpwd with Windows
    assert getpwd("Slack-pythonbot", "user1") == "test123"

    # Test getpwd with Linux
    assert getpwd("Slack-pythonbot", "user1") == "test123"
