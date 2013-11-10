# -*- coding: utf-8 -*-

import sys

if __name__ == '__main__':
    from nose import run
    ok = run(argv=[sys.argv[0], '--all-modules'])
    if not ok:
        sys.exit(1)

