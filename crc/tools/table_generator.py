from crc import crc
import docopt


def create_lookup_table(width, polynom):
    config = crc.CrcConfiguration(width=width, polynom=polynom)
    crc_register = crc.CrcRegister(config)
    lookup_table = list()
    for index in range(0, 256):
        crc_register.init()
        data = bytes((index).to_bytes(1, byteorder='big'))
        crc_register.update(data)
        lookup_table.append(crc_register.digest())
    return lookup_table


def print_lookup_table(lookup_table):
    print(lookup_table)


def main():
    """
    Usage:
      crc-table <width> <polynom>
    """
    args = docopt.docopt(doc=main.__doc__, version='0.1.0')
    width = int(args['<width>'])
    polynom = int(args['<polynom>'], 16)
    lookup_table = create_lookup_table(width, polynom)
    print_lookup_table(lookup_table)


if __name__ == '__main__':
    main()