import os, sys, signal
import random
import numpy as np
from multiprocessing import Process, Queue, current_process, freeze_support
import argparse
import re


parser = argparse.ArgumentParser()
parser.add_argument('--pgmorl', default=False, action='store_true')
parser.add_argument('--ra', default=False, action='store_true')
parser.add_argument('--pfa', default=False, action='store_true')
parser.add_argument('--moead', default=False, action='store_true')
parser.add_argument('--random', default=False, action='store_true')
parser.add_argument('--num-seeds', type=int, default=6)
parser.add_argument('--num-processes', 
                    type=int, 
                    default=1, 
                    help='number of algorithms to be run in parallel (Note: each algorithm needs 4 * num-tasks processors by default, so the total number of processors is 4 * num-tasks * num-processes.)')
parser.add_argument('--save-dir', type=str, default='./results/Hopper-v2')
args = parser.parse_args()

random.seed(2000)
commands = []
save_dir = args.save_dir


test_pgmorl = args.pgmorl
test_ra = args.ra
test_random = args.random
test_pfa = args.pfa
test_moead = args.moead

def worker(input, output):
        for cmd in iter(input.get, 'STOP'):
            ret_code = os.system(cmd)
            if ret_code != 0:
                output.put('killed')
                break
        output.put('done')


# gravity_list = [
#     "-2.539 0 -9.4757", # black
#     "-2.519 0 -10.493", # our new, inherit black
#     "-2.519 0 -10.493"  # base new
# ]
# msg_list = [
#     "_1g_15d_pre",
#     "_11g_135d_new",
#     "_11g_135d_base"
# ]
# inherit_list = [
#     "F", "_1g_15d_pre", "F"
# ]

gravity_list = [
    "-2.539 0 -9.4757" # black but new
]
msg_list = [
    "_1g_15d_new"
]
inherit_list = [
    "_11g_135d_base"
]


xml_path = '/home/qwq/Desktop/RL_Robots/Git_folder/RL_robots/PGMORL_copy/environments/assets/hopper.xml'


for ri in range(len(msg_list)):
    
    for i in range(args.num_seeds):
        seed = random.randint(0, 1000000)
        if test_pgmorl:

            with open(xml_path, 'r') as file:
                xml = file.read()
                new = re.sub(r'' + 'gravity' + r'=".*"', 'gravity' + '="' + gravity_list[ri] + '"', xml)
                file.close()
                with open(xml_path, 'w') as f:
                    f.write(new)
                    f.flush()
                    f.close()

            cmd = 'python morl/run.py '\
                '--env-name MO-Hopper-v2 '\
                '--seed {} '\
                '--num-env-steps 8000000 '\
                '--warmup-iter 200 '\
                '--update-iter 40 '\
                '--min-weight 0.0 '\
                '--max-weight 1.0 '\
                '--delta-weight 0.2 '\
                '--eval-num 1 '\
                '--pbuffer-num 100 '\
                '--pbuffer-size 2 '\
                '--selection-method prediction-guided '\
                '--num-weight-candidates 7 '\
                '--num-tasks 6 '\
                '--sparsity 1.0 '\
                '--obj-rms '\
                '--ob-rms '\
                '--raw '\
                '--msg {} '\
                '--inherit {} '\
                '--save-dir {}/pgmorl/{}/'\
                    .format(seed, msg_list[ri], inherit_list[ri], save_dir, i)
            
            print(cmd)
            commands.append(cmd)
        
        if test_ra:
            cmd = 'python morl/run.py '\
                '--env-name MO-Hopper-v2 '\
                '--seed {} '\
                '--num-env-steps 8000000 '\
                '--warmup-iter 200 '\
                '--update-iter 40 '\
                '--min-weight 0.0 '\
                '--max-weight 1.0 '\
                '--delta-weight 0.2 '\
                '--eval-num 1 '\
                '--pbuffer-num 100 '\
                '--pbuffer-size 2 '\
                '--selection-method ra '\
                '--num-tasks 6 '\
                '--obj-rms '\
                '--ob-rms '\
                '--raw '\
                '--save-dir {}/ra/{}/'\
                    .format(seed, save_dir, i)
            commands.append(cmd)

        if test_random:
            cmd = 'python morl/run.py '\
                '--env-name MO-Hopper-v2 '\
                '--seed {} '\
                '--num-env-steps 8000000 '\
                '--warmup-iter 200 '\
                '--update-iter 40 '\
                '--min-weight 0.0 '\
                '--max-weight 1.0 '\
                '--delta-weight 0.2 '\
                '--eval-num 1 '\
                '--pbuffer-num 100 '\
                '--pbuffer-size 2 '\
                '--selection-method random '\
                '--num-tasks 6 '\
                '--obj-rms '\
                '--ob-rms '\
                '--raw '\
                '--save-dir {}/random/{}/'\
                    .format(seed, save_dir, i)
            commands.append(cmd)

        if test_pfa:
            cmd = 'python morl/run.py '\
                '--env-name MO-Hopper-v2 '\
                '--seed {} '\
                '--num-env-steps 8000000 '\
                '--warmup-iter 200 '\
                '--update-iter 40 '\
                '--min-weight 0.0 '\
                '--max-weight 1.0 '\
                '--delta-weight 0.2 '\
                '--eval-num 1 '\
                '--pbuffer-num 100 '\
                '--pbuffer-size 2 '\
                '--selection-method pfa '\
                '--num-tasks 6 '\
                '--obj-rms '\
                '--ob-rms '\
                '--raw '\
                '--save-dir {}/pfa/{}/'\
                    .format(seed, save_dir, i)
            commands.append(cmd)

        if test_moead:
            cmd = 'python morl/run.py '\
                '--env-name MO-Hopper-v2 '\
                '--seed {} '\
                '--num-env-steps 8000000 '\
                '--warmup-iter 200 '\
                '--update-iter 40 '\
                '--min-weight 0.0 '\
                '--max-weight 1.0 '\
                '--delta-weight 0.2 '\
                '--eval-num 1 '\
                '--pbuffer-num 100 '\
                '--pbuffer-size 2 '\
                '--selection-method moead '\
                '--num-tasks 6 '\
                '--obj-rms '\
                '--ob-rms '\
                '--raw '\
                '--save-dir {}/moead/{}/'\
                    .format(seed, save_dir, i)
            commands.append(cmd)

    

    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    # Submit tasks
    for cmd in commands:
        task_queue.put(cmd)

    # Submit stop signals
    for i in range(args.num_processes):
        task_queue.put('STOP')

    # Start worker processes
    for i in range(args.num_processes):
        Process(target=worker, args=(task_queue, done_queue)).start()

    # Get and print results
    for i in range(args.num_processes):
        print(f'Process {i}', done_queue.get())
