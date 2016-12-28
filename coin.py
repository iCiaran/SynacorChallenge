from itertools import permutations


def main():
    c = {2: "red", 9: "blue", 3: "corroded", 7: "concave", 5: "shiny"}
    for p in permutations(c):
        if p[0] + p[1] * p[2] ** 2 + p[3] ** 3 - p[4] == 399:
            print(p)
            print(c[p[0]], c[p[1]], c[p[2]], c[p[3]], c[p[4]])
            break


if __name__ == '__main__':
    main()
