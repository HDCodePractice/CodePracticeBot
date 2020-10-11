#!/usr/bin/env python3

import pytest

from data import coins

def test_check():
    coins.checkcoins(1,1,"hd")
    assert coins.coins[1]=={1:{'name':'hd',"coins":0}}
    assert len(coins.coins) == 1
    coins.checkcoins(1,2,"hd")
    assert coins.coins[1]=={1:{'name':'hd',"coins":0},2:{'name':'hd',"coins":0}}
    assert len(coins.coins) == 1
    coins.checkcoins(1,2,"hdd")
    assert coins.coins[1]=={1:{'name':'hd',"coins":0},2:{'name':'hdd',"coins":0}}
    assert len(coins.coins) == 1


def test_checkin():
    c1 = coins.checkin(1,1,"hd")
    assert coins.coins[1][1]['coins'] == c1
    c2 = coins.checkin(1,1,"hd")
    assert coins.coins[1][1]['coins'] == c1 + c2