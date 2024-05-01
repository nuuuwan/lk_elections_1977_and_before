from lk_elections import Parser1947


def main():
    for id in [1947, 1952, 1956, '1960-03-19', '1960-07-20', 1965, 1970]:
        p = Parser1947(id)
        p.parse()
        break


if __name__ == "__main__":
    main()
