import numpy as np
import data
import policy

io = data.Data()
# read data from stdin
g_history, team_history = io.observe()

ply = policy.Policy(io.game_iter, io.team_num)
# take policy
sub1, sub2 = ply.predict(g_history, team_history)

# submit
print("{sub1}\t{sub2}".format(sub1=sub1, sub2=sub2))

