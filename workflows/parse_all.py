from lk_elections import Parser1947, Parser1977


def main():
    for id in [1947, 1952, 1956, '1960-03-19', '1960-07-20', 1965, 1970]:
        break
        p = Parser1947(id)
        p.parse()

    for id in [1977]:
        p = Parser1977(id)
        p.parse()


if __name__ == "__main__":
    main()
