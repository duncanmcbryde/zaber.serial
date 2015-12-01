from zaber.serial import BinaryCommand, BinaryDevice, BinaryReply, UnexpectedReplyError

import pytest, struct, threading

@pytest.fixture(scope="module")
def device(binaryserial):
    return BinaryDevice(binaryserial, 1)

def test_constructor(binaryserial):
    bd1 = BinaryDevice(binaryserial, 1)
    bd2 = BinaryDevice(binaryserial, 2)
    assert(bd1.number == 1)
    assert(bd2.number == 2)
    assert(bd1.port == bd2.port == binaryserial)

def test_send(device, fake):
    t = threading.Thread(target = device.send, args = (1, 2, 3))
    t.start()
    fake.expect(pack(device.number, 1, 2, 3))
    fake.send(pack(device.number, 1, 44, 3))
    t.join()

def test_send_overwrites_device_number(device, fake):
    t = threading.Thread(target = device.send,
            args = (BinaryCommand(device.number + 1, 1, 2), ))
    t.start()
    fake.expect(pack(device.number, 1, 2))
    fake.send(pack(device.number, 1, 0))
    t.join()

def test_send_complains_on_unexpected_response(device, fake):
    def device_send_with_pytest_raises():
        with pytest.raises(UnexpectedReplyError):
            device.send(2, 3, 4)
    t = threading.Thread(target = device_send_with_pytest_raises)
    t.start()
    fake.expect(pack(device.number, 2, 3, 4))
    fake.send(pack(device.number + 1, 2, 3, 4))
    t.join()

def test_send_complains_if_message_id_does_not_match(device, fake):
    def device_send_with_pytest_raises():
        with pytest.raises(UnexpectedReplyError):
            device.send(3, 3, 3)
    t = threading.Thread(target = device_send_with_pytest_raises)
    t.start()
    fake.expect(pack(device.number, 3, 3, 3))
    fake.send(pack(device.number, 3, 3, 45))
    t.join()

def test_home(device, fake):
    t = threading.Thread(target = device.home)
    t.start()
    fake.expect(pack(device.number, 1, 0))
    fake.send(pack(device.number, 1, 0))
    t.join()

def test_moveabs(device, fake):
    t = threading.Thread(target = device.move_abs, args = (1000, ))
    t.start()
    fake.expect(pack(device.number, 20, 1000))
    fake.send(pack(device.number, 20 ,1000))
    t.join()

def test_moverel(device, fake):
    t = threading.Thread(target = device.move_rel, args = (1000, ))
    t.start()
    fake.expect(pack(device.number, 21, 1000))
    fake.send(pack(device.number, 21, 2000))
    t.join()

def test_movevel(device, fake):
    t = threading.Thread(target = device.move_vel, args = (200, ))
    t.start()
    fake.expect(pack(device.number, 22, 200))
    fake.send(pack(device.number, 22, 200))
    t.join()

def test_stop(device, fake):
    t = threading.Thread(target = device.stop)
    t.start()
    fake.expect(pack(device.number, 23, 0))
    fake.send(pack(device.number, 23, 23134))
    t.join()

def test_getstatus(device, fake):
    def control_fake():
        fake.expect(pack(device.number, 54, 0))
        fake.send(pack(device.number, 54, 0))
    t = threading.Thread(target = control_fake)
    t.start()
    status = device.get_status()
    t.join()
    assert(status == 0)

def pack(device, command, data = 0, message_id = None):
    packed = struct.pack("<2Bl", device, command, data)
    if message_id is not None:
        packed = packed[:5] + struct.pack("B", message_id)
    return packed

