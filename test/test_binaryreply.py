import pytest

from zaber.serial import BinaryReply

def test_init():
    br = BinaryReply([1, 56, 10502])
    assert(br.device_number == 1)
    assert(br.command_number == 56)
    assert(br.data == 10502)

def test_init_with_message_id():
    br = BinaryReply([2, 44, 21231, 12])
    assert(br.device_number == 2)
    assert(br.command_number == 44)
    assert(br.data == 21231)
    assert(br.message_id == 12)

def test_message_id_is_None():
    br = BinaryReply([3, 32, 0])
    assert(br.message_id == None)

def test_parsing():
    br = BinaryReply(b"\x01\xFF\x03\x00\x00\x00")
    assert(br.device_number == 1)
    assert(br.command_number == 0xFF == 255)
    assert(br.data == 3)

def test_parsing_with_message_id():
    br = BinaryReply(b"\x01\x02\x03\x04\x05\x06", message_id=True)
    assert(br.device_number == 1)
    assert(br.command_number == 2)
    assert(br.data == 3 | (4 << 8) | (5 << 16) == 328707)
    assert(br.message_id == 6)

def test_parsing_without_message_id():
    br = BinaryReply(b"\x01\x02\x03\x04\x05\x06", message_id=False)
    assert(br.device_number == 1)
    assert(br.command_number == 2)
    assert(br.data == 100992003 == 3 | (4 << 8) | (5 << 16) | (6 << 24) )
    assert(br.message_id == None)

def test_dict_will_raise_typeerror():
    br = BinaryReply([1, 2, 3])
    br = BinaryReply(b"\x01\x02\x03\x04\x05\x06")
    with pytest.raises(TypeError):
        br = BinaryReply({
            'device number': 1,
            'command number': 2,
            'data': 3}) # This should fail.


