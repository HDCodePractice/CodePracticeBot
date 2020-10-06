from cmdproc.guesscmd import guess_start
import pytest
from cmdproc import guesscmd
from tests.conftest import make_callback_query_update, make_command_update

def test_start(monkeypatch):
    # 测试发出/start命令
    def reply_text(*args, **kwargs):
        assert "猜大小 Noah&hdcola" in args[0]
        assert kwargs['reply_markup'] == guesscmd.init_replay_markup(guesscmd.start_buttons)
    
    update = make_command_update("/guess")
    monkeypatch.setattr(update.message, 'reply_text', reply_text)
    guesscmd.guess_start(update,None)
    # 测试点add按钮
    def guess_start_add_answer(*args, **kwargs):
        # print(f"args:{args}\nkwargs:{kwargs}\n\n")
        assert args[0] == "加入游戏成功！Join the game successfully!"

    def guess_start_add_edit_message_text(*args, **kwargs):
        # print(f"args:{args}\nkwargs:{kwargs}\n\n")
        assert "玩家列表:\nfirst_name" in kwargs['text']

    update = make_callback_query_update("","guess_start:add")
    monkeypatch.setattr(update.callback_query, 'answer', guess_start_add_answer)
    monkeypatch.setattr(update.callback_query, 'edit_message_text', guess_start_add_edit_message_text)
    guesscmd.guess_start_callback(update,None)
