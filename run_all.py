#!/usr/bin/env python

from migrate import migrate_discogs
from process_woo import process_woo


def main():
    migrate_discogs()
    process_woo()




if __name__ == "__main__":
    main()

