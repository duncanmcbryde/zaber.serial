import pytest

from zaber.serial import AsciiReply

def test_reply_parsing():
    a = AsciiReply("@01 0 OK IDLE -- 0\r\n")
    assert(a.message_type == '@')
    assert(a.device_address == 1)
    assert(a.axis_number == 0)
    assert(a.reply_flag == "OK")
    assert(a.device_status == "IDLE")
    assert(a.warning_flag == "--")
    assert(a.data == "0")

def test_info_parsing():
    a = AsciiReply("#01 0 Visit www.zaber.com for instruction manuals.\r\n")
    assert(a.message_type == '#')
    assert(a.device_address == 1)
    assert(a.axis_number == 0)
    assert(a.data == "Visit www.zaber.com for instruction manuals.")

def test_alert_parsing():
    a = AsciiReply("!01 0 IDLE --\r\n")
    assert(a.message_type == '!')
    assert(a.device_address == 1)
    assert(a.axis_number == 0)
    assert(a.device_status == "IDLE")
    assert(a.warning_flag == "--")
 
def test_message_ids():
    a = AsciiReply("@04 2 12 OK IDLE -- 123\r\n")
    assert(a.message_id == 12)
    assert(a.message_type == '@')
    assert(a.device_address == 4)
    assert(a.axis_number == 2)
    assert(a.reply_flag == "OK")
    assert(a.device_status == "IDLE")
    assert(a.warning_flag == "--")
    assert(a.data == "123")
    
    b = AsciiReply("#03 0 13 Visit www.zaber.com for instruction manuals.\r\n")
    assert(b.message_type == '#')
    assert(b.device_address == 3)
    assert(b.axis_number == 0)
    assert(b.message_id == 13)
    assert(b.data == "Visit www.zaber.com for instruction manuals.")

def test_invalid_string_raises_exception():
    with pytest.raises(ValueError):
        AsciiReply("%33 A OK I AM A BANANA\r\n")
    with pytest.raises(ValueError):
        AsciiReply("4")
    with pytest.raises(ValueError):
        AsciiReply("#BD 4 !! \n")
    with pytest.raises(ValueError):
        AsciiReply("@01 0 OK IDLE --\r\n")
    with pytest.raises(ValueError):
        AsciiReply("@01 0 OK IDLE -- \r\n")

def test_encoding_strings():
    reply_string = "@01 0 OK IDLE -- 0\r\n"
    a = AsciiReply(reply_string)
    assert(a.encode() == reply_string)

def test_encode_with_message_id():
    repstr = "@01 0 12 OK IDLE -- 0\r\n"
    a = AsciiReply(repstr)
    assert(a.encode() == repstr)

def test_encode_with_checksum():
    repstr = "@01 0 OK IDLE -- 0:8D\r\n"
    a = AsciiReply(repstr)
    assert(a.encode() == repstr)

def test_encode_with_single_digit_checksum():
    repstr = "@01 0 OK IDLE -- 7z:0C\r\n"
    a = AsciiReply(repstr)
    assert(a.encode() == repstr)

def test_bad_checksum_raises_exception():
    repstr = "@01 0 OK IDLE -- 0:GG\r\n"
    with pytest.raises(ValueError):
        a = AsciiReply(repstr)
