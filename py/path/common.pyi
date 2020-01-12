from typing import Any, Optional

iswin32: Any
import_errors: Any

class Checkers:
    path: Any = ...
    def __init__(self, path: Any) -> None: ...
    def dir(self) -> None: ...
    def file(self) -> None: ...
    def dotfile(self): ...
    def ext(self, arg: Any): ...
    def exists(self) -> None: ...
    def basename(self, arg: Any): ...
    def basestarts(self, arg: Any): ...
    def relto(self, arg: Any): ...
    def fnmatch(self, arg: Any): ...
    def endswith(self, arg: Any): ...

class NeverRaised(Exception): ...

class PathBase:
    strpath: str

    Checkers: Any = ...
    def __div__(self, other: Any): ...
    __truediv__: Any = ...
    def basename(self): ...
    basename: Any = ...
    def dirname(self): ...
    dirname: Any = ...
    def purebasename(self): ...
    purebasename: Any = ...
    def ext(self): ...
    ext: Any = ...
    def dirpath(self, *args: Any, **kwargs: Any): ...
    def read_binary(self): ...
    def read_text(self, encoding: Any): ...
    def read(self, mode: str = ...): ...
    def readlines(self, cr: int = ...): ...
    def load(self): ...
    def move(self, target: Any) -> None: ...
    def check(self, **kw: Any): ...
    def fnmatch(self, pattern: Any): ...
    def relto(self, relpath: Any): ...
    def ensure_dir(self, *args: Any): ...
    def bestrelpath(self, dest: Any): ...
    def exists(self): ...
    def isdir(self): ...
    def isfile(self): ...
    def parts(self, reverse: bool = ...): ...
    def common(self, other: Any): ...
    def __add__(self, other: Any): ...
    def __cmp__(self, other: Any): ...
    def __lt__(self, other: Any) -> Any: ...
    def visit(self, fil: Optional[Any] = ..., rec: Optional[Any] = ..., ignore: Any = ..., bf: bool = ..., sort: bool = ...) -> None: ...
    def samefile(self, other: Any): ...
    def __fspath__(self): ...

class Visitor:
    rec: Any = ...
    fil: Any = ...
    ignore: Any = ...
    breadthfirst: Any = ...
    optsort: Any = ...
    def __init__(self, fil: Any, rec: Any, ignore: Any, bf: Any, sort: Any) -> None: ...
    def gen(self, path: Any) -> None: ...

class FNMatcher:
    pattern: Any = ...
    def __init__(self, pattern: Any) -> None: ...
    def __call__(self, path: Any): ...
