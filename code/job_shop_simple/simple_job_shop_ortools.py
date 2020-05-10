import sys
sys.path.append('../')

from ortools.sat.python import cp_model
from utils.objects import *
    
def optimize(instance, max_time = 10000, time_limit = 100, threads = 1):
    model = cp_model.CpModel()
    start_vars = dict()
    end_vars = dict()
    durations = dict()
    interval_vars = dict()
    
    # Create variables
    for task in instance.tasks:
        start_vars[task] = model.NewIntVar(0, max_time, 'start' + task.name)
        end_vars[task] = model.NewIntVar(0, max_time, 'end' + task.name)
        durations[task] = task.length
        interval_vars[task] = model.NewIntervalVar(start_vars[task], durations[task], end_vars[task], 'interval' + task.name)
    
    # Precedence and blocking constraints
    for task in instance.tasks:
        if task.next_task:
            model.Add(start_vars[task.next_task] >= end_vars[task])
            
    # No overlap constraints
    for machine in instance.machines:
        for task in machine.tasks:
            model.AddNoOverlap([interval_vars[task] for task in machine.tasks])
            
    # Minimize the makespan
    obj_var = model.NewIntVar(0, max_time, 'makespan')
    model.AddMaxEquality(obj_var, [end_vars[task] for job in instance.jobs for task in job.tasks])
    model.Minimize(obj_var)
    
    # Define solver and solve
    cb = cp_model.ObjectiveSolutionPrinter()
    solver = cp_model.CpSolver()
    #print(dir(solver.parameters)) # I just used this to find the names of the parameters
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = threads
    status = solver.SolveWithSolutionCallback(model, cb)
    
    solution = Solution(instance)
    
    # Print out solution and return it
    for job in instance.jobs:
        for task in job.tasks:
            print(task.name)
            print('Start: %f'%solver.Value(start_vars[task]))
            print('End: %f'%solver.Value(end_vars[task]))
            solution.add(task, solver.Value(start_vars[task]), solver.Value(end_vars[task]))
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