import pytest, py
import re

def exvalue():
    import sys
    return sys.exc_info()[1]

def f():
    return 2

def test_assert():
    try:
        assert f() == 3
    except AssertionError:
        e = exvalue()
        s = str(e)
        assert s.startswith('assert 2 == 3\n')


def test_assert_within_finally():
    with py.test.raises(ZeroDivisionError,
                        match=".*division.* by zero"):
        try:
            1 / 0
        finally:
            i = 42

def test_assert_multiline_1():
    try:
        assert (f() ==
                3)
    except AssertionError:
        e = exvalue()
        s = str(e)
        assert s.startswith('assert 2 == 3\n')

def test_assert_multiline_2():
    try:
        assert (f() == (4,
                   3)[-1])
    except AssertionError:
        e = exvalue()
        s = str(e)
        assert s.startswith('assert 2 ==')

def test_in():
    try:
        assert "hi" in [1, 2]
    except AssertionError:
        e = exvalue()
        s = str(e)
        assert s.startswith("assert 'hi' in")

def test_is():
    try:
        assert 1 is 2
    except AssertionError:
        e = exvalue()
        s = str(e)
        assert s.startswith("assert 1 is 2")


def test_attrib():
    class Foo(object):
        b = 1
    i = Foo()
    try:
        assert i.b == 2
    except AssertionError:
        e = exvalue()
        s = str(e)
        assert s.startswith("assert 1 == 2")

def test_attrib_inst():
    class Foo(object):
        b = 1
    try:
        assert Foo().b == 2
    except AssertionError:
        e = exvalue()
        s = str(e)
        assert s.startswith("assert 1 == 2")

def test_len():
    l = list(range(42))
    try:
        assert len(l) == 100
    except AssertionError:
        e = exvalue()
        s = str(e)
        assert s.startswith("assert 42 == 100")
        assert "where 42 = len([" in s


def test_assert_keyword_arg():
    def f(x=3):
        return False
    try:
        assert f(x=5)
    except AssertionError:
        e = exvalue()
        assert "x=5" in str(e)

# These tests should both fail, but should fail nicely...
class WeirdRepr:
    def __repr__(self):
        return '<WeirdRepr\nsecond line>'

def bug_test_assert_repr():
    v = WeirdRepr()
    try:
        assert v == 1
    except AssertionError:
        e = exvalue()
        assert str(e).find('WeirdRepr') != -1
        assert str(e).find('second line') != -1
        assert 0

def test_assert_non_string():
    try:
        assert 0, ['list']
    except AssertionError:
        e = exvalue()
        assert str(e).find("list") != -1

def test_assert_implicit_multiline():
    try:
        x = [1,2,3]
        assert x != [1,
           2, 3]
    except AssertionError:
        e = exvalue()
        assert str(e).find('assert [1, 2, 3] !=') != -1

@py.test.mark.xfail(py.test.__version__[0] != "2",
                    reason="broken on modern pytest",
                    run=False
)
def test_assert_with_brokenrepr_arg():
    class BrokenRepr:
        def __repr__(self): 0 / 0
    e = AssertionError(BrokenRepr())
    if e.msg.find("broken __repr__") == -1:
        py.test.fail("broken __repr__ not handle correctly")

def test_multiple_statements_per_line():
    try:
        a = 1; assert a == 2
    except AssertionError:
        e = exvalue()
        assert "assert 1 == 2" in str(e)

def test_power():
    try:
        assert 2**3 == 7
    except AssertionError:
        e = exvalue()
        assert "assert (2 ** 3) == 7" in str(e)


class TestView:

    def setup_class(cls):
        cls.View = py.test.importorskip("py._code._assertionold").View

    def test_class_dispatch(self):
        ### Use a custom class hierarchy with existing instances

        class Picklable(self.View):
            pass

        class Simple(Picklable):
            __view__ = object
            def pickle(self):
                return repr(self.__obj__)

        class Seq(Picklable):
            __view__ = list, tuple, dict
            def pickle(self):
                return ';'.join(
                    [Picklable(item).pickle() for item in self.__obj__])

        class Dict(Seq):
            __view__ = dict
            def pickle(self):
                return Seq.pickle(self) + '!' + Seq(self.values()).pickle()

        assert Picklable(123).pickle() == '123'
        assert Picklable([1,[2,3],4]).pickle() == '1;2;3;4'
        assert Picklable({1:2}).pickle() == '1!2'

    def test_viewtype_class_hierarchy(self):
        # Use a custom class hierarchy based on attributes of existing instances
        class Operation:
            "Existing class that I don't want to change."
            def __init__(self, opname, *args):
                self.opname = opname
                self.args = args

        existing = [Operation('+', 4, 5),
                    Operation('getitem', '', 'join'),
                    Operation('setattr', 'x', 'y', 3),
                    Operation('-', 12, 1)]

        class PyOp(self.View):
            def __viewkey__(self):
                return self.opname
            def generate(self):
                return '%s(%s)' % (self.opname, ', '.join(map(repr, self.args)))

        class PyBinaryOp(PyOp):
            __view__ = ('+', '-', '*', '/')
            def generate(self):
                return '%s %s %s' % (self.args[0], self.opname, self.args[1])

        codelines = [PyOp(op).generate() for op in existing]
        assert codelines == ["4 + 5", "getitem('', 'join')",
            "setattr('x', 'y', 3)", "12 - 1"]

def test_underscore_api():
    py.code._AssertionError
    py.code._reinterpret_old # used by pypy
    py.code._reinterpret

def test_assert_customizable_reprcompare(monkeypatch):
    util = pytest.importorskip("_pytest.assertion.util")
    monkeypatch.setattr(util, '_reprcompare', lambda *args: 'hello')
    try:
        assert 3 == 4
    except AssertionError:
        e = exvalue()
        s = str(e)
        assert "hello" in s

def test_assert_long_source_1():
    try:
        assert len == [
            (None, ['somet text', 'more text']),
        ]
    except AssertionError:
        e = exvalue()
        s = str(e)
        assert 're-run' not in s
        assert 'somet text' in s

def test_assert_long_source_2():
    try:
        assert(len == [
            (None, ['somet text', 'more text']),
        ])
    except AssertionError:
        e = exvalue()
        s = str(e)
        assert 're-run' not in s
        assert 'somet text' in s

def test_assert_raise_alias(testdir):
    testdir.makepyfile("""
    import sys
    EX = AssertionError
    def test_hello():
        raise EX("hello"
            "multi"
            "line")
    """)
    result = testdir.runpytest()
    result.stdout.fnmatch_lines([
        "*def test_hello*",
        "*raise EX*",
        "*1 failed*",
    ])

@py.test.mark.xfail(py.test.__version__[0] != "2",
                    reason="broken on modern pytest",
                    run=False)
def test_assert_raise_subclass():
    class SomeEx(AssertionError):
        def __init__(self, *args):
            super(SomeEx, self).__init__()
    try:
        raise SomeEx("hello")
    except AssertionError as e:
        s = str(e)
        assert 're-run' not in s
        assert 'could not determine' in s

def test_assert_raises_in_nonzero_of_object_pytest_issue10():
    class A(object):
        def __nonzero__(self):
            raise ValueError(42)
        def __lt__(self, other):
            return A()
        def __repr__(self):
            return "<MY42 object>"
    def myany(x):
        return True
    try:
        assert not(myany(A() < 0))
    except AssertionError:
        e = exvalue()
        s = str(e)
        assert "<MY42 object> < 0" in s
