import sys
sys.path.append('../')

from docplex.cp.model import *
from utils.objects import *
    
def optimize(instance, max_time = 10000, time_limit = 100, threads = 1):
    model = CpoModel('BlockingJobShop')
    interval_vars = dict()
    
    # Create variables
    for task in instance.tasks:
        interval_vars[task] = interval_var(start = (0, max_time), end = (0, max_time), size = (task.length, max_time), name = 'interval'+str(task.name))
    
    # Precedence and blocking constraints
    for task in instance.tasks:
        if task.next_task:
            model.add(start_of(interval_vars[task.next_task]) == end_of(interval_vars[task]))
            
    # No overlap constraints
    for machine in instance.machines:
        machine_sequence = sequence_var([interval_vars[task] for task in machine.tasks])
        model.add(no_overlap(machine_sequence))
            
    # Minimize the makespan
    obj_var = integer_var(0, max_time, 'makespan')
    for task in instance.tasks:
        model.add(obj_var >= end_of(interval_vars[task]))
    model.minimize(obj_var)
    
    # Define solver and solve
    sol = model.solve(TimeLimit= time_limit, Workers = threads)
    
    solution = Solution(instance)
    
    # Print out solution and return it
    for job in instance.jobs:
        for task in job.tasks:
            print(task.name)
            start = sol.get_value(interval_vars[task])[0]
            end = sol.get_value(interval_vars[task])[1]
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