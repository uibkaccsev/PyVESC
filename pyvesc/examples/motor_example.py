from pyvesc import VESC, Firmware
import time
import logging
import argparse

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
console = logging.StreamHandler()
logger.addHandler(console)


# a function to show how to use the class with a with-statement
def run_motor_using_with(serial_port):
    with VESC(serial_port=serial_port) as motor:
        print("Firmware: ", motor.get_firmware_version())
        motor.set_duty_cycle(.02)

        # run motor and print out rpm for ~2 seconds
        for i in range(30):
            time.sleep(0.1)
            print(motor.get_measurements().rpm)
        motor.set_rpm(0)


# a function to show how to use the class as a static object.
def run_motor_as_object(serial_port):
    motor = VESC(serial_port=serial_port)
    print("Firmware: ", motor.get_firmware_version())

    # sweep servo through full range
    for i in range(100):
        time.sleep(0.01)
        motor.set_servo(i/100)

    # IMPORTANT: YOU MUST STOP THE HEARTBEAT IF IT IS RUNNING BEFORE IT GOES OUT OF SCOPE. Otherwise, it will not
    #            clean-up properly.
    motor.stop_heartbeat()

def time_get_values(serial_port):
    with VESC(serial_port=serial_port) as motor:
        start = time.time()
        motor.get_measurements()
        stop = time.time()
        print("Getting values takes ", stop-start, "seconds.")


def commands_example(port, firmware, compressed):
    """
    Example of using the terminal commands with some additional commands defined here which allow erase and firmware updates
    """

    with VESC(serial_port=port) as motor:
        print(motor.send_terminal_cmd("hw_status"))

        print("\nAll VESC commands are supported, plus the following:")
        print("fw\t\t- update firmware")
        print("erase\t\t- erase firmware ")
        print("\n\nEntering Terminal:\n====================\n")

        while True:
            # terminal console that reads in text on a newline, assigns it to the user_in string
            user_in = input("")
            if user_in == "fw":
                if firmware is None:
                    print("No firmware file specified")
                    continue
                fw = Firmware(firmware, lzss=compressed)
                motor.update_firmware(fw)
                logging.info("This script will exit as it doesn't handle serial ports reconnecting yet.")
                break

            if user_in == "erase":
                print("sending erase")
                erase_res = motor.fw_erase_new_app(fw.size)
                print("Erase status:", erase_res.erase_new_app_result)

            if user_in == "gp":
                print("Getting motor parameters")
                mcconf_res = motor.get_motor_configuration()
                print("Motor configuration: {}".format(mcconf_res))

            print(motor.send_terminal_cmd(user_in))


if __name__ == '__main__':
    # arguments
    parser = argparse.ArgumentParser(description='VESC Motor Example')
    parser.add_argument('-p', '--port', type=str, help='Serial port', default='')
    parser.add_argument('-f', '--firmware', type=str, help='Firmware file', default=None)
    parser.add_argument('-c', '--compressed', action='store_true', help='Compressed firmware', default=True)
    args = parser.parse_args()

    run_motor_using_with(args.port)
    run_motor_as_object(args.port)
    time_get_values(args.port)
    commands_example(args.port, args.firmware, args.compressed)
