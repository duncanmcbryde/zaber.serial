import pytest
import threading
import time

from zaber.serial import AsciiSerial, AsciiCommand, AsciiReply, BinaryCommand, TimeoutError

def test_write_command(asciiserial, fake):
    a = AsciiCommand("/1 echo TEST\r\n")
    asciiserial.write(a)
    asciiserial.write("/1 echo TEST\r\n")
    asciiserial.write("1 echo TEST")
    fake.expect("/1 0 echo TEST\r\n")
    fake.expect("/1 0 echo TEST\r\n")
    fake.expect("/1 0 echo TEST\r\n")

def test_write_empty_string(asciiserial, fake):
    asciiserial.write("")
    fake.expect("/0 0\s*\r\n")
    asciiserial.write("1")
    fake.expect("/1 0\r\n")
    asciiserial.write("2 2")
    fake.expect("/2 2\r\n")

def test_write_string(asciiserial, fake):
    asciiserial.write("home")
    fake.expect("/0 0 home\r\n")
    asciiserial.write("1 move abs 2000")
    fake.expect("/1 0 move abs 2000\r\n")
    asciiserial.write("5 tools setcomm 9600 1")
    fake.expect("/5 0 tools setcomm 9600 1\r\n")
    asciiserial.write("3 2 move rel -200")
    fake.expect("/3 2 move rel -200\r\n")

def test_write_binary_bytes(asciiserial, fake):
    asciiserial.write(b"1 home\r\n")
    fake.expect("/1 0 home\r\n")

def test_read_returns_command(asciiserial, fake):
    fake.send("@01 0 OK IDLE -- 0\r\n")
    reply = asciiserial.read()
    assert(isinstance(reply, AsciiReply))
    assert(reply.device_address == 1)
    assert(reply.axis_number == 0)
    assert(reply.reply_flag == 'OK')
    assert(reply.device_status == 'IDLE')
    assert(reply.warning_flag == '--')
    assert(reply.data == '0')

def test_read_complains_on_malformed_input(asciiserial, fake):
    fake.send("bad input\r\n")
    with pytest.raises(ValueError):
        asciiserial.read()

def test_can_set_timeout(asciiserial, fake):
    asciiserial.timeout += 10
    t = threading.Thread(target = asciiserial.read)
    t.start()

    # If the timeout hasn't been properly set, 
    # this sleep will trigger a TimeoutError.
    time.sleep(asciiserial.timeout - 9)
    fake.send("@01 0 OK IDLE -- 0\r\n")
    t.join()
    asciiserial.timeout -= 10 

def test_can_change_baudrate(asciiserial):
    # If _ser gets renamed, then this test will need to be changed too.
    underlying_serial = asciiserial._ser
    for rate in (9600, 19200, 38400, 57600, 115200):
        asciiserial.baudrate = rate 
        assert(underlying_serial.baudrate == rate)

def test_sending_BinaryCommand_raises_error(asciiserial):
    with pytest.raises(TypeError):
        asciiserial.write(BinaryCommand(1, 55, 23423))

def test_read_times_out_with_empty_buffer(asciiserial):
    with pytest.raises(TimeoutError):
        asciiserial.read()

def test_close_and_reopen(asciiserial):
    asciiserial.close()
    asciiserial.open()
