def hexdump(src, length=16, sep='.'):
    """
    function that help pretty print bytes content
    thank to https://gist.github.com/7h3rAm/5603718
    adapted to lib needs.
    """
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or sep for x in range(256)])
    lines = []

    for c in range(0, len(src), length):
        chars = src[c:c + length]

        hexstr = ' '.join(["%02x" % ord(x) for x in chars]) if isinstance(chars, str) else ' '.join(
            ['{:02x}'.format(x) for x in chars])

        if len(hexstr) > 24:
            hexstr = "%s %s" % (hexstr[:24], hexstr[24:])

        printable = ''.join(
            [
                "%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or sep) for x in chars
            ]
        ) if isinstance(chars, str) else ''.join(['{}'.format((x <= 127 and FILTER[x]) or sep) for x in chars])

        lines.append("%08x:  %-*s  |%s|" % (c, length * 3, hexstr, printable))
    print('\n'.join(lines))
