import docopt
from crc.crc import create_lookup_table


def main():
    """
    Usage:
      crc-table <width> <polynom>
    """
    args = docopt.docopt(doc=main.__doc__, version='0.1.0')
    width = int(args['<width>'])
    polynom = int(args['<polynom>'], 16)
    lookup_table = create_lookup_table(width, polynom)
    print("{}".format(lookup_table))


if __name__ == '__main__':
    main()