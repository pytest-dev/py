import sys
if __name__ == '__main__':
    import py
    sys.exit(py.test.cmdline.main())
else:
    import sys, pytest
    sys.modules['py.test'] = pytest

# for more API entry points see the 'tests' definition
# in __init__.py
