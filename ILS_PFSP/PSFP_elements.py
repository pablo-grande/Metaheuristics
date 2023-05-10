class Job:
    def __init__(self, ID, processing_times, TPT):
        self.ID = ID
        self.processing_times = processing_times
        self.TPT = TPT


class Solution:
    last_ID = -1
    
    def __init__(self, n_jobs, n_machines):
        Solution.last_ID += 1
        self.ID = Solution.last_ID
        self.n_jobs = n_jobs
        self.n_machines = n_machines
        self.jobs = []
        self.makespan = 0.0


    def calculate_makespan(self):
        rows = self.n_jobs
        cols = self.n_machines
        times = [[0 for _ in range(cols)] for _ in range(rows)]
        for column in range(cols):
            for row in range(rows):
                if column == row == 0:
                    times[0][0] = self.jobs[0].processing_times[0]
                elif column == 0:
                    times[row][0] = times[row -1][0] + self.jobs[row].processing_times[0]
                elif row == 0:
                    times[0][column] = times[0][column - 1] + self.jobs[0].processing_times[column]
                else:
                    max_time = max(times[row - 1][column], times[row][column - 1])
                    times[row][column] = max_time + self.jobs[row].processing_times[column]
        return times[rows - 1][cols - 1]
