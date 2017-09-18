import time
import argparse
from datetime import datetime
from subprocess import call


PYSHGP_PATH = '/home/erp12/pyshgp'
JOB_FILE = PYSHGP_PATH + '/benchmark/fly-template.alf'
PYTHON_HOME = '/home/erp12/anaconda3/bin/python'
LOG_PATH = '/home/erp12/gp_runs/pyshgp'


def get_log_file(problem_file: str) -> str:
    problem = problem_file.split('/')[-2:]
    problem[1] = problem[1].split('.')[0]
    log = '{log}/{prob_dir}/{prob_name}__{d}.txt'.format(
        log=LOG_PATH,
        prob_dir=problem[0],
        prob_name=problem[1],
        d=str(datetime.now()).replace(' ', '_'))
    return log


def get_python_call(problem_file: str) -> str:
    log = get_log_file(problem_file)
    python_call = '{py} {file} > {log}'
    return python_call.format(py=PYTHON_HOME, file=problem_file, log=log)


def start_run(job_name: str, problem_file: str):
    run_line = get_python_call(problem_file)
    job_cmd = ''
    with open(JOB_FILE, 'r') as f:
        job_cmd = f.read().format(
            job_name=job_name,
            task_name=job_name,
            pyshgp_path=PYSHGP_PATH,
            run_line=run_line)
    with open('pysh_job.alf', 'w') as f:
        f.write(job_cmd)
    call([
        '/opt/pixar/tractor-blade-1.7.2/python/bin/python2.6',
        '/opt/pixar/tractor-blade-1.7.2/tractor-spool.py',
        '--engine=fly:8000',
        'pysh_job.alf'
    ])


def start_n_runs(problem_file, n_runs):
    problem_name = problem_file.split('/')[-1]
    for i in range(n_runs):
        job_name = '{prob}_{n}_pyshgp'.format(prob=problem_name, n=i)
        start_run(job_name, problem_file)
        time.sleep(1)


def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file',
        type=str,
        help='Path to problem file realtive to pyshgp root. Likely in examples folder.')
    parser.add_argument(
        'n',
        type=int,
        help='Number of runs to start.')
    return parser.parse_args()


if __name__ == "__main__":
    cli_args = get_cli_args()
    start_n_runs(cli_args.file, cli_args.n)
