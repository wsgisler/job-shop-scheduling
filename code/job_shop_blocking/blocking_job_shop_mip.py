import sys
sys.path.append('../')

from docplex.mp.model import *
from utils.objects import *
    
def optimize(instance, max_time = 10000, time_limit = 100, threads = 1):
    model = Model('BlockingJobShop')
    start_time = dict()
    duration = dict()
    
    bigm = max_time
    
    # Create variables
    for task in instance.tasks:
        start_time[task] = model.continuous_var()
        duration[task] = model.continuous_var(lb = task.length)
    
    # Precedence and blocking constraints
    for task in instance.tasks:
        if task.next_task:
            model.add(start_time[task.next_task] == duration[task]+start_time[task])
            
    # No overlap constraints
    for machine in instance.machines:
        for t1 in machine.tasks:
            for t2 in machine.tasks:
                if t1.name > t2.name:
                    prec = model.binary_var(name = t1.name+'_precedes_'+t2.name)
                    model.add(start_time[t1] + duration[t1]-bigm*(1-prec) <= start_time[t2])
                    model.add(start_time[t2] + duration[t2]-bigm*prec <= start_time[t1])
            
    # Minimize the makespan
    obj_var = model.continuous_var(0, max_time, 'makespan')
    for task in instance.tasks:
        model.add(obj_var >= start_time[task] + duration[task])
    model.minimize(obj_var)
    
    # Define solver and solve
    model.parameters.timelimit.set(time_limit)
    model.parameters.threads.set(threads)
    sol = model.solve(log_output = True)
    
    solution = Solution(instance)
    
    # Print out solution and return it
    for job in instance.jobs:
        for task in job.tasks:
            print(task.name)
            start = sol.get_value(start_time[task])
            end = start + sol.get_value(duration[task])
            print('Start: %f'%start)
            print('End: %f'%end)
            solution.add(task, start, end)
    return solution

def optimize_and_visualize(instance_name, time_limit = 100, threads = 1):
    reader = Reader(instance_name)
    instance = reader.get_instance()
    solution = optimize(instance, time_limit = time_limit, threads = threads)
    solution.visualize(time_factor = 1, time_grid = 50)
    
if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print('Usage: python %s <instance>'%args[0])
        quit()
    time_limit = 1000
    threads = 1
    if len(args) >= 3:
        time_limit = int(args[2])
    if len(args) >= 4:
        threads = int(args[3])
    optimize_and_visualize(sys.argv[1], time_limit = time_limit, threads = threads)