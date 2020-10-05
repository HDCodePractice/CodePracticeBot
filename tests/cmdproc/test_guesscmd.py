from cmdproc.guesscmd import guess_start
import pytest
from cmdproc import guesscmd
from tests.conftest import make_command_update

def test_start(monkeypatch):
    def reply_text(*args, **kwargs):
        assert "猜大小 Noah&hdcola" in args[0]
        assert kwargs['reply_markup'] == guesscmd.init_replay_markup(guesscmd.start_buttons)
    
    update = make_command_update("/guess")
    monkeypatch.setattr(update.message, 'reply_text', reply_text)
    guesscmd.guess_start(update,None)
