import numpy as np
import sys

class Data:

    def __init__(self):
        # game info
        self.team_num = 0
        self.game_iter = 0

    def observe(self, preprocess=False):
        """
        read data from stdin
        return: g_history: 1-D np array, start from iter1 to newest
                team_history: 3-D np array, [a][b][c] gets 
                            a_th team at b iteration submit number c(0-1)
        """
        # get team number and game iter
        first_line = [int(i) for i in input().split()]
        game_iter, team_num = first_line[0], first_line[1]
        team_num = int((team_num - 1) / 2)
        self.game_iter = game_iter
        self.team_num = team_num
        # get G history and every team input history
        data = np.array([], dtype=np.float)
        for _ in range(game_iter):
            line = np.fromstring(input(), dtype=np.float, sep='\t')
            data = np.append(data, line)
        data = data.reshape((game_iter, 2 * team_num + 1))
        # extract gold point history
        g_history = data[:,0].reshape((game_iter,))
        # extract team submit history
        team_data = np.transpose(data[:,1:])
        team_history = np.dstack((team_data[::2,:], team_data[1::2, :]))
        return g_history, team_history




if __name__ == "__main__":
    # test for observe()
    line1 = '2 5'
    line2 = '18.07  30  30  17  40'
    line3 = '24.87  18.08   18.08   99.9    25'
    io = Data()
    p1, p2 = io.observe()
    print(p1)
    print(p2)