import pytest
import threading

from zaber.serial import AsciiDevice, AsciiCommand

@pytest.fixture
def device(asciiserial):
    return AsciiDevice(asciiserial, 1)

def test_constructor(asciiserial):
    ad = AsciiDevice(asciiserial, 1)
    assert(ad.port == asciiserial)
    assert(ad.address == 1)

def test_send_command(device, fake):
    t = threading.Thread(target = device.send, args = (AsciiCommand("home"), ))
    t.start()
    fake.expect("/1 0 home\r\n")
    fake.send("@01 0 OK BUSY WR 0\r\n")
    t.join()

def test_send_command_with_device_number(device, fake):
    t = threading.Thread(target = device.send, args = (AsciiCommand("1 home"), ))
    t.start()
    fake.expect("/1 0 home\r\n")
    fake.send("@01 0 OK BUSY -- 0\r\n")
    t.join()

def test_send_str(device, fake):
    t = threading.Thread(target = device.send, args = ("home", ))
    t.start()
    fake.expect("/1 0 home\r\n")
    fake.send("@01 0 OK BUSY -- 0\r\n")
    t.join()

def test_send_str_with_device_number(device, fake):
    t = threading.Thread(target = device.send, args = ("1 move vel 1000", ))
    t.start()
    fake.expect("/1 0 move vel 1000\r\n")
    fake.send("@01 0 OK BUSY -- 0\r\n")
    t.join()

def test_send_str_with_axis_number(device, fake):
    t = threading.Thread(target = device.send, args = ("1 1 move rel -1000", ))
    t.start()
    fake.expect("/1 1 move rel -1000\r\n")
    fake.send("@01 1 OK BUSY -- 0\r\n")
    t.join()

def test_send_str_with_multiple_arguments(device, fake):
    t = threading.Thread(target = device.send, args=("/tools setcomm 9600 1\r\n", ))
    t.start()
    fake.expect("/1 0 tools setcomm 9600 1\r\n")
    fake.send("@01 0 OK IDLE NU 0")
    t.join()

def test_home(device, fake):
    t = threading.Thread(target = device.home)
    t.start()
    fake.expect("/1 0 home\r\n")
    fake.send("@01 0 OK BUSY WR 0\r\n")
    fake.expect("/1 0\r\n")
    fake.send("@01 0 OK BUSY WR 0\r\n")
    fake.expect("/1 0\r\n")
    fake.send("@01 0 OK IDLE -- 0\r\n")
    t.join()

def test_move_abs(device, fake):
    t = threading.Thread(target = device.move_abs, args = (1000, ))
    t.start()
    fake.expect("/1 0 move abs 1000\r\n")
    fake.send("@01 0 OK BUSY -- 0\r\n")
    fake.expect("/1 0\r\n")
    fake.send("@01 0 OK BUSY -- 0\r\n")
    fake.expect("/1 0\r\n")
    fake.send("@01 0 OK IDLE -- 0\r\n")
    t.join()

def test_move_rel(device, fake):
    t = threading.Thread(target = device.move_rel, args = (1322, ))
    t.start()
    fake.expect("/1 0 move rel 1322\r\n")
    fake.send("@01 0 OK BUSY -- 0\r\n")
    fake.expect("/1 0\r\n")
    fake.send("@01 0 OK IDLE -- 0\r\n")
    t.join()

def test_move_vel(device, fake):
    t = threading.Thread(target = device.move_vel, args = (3243, ))
    t.start()
    fake.expect("/1 0 move vel 3243\r\n")
    fake.send("@01 0 OK BUSY -- 0\r\n")
    t.join()

def test_stop(device, fake):
    t = threading.Thread(target = device.stop)
    t.start()
    fake.expect("/1 0 stop\r\n")
    fake.send("@01 0 OK BUSY NI 0\r\n")
    fake.expect("/1 0\r\n")
    fake.send("@01 0 OK IDLE NI 0\r\n")
    t.join()

def test_get_status(device, fake):
    t = threading.Thread(target = device.get_status)
    t.start()
    fake.expect("/1 0\r\n")
    fake.send("@01 0 OK BUSY -- 0\r\n")
    t.join()
