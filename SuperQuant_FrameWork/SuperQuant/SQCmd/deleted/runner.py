import shlex
import subprocess
import sys

from SuperQuant.SQUtil.SQLogs import SQ_util_log_info


def run_backtest(shell_cmd):
    shell_cmd = 'python "{}"'.format(shell_cmd)
    cmd = shlex.split(shell_cmd)
    p = subprocess.Popen(
        cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while p.poll() is None:
        line = p.stdout.readline()
        line = line.strip()
        if line:

            SQ_util_log_info(line)
            #print('SuperQuant: [{}]'.format(line))
    if p.returncode == 0:
        SQ_util_log_info('backtest run  success')

    else:
        SQ_util_log_info('Subprogram failed')
    return p.returncode


def run():
    shell_cmd = sys.argv[1]
    print(shell_cmd)
    return run_backtest(shell_cmd)


if __name__ == "__main__":
    print(run())

