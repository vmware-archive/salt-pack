"""Checks if all *.pyc and *.pyo files have later mtime than their *.py files."""

import imp
import os
import sys

# list of test and other files that we expect not to have bytecode
not_compiled = [
    'test/bad_coding.py',
    'test/bad_coding2.py',
    'test/badsyntax_3131.py',
    'test/badsyntax_future3.py',
    'test/badsyntax_future4.py',
    'test/badsyntax_future5.py',
    'test/badsyntax_future6.py',
    'test/badsyntax_future7.py',
    'test/badsyntax_future8.py',
    'test/badsyntax_future9.py',
    'test/badsyntax_future10.py',
    'test/badsyntax_pep3120.py',
    'lib2to3/tests/data/bom.py',
    'lib2to3/tests/data/crlf.py',
    'lib2to3/tests/data/different_encoding.py',
    'lib2to3/tests/data/false_encoding.py',
    'lib2to3/tests/data/py2_test_grammar.py',
    '.debug-gdb.py',
]
failed = 0

def bytecode_expected(source):
    for f in not_compiled:
        if source.endswith(f):
            return False
    return True

compiled = filter(lambda f: bytecode_expected(f), sys.argv[1:])
for f in compiled:
    # check both pyo and pyc
    to_check = map(lambda b: imp.cache_from_source(f, b), (True, False))
    f_mtime = os.path.getmtime(f)
    for c in to_check:
        c_mtime = os.path.getmtime(c)
        if c_mtime < f_mtime:
            sys.stderr.write('Failed bytecompilation timestamps check: ')
            sys.stderr.write('Bytecode file {} is older than source file {}.\n'.format(c, f))
            failed += 1

if failed:
    sys.stderr.write('\n{} files failed bytecompilation timestamps check.\n'.format(failed))
    sys.exit(1)
