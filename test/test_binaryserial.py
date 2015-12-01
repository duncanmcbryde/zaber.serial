import pytest
import struct

from zaber.serial import BinaryCommand, BinarySerial

def test_write(binaryserial, fake):
    cmd = BinaryCommand(1, 54)
    binaryserial.write(cmd)
    fake.expect(cmd.encode())

def test_read(binaryserial, fake):
    fake.send(1, 54, 0)
    rep = binaryserial.read().encode().decode()
    assert(rep[0] == '\x01')
    assert(rep[1] == '\x36')
    assert(rep[2] == rep[3] == rep[4] == rep[5] == '\x00')

def test_write_multiple_arguments(binaryserial, fake):
    binaryserial.write(1, 2, 3)
    fake.expect(pack(1, 2, 3))

def test_write_multi_args_with_message_id(binaryserial, fake):
    binaryserial.write(1, 2, 3, 4)
    fake.expect(pack(1, 2, 3, 4))

def test_write_complains_when_passed_wrong_type(binaryserial):
    with pytest.raises(TypeError):
        binaryserial.write({"aaaa": "bbb"})
    with pytest.raises(TypeError):
        binaryserial.write(binaryserial)

def test_constructor_fails_when_not_passed_a_string():
    with pytest.raises(TypeError):
        BinarySerial(1)

def test_read_reads_message_id(binaryserial, fake):
    fake.send(BinaryCommand(1, 55, 34, 22))
    reply = binaryserial.read(message_id = True)
    assert(reply.device_number == 1)
    assert(reply.command_number == 55)
    assert(reply.data == 34)
    assert(reply.message_id == 22)

def test_read_truncates_data_when_using_message_id(binaryserial, fake):
    fake.send(BinaryCommand(3, 55, -1, 1))
    reply = binaryserial.read(True)
    assert(reply.device_number == 3)
    assert(reply.command_number == 55)
    assert(reply.data == 16777215)
    assert(reply.message_id == 1)

def pack(device, command, data = 0, message_id = None):
    packed = struct.pack("<2Bl", device, command, data)
    if message_id is not None:
        packed = packed[:5] + struct.pack("B", message_id)
    return packed
