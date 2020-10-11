import pytest
from cmdproc import guesscmd
from tests.conftest import make_callback_query_update, make_command_update

def test_gen_end_result():
    assert guesscmd.check_chatid(1) == False
    assert guesscmd.check_chatid(1) == True
    
    
    for i in range(30):
        msg = guesscmd.gen_end_result(1)
        # print(msg)
        assert len(msg.split('+'))==3
        assert len(msg.split('='))==2
        # print(guesscmd.guessResult[1]['histore'])
        assert len(guesscmd.guessResult[1]['histore']) == i + 1 
    
    msg = guesscmd.gen_end_result(1)
    assert len(msg.split('+'))==3
    assert len(msg.split('='))==2
    # print(guesscmd.guessResult[1]['histore'])
    assert len(guesscmd.guessResult[1]['histore']) == 30
    msg = guesscmd.gen_end_result(1)
    assert len(msg.split('+'))==3
    assert len(msg.split('='))==2
    # print(guesscmd.guessResult[1]['histore'])
    assert len(guesscmd.guessResult[1]['histore']) == 30


def test_start(monkeypatch):
    # 测试发出/start命令
    def reply_text(*args, **kwargs):
        assert "猜大小" in args[0]
        assert kwargs['reply_markup'] == guesscmd.init_replay_markup(guesscmd.start_buttons)
    
    update = make_command_update("/guess")
    monkeypatch.setattr(update.message, 'reply_text', reply_text)
    guesscmd.guess_start(update,None)

    # 测试点add按钮
    def guess_start_add_answer(*args, **kwargs):
        # print(f"args:{args}\nkwargs:{kwargs}\n\n")
        nonlocal step
        if step == "start":
            assert args[0] == "加入游戏成功！You joined the game successfully!"
            step = "join"
        elif step == "join":
            assert args[0] == "你已经加入游戏了！You're in the game!"
            step = "playing"
        else:
            assert args[0] == "开局啦"

    def guess_start_add_edit_message_text(*args, **kwargs):
        # print(f"args:{args}\nkwargs:{kwargs}\n\n")
        if step == "playing":
            assert "first_name:🔴未完成" in kwargs['text']
            assert kwargs['reply_markup'] == guesscmd.init_replay_markup(guesscmd.play_buttons)
        else:
            assert kwargs['reply_markup'] == guesscmd.init_replay_markup(guesscmd.start_buttons)
        assert "玩家列表:\nfirst_name" in kwargs['text']

    step = "start"
    addupdate = make_callback_query_update("","guess_start:add")
    monkeypatch.setattr(addupdate.callback_query, 'answer', guess_start_add_answer)
    monkeypatch.setattr(addupdate.callback_query, 'edit_message_text', guess_start_add_edit_message_text)
    # 点第一次add按钮
    guesscmd.guess_start_callback(addupdate,None)
    # 点第二次add按钮
    guesscmd.guess_start_callback(addupdate,None)

    startupdate = make_callback_query_update("","guess_start:start")
    monkeypatch.setattr(startupdate.callback_query, 'answer', guess_start_add_answer)
    monkeypatch.setattr(startupdate.callback_query, 'edit_message_text', guess_start_add_edit_message_text)
    # 点一下start按钮
    guesscmd.guess_start_callback(startupdate,None)

    # 测试点add按钮
    def guess_play_answer(*args, **kwargs):
        # print(f"args:{args}\nkwargs:{kwargs}\n\n")
        nonlocal step
        if step == "d":
            assert args[0] == "你选择了大"
        elif step == "dd":
            assert args[0] == "你已经选择了大"
        elif step == "x":
            assert args[0] == "你选择了小"
        elif step == "xx":
            assert args[0] == "你已经选择了小"
        elif step == "do":
            assert args[0] == "结算结果"

    def guess_play_edit_message_text(*args, **kwargs):
        # print(f"args:{args}\nkwargs:{kwargs}\n\n")
        if step == "d":
            assert "first_name:🔼大" in kwargs['text']
            assert kwargs['reply_markup'] == guesscmd.init_replay_markup(guesscmd.play_buttons)
        elif step == "x":
            assert "first_name:🔽小" in kwargs['text']
            assert kwargs['reply_markup'] == guesscmd.init_replay_markup(guesscmd.play_buttons)
        elif step == "do":
            assert "结算结果" in kwargs['text']
    
    # 大按钮
    dupdate = make_callback_query_update("","guess_play:d")
    monkeypatch.setattr(dupdate.callback_query, 'answer', guess_play_answer)
    monkeypatch.setattr(dupdate.callback_query, 'edit_message_text', guess_play_edit_message_text)
    # 小按钮
    xupdate = make_callback_query_update("","guess_play:x")
    monkeypatch.setattr(xupdate.callback_query, 'answer', guess_play_answer)
    monkeypatch.setattr(xupdate.callback_query, 'edit_message_text', guess_play_edit_message_text)
    # 结算按钮
    doupdate = make_callback_query_update("","guess_play:do")
    monkeypatch.setattr(doupdate.callback_query, 'answer', guess_play_answer)
    monkeypatch.setattr(doupdate.callback_query, 'edit_message_text', guess_play_edit_message_text)
    step="d"
    guesscmd.guess_play_callback(dupdate,None)
    step="dd"
    guesscmd.guess_play_callback(dupdate,None)
    step="x"
    guesscmd.guess_play_callback(xupdate,None)
    step="xx"
    guesscmd.guess_play_callback(xupdate,None)
    step="do"
    guesscmd.guess_play_callback(doupdate,None)

def test_not_choose(monkeypatch):
    def reply_text(*args, **kwargs):
        pass
    
    def guess_answer(*args, **kwargs):
        pass

    def guess_edit_message_text(*args, **kwargs):
        if step == "do":
            assert ":未参与" in kwargs['text']

    # guess_cmd
    guessupdate = make_command_update("/guess")
    monkeypatch.setattr(guessupdate.message, 'reply_text', reply_text)
    # 加入游戏button
    addupdate = make_callback_query_update("","guess_start:add")
    monkeypatch.setattr(addupdate.callback_query, 'answer', guess_answer)
    monkeypatch.setattr(addupdate.callback_query, 'edit_message_text', guess_edit_message_text)
    # 开始button
    startupdate = make_callback_query_update("","guess_start:start")
    monkeypatch.setattr(startupdate.callback_query, 'answer', guess_answer)
    monkeypatch.setattr(startupdate.callback_query, 'edit_message_text', guess_edit_message_text)
    # 大按钮
    dupdate = make_callback_query_update("","guess_play:d")
    monkeypatch.setattr(dupdate.callback_query, 'answer', guess_answer)
    monkeypatch.setattr(dupdate.callback_query, 'edit_message_text', guess_edit_message_text)
    # 小按钮
    xupdate = make_callback_query_update("","guess_play:x")
    monkeypatch.setattr(xupdate.callback_query, 'answer', guess_answer)
    monkeypatch.setattr(xupdate.callback_query, 'edit_message_text', guess_edit_message_text)
    # 结算按钮
    doupdate = make_callback_query_update("","guess_play:do")
    monkeypatch.setattr(doupdate.callback_query, 'answer', guess_answer)
    monkeypatch.setattr(doupdate.callback_query, 'edit_message_text', guess_edit_message_text)

    step = ""
    # 开始
    guesscmd.guess_start(guessupdate,None)
    # 加入游戏
    guesscmd.guess_start_callback(addupdate,None)
    # 开始游戏
    guesscmd.guess_start_callback(startupdate,None)
    # 直接结束
    step = "do"
    guesscmd.guess_play_callback(doupdate,None)