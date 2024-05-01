class Int:
    def parse(x):
        x = str(x)
        if x == 'Uncontested-':
            return 0
        if x == '-':
            return 0
        if x == '':
            return 0
        x = x.replace(',', '')
        return int(x)

    def isinstance(x):
        try:
            Int.parse(x)

            return True
        except BaseException:
            return False
