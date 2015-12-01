import pytest
from threading import Thread

from zaber.serial import AsciiAxis, AsciiDevice

@pytest.fixture
def device(asciiserial):
    return AsciiDevice(asciiserial, 1)

@pytest.fixture
def axis(device):
    return AsciiAxis(device, 1)

def test_constructor(device):
    a = AsciiAxis(device, 1)
    assert(a.number == 1)
    assert(a.parent is not None)

def test_can_be_constructed_from_asciidevice(device):
    a = device.axis(1)
    b = device.axis(2)
    assert(a.number == 1)
    assert(b.number == 2)

def test_home(axis, fake):
    t = Thread(target = axis.home)
    t.start()
    fake.expect("/1 1 home\r\n")
    fake.send("@01 1 OK BUSY WR 0\r\n")
    fake.expect("/1 1\r\n")
    fake.send("@01 1 OK IDLE -- 0\r\n")
    t.join()

def test_move_abs(axis,fake):
    t = Thread(target = axis.move_abs, args = (10234, ))
    t.start()
    fake.expect("/1 1 move abs 10234\r\n")
    fake.send("@01 1 OK BUSY -- 0\r\n")
    fake.expect("/1 1\r\n")
    fake.send("@01 1 OK IDLE -- 0\r\n")
    t.join()

def test_poll_until_idle_will_continue_polling(axis, fake):
    t = Thread(target = axis.poll_until_idle)
    t.start()
    for i in range(100):
        fake.expect("/1 1\r\n")
        fake.send("@01 1 OK BUSY -- 0\r\n")
    fake.expect("/1 1\r\n")
    fake.send("@01 1 OK IDLE -- 0\r\n")
    t.join()

def test_move_rel(axis, fake):
    t = Thread(target = axis.move_rel, args = (12312, ))
    t.start()
    fake.expect("/1 1 move rel 12312\r\n")
    fake.send("@01 1 OK BUSY -- 0\r\n")
    fake.expect("/1 1\r\n")
    fake.send("@01 1 OK IDLE -- 0\r\n")
    t.join()

def test_move_vel(axis, fake):
    t = Thread(target = axis.move_vel, args = (1005, ))
    t.start()
    fake.expect("/1 1 move vel 1005\r\n")
    fake.send("@01 1 OK BUSY -- 0\r\n")
    t.join()

def test_stop(axis, fake):
    t = Thread(target = axis.stop)
    t.start()
    fake.expect("/1 1 stop\r\n")
    fake.send("@01 1 OK BUSY NI 0\r\n")
    fake.expect("/1 1\r\n")
    fake.send("@01 1 OK IDLE -- 0\r\n")
    t.join()

def test_invalid_axis_number_raises_value_error(device):
    with pytest.raises(ValueError):
        AsciiAxis(device, 10)

def test_get_status(axis, fake):
    def test_return_value_from_get_status():
        assert(axis.get_status() == "IDLE")
        assert(axis.get_status() == "BUSY")
    t = Thread(target = test_return_value_from_get_status)
    t.start()
    fake.expect("/1 1\r\n")
    fake.send("@01 1 OK IDLE -- 0\r\n")
    fake.expect("/1 1\r\n")
    fake.send("@01 1 OK BUSY -- 0\r\n")
    t.join()
