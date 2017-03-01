#!/usr/bin/python
# coding=utf8
from Queue import Queue
import threading
import contextlib

WorkerStop = object()


class ThreadPool:
    workers = 0
    thread_factory = threading.Thread
    current_thread = staticmethod(threading.currentThread)

    def __init__(self, max_threads=32, name=None):
        self.queue = Queue(0)
        self.max_threads = max_threads
        self.name = name
        self.waiters = []                   # 存放等待线程的列表
        self.working = []                   # 存放工作线程的列表

    def start(self):
        need_size = self.queue.qsize()
        while self.workers < min(self.max_threads, need_size):
            self.start_a_worker()

    def start_a_worker(self):
        self.workers += 1
        new_thread = self.thread_factory(target=self._worker, name='New Worker')
        new_thread.start()

    def call_in_thread(self, func, *args, **kwargs):
        self.call_in_thread_with_callback(None, func, *args, **kwargs)

    def call_in_thread_with_callback(self, on_result, func, *args, **kwargs):
        job = (func, args, kwargs, on_result)
        self.queue.put(job)

    @contextlib.contextmanager
    def _work_state(self, states, worker_thread):
        assert isinstance(states, list)
        states.append(worker_thread)        # 把当前执行线程加入线程状态列表states
        try:
            yield
        finally:
            states.remove(worker_thread)    # 执行完成后从状态列表中移除

    def _worker(self):
        ct = self.current_thread()          # 获取当前线程id
        job = self.queue.get()

        while job is not WorkerStop:
            with self._work_state(self.working, ct):
                func, args, kwargs, on_result = job
                del job
                try:
                    result = func(*args, **kwargs)
                    success = True
                except:
                    success = False

                del func, args, kwargs
                if on_result is not None:
                    try:
                        on_result(success, result)
                    except:
                        pass
                del on_result, result
            with self._work_state(self.waiters, ct):
                job = self.queue.get()

    def stop(self):
        """
        Close threads
        :return:
        """
        while self.workers:
            self.queue.put(WorkerStop)
            self.workers -= 1

if __name__ == '__main__':

    def show_timestamp(name):
        import time
        print '%s: %s' % (name, time.time())
        time.sleep(1)
    pool = ThreadPool(10)
    for i in range(100):
        pool.call_in_thread(show_timestamp, i)
    print '# Before start()'
    pool.start()
    print '# After start()'
    pool.stop()
    print '# After stop()'
