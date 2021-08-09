import sys
from luma.core import cmdline, error

def get_device(actual_args=None):
    """
    Create device from command-line arguments and return it.
    """
    actual_args = sys.argv[1:]
    parser = cmdline.create_parser(description='firmware args parser')
    args = parser.parse_args(actual_args)

    # create device
    try:
        args.display = 'sh1106'
        args.height = 128
        args.rotate = 2
        args.interface = 'spi'
        args.gpio_data_command = 9
        args.spi_device = 1 
        device = cmdline.create_device(args)
        return device

    except error.Error as e:
        parser.error(e)
        return None
