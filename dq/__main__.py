import time

from rdflib import Graph


def main():
    print("Running BDR-DQ...")
    for i in range(3):
        time.sleep(1)
        print(f"{i+1}...")
    time.sleep(1)
    print("Done!")


def one(g: Graph) -> int:
    return len(g)


if __name__ == "__main__":
    main()
