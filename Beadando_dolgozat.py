import numpy as np

def makespan(mat, job_seq):
  """calculate the makespan of a flow shop by given job order

  Args:
      mat (number[][]): n x m matrix
      job_seq (number[]): n list the order of jobs

  Returns:
      makespan (number): the time to complete all jobs
  """
  n, m = len(mat), len(mat[0])
  costs = np.zeros((n, m), dtype=np.int32)

  # calculate the first row of the cost matrix
  costs[0][0] = mat[job_seq[0]][0]
  for j in range(1, m):
    costs[0][j] = costs[0][j - 1] + mat[job_seq[0]][j]

  # first column of cost matrix
  for i in range(1, n):
    costs[i][0] = costs[i - 1][0] + mat[job_seq[i]][0]

  # the rest of the cost matrix
  for i in range(1, n):
    for j in range(1, m):
      costs[i][j] = max(costs[i][j - 1], costs[i - 1][j]) + mat[job_seq[i]][j]

  # get the makespan
  return costs[-1][-1]