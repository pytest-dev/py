
"""
    ForkedFunc provides a way to run a function in a forked process
    and get at its return value, stdout and stderr output as well
    as signals and exitstatusus.
"""

import py
import os
import sys
import marshal


class HookMixin(object):
    _on_start = list()
    _on_exit = list()

    @classmethod
    def register_on_start(cls, callback):
        cls._on_start.append(callback)

    @classmethod
    def register_on_exit(self, callback):
        self._on_exit.append(callback)

    def _run_on_start(self):
        self._run_callbacks(self._on_start)

    def _run_on_exit(self):
        self._run_callbacks(self._on_exit)

    def _run_callbacks(self, callbacks):
        for callback in callbacks:
            callback(self)


class ForkedFunc(HookMixin):
    EXITSTATUS_EXCEPTION = 3


    def __init__(self, fun, args=None, kwargs=None, nice_level=0):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        self.fun = fun
        self.args = args
        self.kwargs = kwargs
        self.tempdir = tempdir = py.path.local.mkdtemp()
        self.RETVAL = tempdir.ensure('retval')
        self.STDOUT = tempdir.ensure('stdout')
        self.STDERR = tempdir.ensure('stderr')

        pid = os.fork()
        if pid:  # in parent process
            self.pid = pid
        else:  # in child process
            self.pid = None
            self._child(nice_level)

    def _child(self, nice_level):
        # right now we need to call a function, but first we need to
        # map all IO that might happen
        sys.stdout = stdout = open(str(self.STDOUT), "wb", 0)
        fdstdout = stdout.fileno()
        if fdstdout != 1:
            os.dup2(fdstdout, 1)
        sys.stderr = stderr = open(str(self.STDERR), "wb", 0)
        fdstderr = stderr.fileno()
        if fdstderr != 2:
            os.dup2(fdstderr, 2)
        retvalf = self.RETVAL.open("wb")
        EXITSTATUS = 0
        try:
            if nice_level:
                os.nice(nice_level)
            try:
                self._run_on_start()
                retval = self.fun(*self.args, **self.kwargs)
                retvalf.write(marshal.dumps(retval))
                self._run_on_exit()
            except:
                excinfo = py.code.ExceptionInfo()
                stderr.write(excinfo.exconly())
                EXITSTATUS = self.EXITSTATUS_EXCEPTION
        finally:
            stdout.close()
            stderr.close()
            retvalf.close()
        os.close(1)
        os.close(2)
        os._exit(EXITSTATUS)

    def waitfinish(self, waiter=os.waitpid):
        pid, systemstatus = waiter(self.pid, 0)
        if systemstatus:
            if os.WIFSIGNALED(systemstatus):
                exitstatus = os.WTERMSIG(systemstatus) + 128
            else:
                exitstatus = os.WEXITSTATUS(systemstatus)
        else:
            exitstatus = 0
        signal = systemstatus & 0x7f
        if not exitstatus and not signal:
            retval = self.RETVAL.open('rb')
            try:
                retval_data = retval.read()
            finally:
                retval.close()
            retval = marshal.loads(retval_data)
        else:
            retval = None
        stdout = self.STDOUT.read()
        stderr = self.STDERR.read()
        self._removetemp()
        return Result(exitstatus, signal, retval, stdout, stderr)

    def _removetemp(self):
        if self.tempdir.check():
            self.tempdir.remove()

    def __del__(self):
        if self.pid is not None:  # only clean up in main process
            self._removetemp()


class Result(object):
    def __init__(self, exitstatus, signal, retval, stdout, stderr):
        self.exitstatus = exitstatus
        self.signal = signal
        self.retval = retval
        self.out = stdout
        self.err = stderr
