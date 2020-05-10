# Job Shop Scheduling

Walter Sebastian Gisler
May 9, 2020

## Motivation

Job shop scheduling problems are complicated combinatorial problems. They are widely studied and real life examples are present in manufacturing companies, rail road scheduling, sports scheduling etc. No efficient optimal methods exist and normally heuristics are used to find quality solutions quickly.

Constraint programming solvers have also been used widely. They allow rapid prototyping and fast adjustments of the code to meet varying real life constraints, which is often more challenging with custom built heuristics.

I have been using CpOptimizer, which is distributed as part of the IBM Cplex Studio almost exclusively for scheduling problems that have elements of job shop scheduling problems. However, CpOptimizer is expensive, which is why alternatives are needed. It is hard to compare constraint programming solvers, because they don't use a common input format (like for example MIP solvers). That makes benchmarking them more challenging, because it means that for each of them, a custom model has to be written (unless you use MiniZinc, but even that doesn't support all solvers). I therefore decided to implement some common problems, for which benchmarking instances exist using CpOptimizer and other, freely available optimizers.

## What is the job shop scheduling problem?

A job shop scheduling problem consists of sequencing a number of jobs on different machines. Each job consists of a number of tasks that have to be processed in a given order. Each task has a given duration and a machine on which it has to be processed.

Typically, we want to minimize the total time that is needed to complete all jobs. There is an exponential number of possible solutions, and the problem is NP-complete.

For this benchmarking, we are considering two types of job shop scheduling problems:
- Simple job shop scheduling problem: the normal case
- Blocking job shop scheduling problem: there is no room to store jobs between machines. This implies, that a task that is completed is blocking the machine it is on until it is moved to the next machine

Simple job shop solution: abz5
![](doc/simple.png)

Blocking job shop solution: abz5 (blocking operations are dotted)
![](doc/blocking.png)

### Variations

Various variations and extensions of the job shop scheduling problem exist, for example job shop scheduling with sequence dependent setup times, flexible job shop scheduling problems (with a choice of >= 1 machines for each task) etc.

## Benchmarking instances

The benchmarking instances are commonly known instances that are widely used in literature. I took the from the following repository: https://github.com/tamy0612/JSPLIB

The format can be read as follows:

- Line comments start with a hashtag: # this is a comment
- The first line that is not a comment in each instance file contains the number of jobs and the number of machines
- Each following line after that represents a job. Each job is made up of tuples of numbers. Each tuple is representing a task and the tasks are in the order they are supposed ot be processed in. The first number of task tuple defines which machine a job is supposed to be processed on and the second tuple gives the duration of each task

## Structure of this repository

- readme.md: this document
- instances.json: overview of all instances
- instances/ : for each instance, there is a file in this folder
- code/benchmarking: code to run the benchmarking automatically
- code/job_shop_blocking: code for blocking job shop
- code/job_shop_simple: code for the simple job shop
- code/utils/: code to read and visualize instances and represent the data in a unified way, furthermore, this folder also contains a script to generate visually distinct colors, which can be used to visualize the solutions in a visually appealing Gantt-chart

## Solvers

- CpOptimizer: https://www.ibm.com/analytics/cplex-cp-optimizer
- OR-Tools: https://developers.google.com/optimization

## Benchmarking setup

For every instance, we run a series of experiments. Every experiment is repeated 3 times to get an average and worst and best case scenario:

Thread configurations:
- 1 thread
- 2 threads
- 4 threads
- 8 threads

Time limits:
- 10 seconds
- 20 seconds
- 1 minute
- 2 minutes

## Results