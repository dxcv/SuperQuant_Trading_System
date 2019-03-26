#


from SuperQuant.SQUtil.SQRandom import SQ_util_random_with_topic


"""标准的SuperQuant事件方法,具有SQ_Thread,SQ_Event等特性,以及一些日志和外部接口"""


class SQ_Task():
    def __init__(self, worker, event, engine=None, callback=False):
        self.worker = worker
        self.event = event
        self.res = None
        self.callback = callback
        self.task_id = SQ_util_random_with_topic('Task')
        self.engine = engine

    def __repr__(self):
        return '< SQ_Task engine {} , worker {} , event {},  id = {} >'.format(self.engine,self.worker, self.event, id(self))

    def do(self):
        self.res = self.worker.run(self.event)
        if self.callback:
            self.callback(self.res)

    @property
    def result(self):
        # return {
        #     'task_id': self.task_id,
        #     'result': self.res,
        #     'worker': self.worker,
        #     'event': self.event
        # }
        return {
            'task_id': self.task_id,
            'result': self.res
        }


if __name__ == '__main__':
    pass

