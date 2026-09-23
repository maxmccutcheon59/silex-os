import pytest

from silex.auth import Role, require
from silex.channel import Channel
from silex.errors import SilexError
from silex.server import serve
from silex.writ import Issuer, load_issuer_secret


def test_operator_cannot_revoke():
    with pytest.raises(SilexError, match="cannot call"):
        require("/api/revoke", Role.OPERATOR)


def test_supervisor_can_revoke():
    require("/api/revoke", Role.SUPERVISOR)


def test_admin_can_reset():
    require("/api/reset", Role.ADMIN)


def test_channel_rejects_bad_ticket():
    ch = Channel(secret="x" * 32)
    ticket = ch.ticket("cell-1", "pick", "writ-1")
    ch.accept("cell-1", "pick", "writ-1", ticket)
    with pytest.raises(SilexError, match="rejected"):
        ch.accept("cell-1", "pick", "writ-1", "00" * 32)


def test_short_issuer_secret_rejected():
    with pytest.raises(SilexError):
        load_issuer_secret("short")


def test_remote_requires_console_token(monkeypatch):
    monkeypatch.setenv("SILEX_ALLOW_REMOTE", "1")
    monkeypatch.delenv("SILEX_CONSOLE_TOKEN", raising=False)
    with pytest.raises(SilexError, match="CONSOLE_TOKEN"):
        serve("0.0.0.0", 8080)
