import os
import time
import uuid
from datetime import datetime

from conf import (
    FLY_PYSHGP_PATH,
    FLY_JOB_TEMPLATE,
    FLY_PYTHON_HOME,
    FLY_LOG_PATH
)


def get_log_file(problem_file: str) -> str:
    problem = problem_file.split('/')[-2:]
    problem[1] = problem[1].split('.')[0]
    log = '{log}/{prob_dir}/{prob_name}__{d}.txt'.format(
        log=FLY_LOG_PATH,
        prob_dir=problem[0],
        prob_name=problem[1],
        d=str(datetime.now()).replace(' ', '_'))
    return log


def get_python_call(problem_file: str) -> str:
    # log = get_log_file(problem_file)
    python_call = '{py} {pyshgp}/{file}'
    return python_call.format(
        py=FLY_PYTHON_HOME, pyshgp=FLY_PYSHGP_PATH, file=problem_file)


def start_fly_run(job_name: str, problem_file: str):
    run_line = get_python_call(problem_file)
    job_cmd = ''
    with open(FLY_JOB_TEMPLATE, 'r') as f:
        job_cmd = f.read().format(
            job_name=job_name,
            task_name=job_name,
            pyshgp_path=FLY_PYSHGP_PATH,
            run_line=run_line)
    with open('run_manager/pysh_job.alf', 'w') as f:
        f.write(job_cmd)
    os.system(' '.join(
        ['/opt/pixar/tractor-blade-1.7.2/python/bin/python2.6',
         '/opt/pixar/tractor-blade-1.7.2/tractor-spool.py',
         '--engine=fly:8000',
         '{}/run_manager/pysh_job.alf'.format(FLY_PYSHGP_PATH)]))


def start_n_fly_runs(problem_file, n_runs):
    problem_filename = problem_file.split('/')[-1]
    problem_name = problem_filename.split('.')[0]
    batch_hash = str(uuid.uuid4())[:8]
    for i in range(n_runs):
        job_name = 'pyshgp_{prob}_{n}_{hash}'.format(
            prob=problem_name, n=i, hash=batch_hash)
        start_fly_run(job_name, problem_file)
        time.sleep(1)
