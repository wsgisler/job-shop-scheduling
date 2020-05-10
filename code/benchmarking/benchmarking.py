import sys
import json
sys.path.append('../')

from docplex.cp.model import *
from utils.objects import *
from time import time
from job_shop_blocking.blocking_job_shop_cpoptimizer import optimize as opt1
from job_shop_blocking.blocking_job_shop_ortools import optimize as opt2
from job_shop_simple.simple_job_shop_cpoptimizer import optimize as opt3
from job_shop_simple.simple_job_shop_ortools import optimize as opt4
from job_shop_simple.blocking_job_shop_mip import optimize as opt5
from job_shop_simple.simple_job_shop_mip import optimize as opt6

def optimize_and_visualize(instance_name, time_limit = 100, threads = 1):
    reader = Reader(instance_name)
    instance = reader.get_instance()
    solution = optimize(instance, time_limit = time_limit, threads = threads)
    solution.visualize(time_factor = 1, time_grid = 50)
    
if __name__ == '__main__':
    stats = open('../../solutions/benchmarking.csv','w')
    stats.write('Instance name,Type,Solver,Time limit,Threads,Attempt,Makespan,Proved Optimal\n')

    f = open('../../instances.json','r')
    data = json.load(f)
    for instance_data in data:
        for time_limit in [10,20,60,300]:
            for threads in [1,2,4,8,16,32]:
                for attempt in range(5):
                    reader = Reader(instance_data['name'])
                    instance = reader.get_instance()
                    st = time()
                    solution = opt1(instance, time_limit = time_limit, threads = threads)
                    opt = 'True' if time()-st < time_limit else 'False'
                    stats.write('%s,Blocking,CPOPT,%i,%i,%i,%f,%s\n'%(instance.name,time_limit,threads,attempt,solution.get_makespan(),opt))
                    st = time()
                    solution = opt2(instance, time_limit = time_limit, threads = threads)
                    opt = 'True' if time()-st < time_limit else 'False'
                    stats.write('%s,Blocking,ORTOOLS,%i,%i,%i,%f,%s\n'%(instance.name,time_limit,threads,attempt,solution.get_makespan(),opt))
                    st = time()
                    solution = opt5(instance, time_limit = time_limit, threads = threads)
                    opt = 'True' if time()-st < time_limit else 'False'
                    stats.write('%s,Blocking,MIPCPLEX,%i,%i,%i,%f,%s\n'%(instance.name,time_limit,threads,attempt,solution.get_makespan(),opt))
                    st = time()
                    solution = opt3(instance, time_limit = time_limit, threads = threads)
                    opt = 'True' if time()-st < time_limit else 'False'
                    stats.write('%s,Simple,CPOPT,%i,%i,%i,%f,%s\n'%(instance.name,time_limit,threads,attempt,solution.get_makespan(),opt))
                    st = time()
                    solution = opt4(instance, time_limit = time_limit, threads = threads)
                    opt = 'True' if time()-st < time_limit else 'False'
                    stats.write('%s,Simple,ORTOOLS,%i,%i,%i,%f,%s\n'%(instance.name,time_limit,threads,attempt,solution.get_makespan(),opt))
                    st = time()
                    solution = opt6(instance, time_limit = time_limit, threads = threads)
                    opt = 'True' if time()-st < time_limit else 'False'
                    stats.write('%s,Simple,MIPCPLEX,%i,%i,%i,%f,%s\n'%(instance.name,time_limit,threads,attempt,solution.get_makespan(),opt))
                    stats.flush()
    stats.close()
    f.close()