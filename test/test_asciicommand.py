from zaber.serial import AsciiCommand

def test_string_constructor():
    ac = AsciiCommand("home")
    assert(ac.device_address == 0)
    assert(ac.axis_number == 0)
    assert(ac.data == "home")

def test_leading_slash():
    ac = AsciiCommand("/move rel 1000")
    assert(ac.device_address == 0)
    assert(ac.axis_number == 0)
    assert(ac.data == "move rel 1000")

def test_trailing_return_newline():
    ac = AsciiCommand("tools setcomm 9600 1\r\n")
    assert(ac.device_address == 0)
    assert(ac.axis_number == 0)
    assert(ac.data == "tools setcomm 9600 1")

def test_device_address():
    ac = AsciiCommand("/1 home")
    assert(ac.device_address == 1)
    assert(ac.axis_number == 0)
    assert(ac.data == "home")

def test_axis_number():
    ac = AsciiCommand("/12 3 move abs 1000\r\n")
    assert(ac.device_address == 12)
    assert(ac.axis_number == 3)
    assert(ac.data == "move abs 1000")

def test_message_id_present():
    ac = AsciiCommand("1 2 3 home")
    assert(ac.device_address == 1)
    assert(ac.axis_number == 2)
    assert(ac.message_id == 3)
    assert(ac.data == "home")

def test_message_id_is_none():
    ac = AsciiCommand("1 1 home")
    assert(ac.device_address == 1)
    assert(ac.axis_number == 1)
    assert(ac.message_id == None)
    assert(ac.data == "home")

def test_multiple_arguments():
    ac = AsciiCommand(1, 2, "home")
    assert(ac.device_address == 1)
    assert(ac.axis_number == 2)
    assert(ac.data == "home")

def test_arguments_without_axis_number():
    ac = AsciiCommand(3, "asdf")
    assert(ac.device_address == 3)
    assert(ac.axis_number == 0)
    assert(ac.data == "asdf")

def test_arguments_with_message_id():
    ac = AsciiCommand(5, 6, 7, "home")
    assert(ac.device_address == 5)
    assert(ac.axis_number == 6)
    assert(ac.message_id == 7)
    assert(ac.data == "home")

def test_empty_constructor():
    ac = AsciiCommand()
    assert(ac.device_address == 0)
    assert(ac.axis_number == 0)
    assert(ac.data == "")

def test_multiple_string_arguments():
    ac = AsciiCommand("1", "2", "4", "move rel", "10000")
    assert(ac.device_address == 1)
    assert(ac.axis_number == 2)
    assert(ac.message_id == 4)
    assert(ac.data == "move rel 10000")

def test_multiple_string_arguments_with_integer_arguments():
    ac = AsciiCommand(1, 2, "move abs", "4000")
    assert(ac.device_address == 1)
    assert(ac.axis_number == 2)
    assert(ac.data == "move abs 4000")

def test_command_parameter_as_integer():
    ac = AsciiCommand(1, "move rel", 5000)
    assert(ac.device_address == 1)
    assert(ac.data == "move rel 5000")

def test_binary_strings():
    ac = AsciiCommand(1, b"move abs", 4000)
    assert(ac.device_address == 1)
    assert(ac.data == "move abs 4000")
    ac2 = AsciiCommand(b"/1 0 tools setcomm 9600 1\r\n")
    assert(ac2.device_address == 1)
    assert(ac2.axis_number == 0)
    assert(ac2.data == "tools setcomm 9600 1")

def test_print():
    command_string = "/1 0 get system.temperature\r\n"
    ac = AsciiCommand(command_string)
    printed_string = str(ac)
    assert(printed_string == command_string.rstrip("\r\n"))
