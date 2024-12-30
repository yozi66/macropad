import busio
import board

class Bridge:

    def __init__(self):
        # Initialize the I²C bus (using default pins for SDA and SCL)
        self.i2c = busio.I2C(board.SCL, board.SDA)

        # Check if the I²C bus is initialized correctly
        if not self.i2c.try_lock():
            print("Failed to initialize I2C bus")
            exit()

        # Scan the I²C bus for connected devices (check device addresses)
        print("I2C devices found:")
        devices = self.i2c.scan()
        if not devices:
            print("No devices found")
        else:
            for device in devices:
                print(hex(device))

    def write(self, message):
        data = bytearray(message, "ascii")
        self.i2c.writeto(8, data)
