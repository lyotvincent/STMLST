#!/usr/bin/env python

import os
import sys
import serotools.serotools as sero


def main():
    wklm = sero.wklm_df
    print(wklm.head())
    


if __name__ == '__main__':
    main()

