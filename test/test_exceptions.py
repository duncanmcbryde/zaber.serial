import pytest
import threading

from zaber.serial import UnexpectedReplyError, TimeoutError, AsciiReply, BinaryReply, AsciiCommand, AsciiDevice

def test_unexpectedreplyerror_accepts_reply():
    rep = AsciiReply("@01 0 OK IDLE -- 0\r\n")
    ex = UnexpectedReplyError("Oh no!", rep)
    assert(ex.args == ("Oh no!", ))
    assert(ex.reply == rep)

def test_message_available_from_raises():
    try:
        raise UnexpectedReplyError("TEST", BinaryReply([1, 2, 3]))
    except UnexpectedReplyError as ex:
        assert(ex.args)
        assert(ex.reply)
        
def test_unexpectedreplyerror_contains_unexpected_reply(fake, asciiserial):
    def test_write_and_check_exception():
        cmd = AsciiCommand("1 1 move abs 200")
        device = AsciiDevice(asciiserial, 1)
        rep = None
        try:
            device.send(cmd)
        except UnexpectedReplyError as ure:
            rep = ure.reply
        assert(rep != None)
    t = threading.Thread(target = test_write_and_check_exception)
    t.start()
    fake.expect("/1 1 move abs 200\r\n")
    fake.send("@02 2 OK IDLE -- 0\r\n")
    t.join()
