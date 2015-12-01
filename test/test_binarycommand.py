import pytest

from zaber.serial import BinaryCommand

def test_3_argument_constructor():
    bc = BinaryCommand(1, 5, 334)
    assert(bc.device_number == 1)
    assert(bc.command_number == 5)
    assert(bc.data == 334)

def test_message_id_in_4th_arg():
    bc = BinaryCommand(1, 2, 3, 4)
    assert(bc.device_number == 1)
    assert(bc.command_number == 2)
    assert(bc.data == 3)
    assert(bc.message_id == 4)

def test_message_id_is_none():
    bc = BinaryCommand(2, 54, 34)
    assert(bc.device_number == 2)
    assert(bc.command_number == 54)
    assert(bc.data == 34)
    assert(bc.message_id == None)

def test_2_argument_constructor():
    bc = BinaryCommand(1, 0)
    assert(bc.device_number == 1)
    assert(bc.command_number == 0)
    assert(bc.data == 0)
    assert(bc.message_id == None)

def test_no_arguments_throws_typeerror():
    with pytest.raises(TypeError):
        BinaryCommand()

def test_negative_device_or_command_number_raises_valueerror():
    with pytest.raises(ValueError):
        BinaryCommand(-1, 1, 0)
    with pytest.raises(ValueError):
        BinaryCommand(3, -2, 123, 3)

def test_negative_data_does_not_raise_exceptions():
    BinaryCommand(1, 55, -12312)

def test_encode():
    bc = BinaryCommand(1, 2, 3)
    # In this case encode() is not the inverse of decode().
    # encode() will convert from a BinaryCommand to "bytes",
    # and then decode will convert from bytes to unicode str.
    # The "decode()" call is only necessary to make this test
    # consistent in both Python 2 and 3.
    s = bc.encode().decode()
    assert(s[0] == '\x01')
    assert(s[1] == '\x02')
    assert(s[2] == '\x03')
    assert(s[3] == s[4] == s[5] == '\x00')

def test_encode_with_message_id():
    bc = BinaryCommand(1, 2, 3, 4)
    s = bc.encode().decode()
    assert(s[0] == '\x01')
    assert(s[1] == '\x02')
    assert(s[2] == '\x03')
    assert(s[3] == s[4] == '\x00')
    assert(s[5] == '\x04')

def test_message_id_clobbers_4th_data_bit():
    bc = BinaryCommand(1, 2, 2038004089, 9)
    s = bc.encode().decode()
    assert(s[0] == '\x01')
    assert(s[1] == '\x02')
    assert(s[2] == s[3] == s[4] == '\x79')
    assert(s[5] == '\x09')
