import bluetooth


class Alpha1S:

    """
    Class to control the Ubtech Alpha 1S robot
    """

    def __init__(self, name="ALPHA 1S"):
        self.__bt = self.Alpha1S_bluetooth(name)

    def battery(self):
        """
        Get battery information.

        Returns:
        dict: Dictionary with fields:
            percent: Remaining battery capacity
            state:
                0: Battery not charging
                1: Battery charging
                2: Battery not present
            mV: Battery voltage in mV
        """
        msg = b'\x18\x00'
        parameter_len = 4
        ans = self.__bt.read(msg, parameter_len)
        if ans is not None:
            battery = {
                "percent": int.from_bytes(ans[3:], "big"),
                "state": int.from_bytes(ans[2:3], "big"),
                "mV": int.from_bytes(ans[:2], "big")
            }
            return battery
        return None

    def servo_read(self, servo_id):
        """
        Read the position of a single servo.
        Note: Reading a servo will automatically power it off.

        Parameters:
        servo_id: Servo id between 0-15, integer

        Returns:
        int: Position of the servo between 0-180
        """
        # Adding 1 to the servo_id because the robot starts counting at 1
        servo_id = bytes([servo_id+1])
        msg = b'\x24' + servo_id
        parameter_len = 2
        ans = self.__bt.read(msg, parameter_len)
        if ans is not None:
            # Check that the received value corresponds to the specified servo
            if ans[:1] == servo_id:
                return int.from_bytes(ans[1:], "big")
        return None

    def servo_read_all(self):
        """
        Read the positions for all the servos simultaneously.
        Note: Reading a servo will automatically power it off.

        Returns:
        [int]: List of 16 integer positions between 0-180
        """
        msg = b'\x25\x00'
        parameter_len = 16
        ans = self.__bt.read(msg, parameter_len)
        if ans is not None:
            return [x for x in ans]
        return None

    def servo_write(self, servo_id, angle, travelling=20):
        """
        Set a specific servo to an angle.

        Parameters:
        servo_id: Servo id between 0-15, integer
        angle: Angle between 0-180, integer
        travelling: Time the servo takes to move to the position

        Returns:
        int: Error code:
            0: Success
            1: Wrong servo servo_id
            2: Allow servo angle excess
            3: No reply from servo
        """
        # Adding 1 to the servo_id because the robot starts counting at 1
        servo_id = bytes([servo_id+1])
        angle = bytes([angle])
        run_time = bytes([travelling])
        time_frames = b'\x00\x10'
        msg = b'\x22' + servo_id + angle + run_time + time_frames
        parameter_len = 2
        ans = self.__bt.read(msg, parameter_len)
        if ans is not None:
            # Check that the received value corresponds to the specified servo
            if ans[:1] == servo_id:
                return int.from_bytes(ans[1:], "big")
        return None

    def servo_write_all(self, angles, travelling=20):
        """
        Set all servos to the specified positions simultaneously.

        Parameters:
        angles: List of integer angles between 0-180
        travelling: Time the servo takes to move to the position, integer

        Returns:
        [int]: List of error codes for each servo:
            0: Success
            1: Wrong servo servo_id
            2: Allow servo angle excess
            3: No reply from servo
        """
        if len(angles) != 16:
            return None
        angles = bytearray(angles)
        run_time = bytes([travelling])
        time_frames = b'\x00\x10'
        msg = b'\x23' + angles + run_time + time_frames
        parameter_len = 16
        ans = self.__bt.read(msg, parameter_len)
        if ans is not None:
            return [x for x in ans]
        return None

    def servo_off(self):
        """
        Send command to power off all the servos in the robot.
        """
        msg = b'\x0C\x00'
        self.__bt.write(msg)

    class Alpha1S_bluetooth:

        """
        Class to handle the Alpha1S' bluetooth protocol
        Download Bluetooth protocol datasheet from
        https://assets-new.ubtrobot.com/downloads/Alpha%201%20Series%20Bluetooth%20communication%20protocol?download
        """  # noqa

        def __init__(self, name):
            address = self.__discover(name)
            assert(address is not None), f"Error: {name} not found"
            self.__connect(address)

        def __del__(self):
            self.sock.close()

        def __discover(self, name):
            address = None
            devices = bluetooth.discover_devices(lookup_names=True)
            for add, text in devices:
                if text == name:
                    address = add
                    break
            return address

        def __connect(self, addr):
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.sock.connect((addr, 6))
            self.sock.settimeout(10.0)

        def write(self, msg):
            """
            Compose an outgoing message following the required format and send
            over the bluetooth socket. Takes bytes as input.
            """
            cmd = self.__compose(msg)
            self.sock.send(cmd)

        def read(self, msg, ans_len):
            """
            Use the write() function to send a command and receive its answer.

            Returns the 'Parameter' field in bytes if the message was received
            correctly, None otherwise.
            """
            self.write(msg)
            # Length is sum of header(2), length, check, cmd, ans_len and end
            length = 6 + ans_len
            ans = self.sock.recv(length)
            if self.__check(ans):
                return ans[4:-2]
            return None

        def __compose(self, msg):
            """
            Compose a byte message with the header, length, check and end
            bytes in the required format.
            """
            header = b'\xFB\xBF'
            end = b'\xED'
            # Length is sum of header(2), length, check + msg bytes
            length = bytes([4 + len(msg)])
            # Check is sum of length + msg (length+(cmd+params)), with modulus
            # to fit into a single byte
            check_list = bytearray(length)
            check_list.extend(msg)
            check = bytes([sum(check_list) % 256])
            return header + length + msg + check + end

        def __check(self, msg):
            """
            Check that the received message follows the correct format and that
            the check byte is correct.

            Returns True if message is correct, False otherwise
            """
            msg = bytearray(msg)
            # Check that header is correct
            if msg[:2] != b'\xFB\xBF':
                return False
            # Check that ending is correct
            elif msg[-1:] != b'\xED':
                return False
            # Check that check byte is correct
            elif msg[-2:-1] != bytes([sum(msg[2:-2]) % 256]):
                return False
            else:
                return True
