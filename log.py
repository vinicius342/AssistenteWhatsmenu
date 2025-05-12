import datetime
from utils import FILE_LOG

datetime_now = datetime.datetime

try:
    open(FILE_LOG, 'xt', encoding='UTF-8') if not FILE_LOG.exists() else None
except Exception:
    ...


class Log:

    log_on = True
    def _log(self, msg): ...

    def log_success(self, msg):
        if not self.log_on:
            return
        return self._log(f'SUCCESS: {msg} '
                         '({self.__class__.__name__}) '
                         f'{datetime_now.now().strftime('%d/%m/%Y %H:%M:%S')}')

    def log_error(self, msg):
        if not self.log_on:
            return
        return self._log(f'ERROR: {msg} ({self.__class__.__name__}) '
                         f'{datetime_now.now().strftime('%d/%m/%Y %H:%M:%S')}')


class LogFileMixin(Log):
    def _log(self, msg):
        with open(FILE_LOG, 'a', encoding='utf8') as file:
            file.write(msg)
            file.write('\n')


if __name__ == '__main__':
    test = LogFileMixin()
    test.log_success('vincii')
    test.log_error('camiiss')
