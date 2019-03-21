# -*- coding: utf-8 -*-


from multiprocessing import Pool, cpu_count


class ParallelSim(object):
    """ 多进程map类
        pl = ParallelSim()
        pl.add(yourFunc, yourIter)
        data = pl.get_results()
        data = list(data)
        print(data)
    """

    def __init__(self, processes=cpu_count()):
        '''

        :param processes: 进程数量，默认为cpu个数
        '''
        self.pool = Pool(processes=processes)
        self.total_processes = 0
        self.completed_processes = 0
        self.results = []
        self.data = None
        self.cores = processes  # cpu核心数量

    def add(self, func, iter):
        if isinstance(iter, list) and self.cores > 1:
            for i in range(self.cores):
                pLen = int(len(iter) / self.cores) + 1
                self.data = self.pool.starmap_async(func, iter[int(i * pLen):int((i + 1) * pLen)],
                                                    callback=self.complete)
                self.total_processes += 1
        else:
            self.data = self.pool.starmap_async(func=func, iterable=iter, callback=self.complete)
            self.total_processes += 1
        self.data.get()

    def complete(self, result):
        self.results.extend(result)
        self.completed_processes += 1
        print('Progress: {:.2f}%'.format((self.completed_processes / self.total_processes) * 100))

    def run(self):
        self.pool.close()
        self.pool.join()

    def get_results(self):
        return self.results
