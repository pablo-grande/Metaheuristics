import operator

from time import time

from PSFP_elements import Job, Solution



def timeit(func):
    def wrap_func(*args, **kwargs):
        print(f"{args[1]} jobs and {args[2]} machines")
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} computation time: {(t2-t1):.4f}s')
        return result
    return wrap_func


def read_instance(instance_name):
    file_name = f"data/{instance_name}_inputs.txt"
    jobs, n_jobs, n_machines = [], 0, 0
    with open(file_name) as instance:
        i = -3
        for line in instance:
            if i == -3: pass
            elif i == -2:
                n_jobs = int(line.split()[0])
                n_machines = int(line.split()[1])
            elif i == -1: pass
            else:
                data = [float(x) for x in line.split("\t")]
                jobs.append(Job(i, data, sum(data)))
            i += 1
    return jobs, n_jobs, n_machines


def calc_QMatrix(solution, k):
    rows = k + 1
    cols = n_machines
    q = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(k, -1, -1):
        for j in range(n_machines - 1, -1, -1):
            if i == k:
                q[k][j] = 0
            elif i == k-1 and j == n_machines - 1:
                q[k-1][n_machines-1] = solution.jobs[k-1].processing_times[n_machines-1]
            elif j == n_machines - 1:
                q[i][n_machines - 1] = q[i+1][n_machines-1] + solution.jobs[i].processing_times[n_machines-1]
            elif i == k - 1:
                q[k-1][j] = q[k-1][j+1] + solution.jobs[k-1].processing_times[j]
            else:
                max_time = max(q[i+1][j], q[i][j+1])
                q[i][j] = max_time + solution.jobs[i].processing_times[j]
    return q


def calc_FMatrix(solution, k, e):
    rows = k + 1
    cols = n_machines
    f = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(k+1):
        for j in range(n_machines):
            if i == j == 0:
                f[0][0] = solution.jobs[k].processing_times[0]
            elif j == 0:
                f[i][0] = e[i -1][0] + solution.jobs[k].processing_times[0]
            elif i == 0:
                f[0][j] = f[0][j - 1] + solution.jobs[k].processing_times[j]
            else:
                max_time = max(e[i - 1][j], f[i][j - 1])
                f[i][j] = max_time + solution.jobs[k].processing_times[j]
    return f


def calc_EMatrix(solution, k):
    rows = k
    cols = n_machines
    e = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(k):
        for j in range(n_machines):
            if i == j == 0:
                e[0][0] = solution.jobs[0].processing_times[0]
            elif j == 0:
                e[i][0] = e[i -1][0] + solution.jobs[i].processing_times[0]
            elif i == 0:
                e[0][j] = e[0][j - 1] + solution.jobs[0].processing_times[j]
            else:
                max_time = max(e[i - 1][j], e[i][j - 1])
                e[i][j] = max_time + solution.jobs[i].processing_times[j]
    return e



def improve_by_shifting_job_to_left(solution, k):
    best_position = k
    min_makespan = float("inf")
    e_matrix = calc_EMatrix(solution, k)
    q_matrix = calc_QMatrix(solution, k)
    f_matrix = calc_FMatrix(solution, k, e_matrix)
    for i in range(k, -1, -1):
        max_sum = 0.0
        for j in range(solution.n_machines):
            new_sum = f_matrix[i][j] + q_matrix[i][j]
            if new_sum > max_sum: max_sum = new_sum
        new_makespan = max_sum
        if new_makespan <= min_makespan:
            min_makespan = new_makespan
            best_position = i

    if best_position < k:
        job = solution.jobs[k]
        for i in range(k, best_position, -1):
            solution.jobs[i] = solution.jobs[i-1]
        solution.jobs[best_position] = job
    if k == solution.n_jobs -1:
        solution.makespan = min_makespan
    return solution


@timeit
def neh(jobs, n_jobs, n_machines):
    jobs.sort(key=operator.attrgetter("TPT"), reverse=True)
    solution = Solution(n_jobs, n_machines)
    for index in range(n_jobs):
        solution.jobs.append(jobs[index])
        solution = improve_by_shifting_job_to_left(solution, index)
    print(f"NEH makespan with Taillard acceleration {solution.makespan:.2f}")
    print(f"NEH verification with traditional method: {solution.calculate_makespan():.2f}")


instances = ["tai117_500_20", "tai079_100_10", "tai044_50_10", "tai002_20_5"]
for instance in instances:
    print(f"Instance {instance}")
    jobs, n_jobs, n_machines = read_instance(instance)
    neh(jobs, n_jobs, n_machines)
    print(f"Solution: {[str(job.ID) for job in jobs]}\n")
