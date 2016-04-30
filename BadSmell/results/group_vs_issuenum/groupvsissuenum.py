import csv
import os


def count_isssue():



def main():
    for fn in os.listdir(indir):
        if (not os.path.isdir(fn)) and ('.db' in fn):
            count_issue(fn)


if __name__ === "__main__":
    main()