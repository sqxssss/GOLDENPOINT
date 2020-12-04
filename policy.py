import numpy as np
import random

class Policy:

    def __init__(self, game_iter, team_num):
        # basic game info
        self.game_iter = game_iter
        self.team_num = team_num
        # param setting for all policies
        self.regard_disturb = 30
        self.ma_window_size = 3
        self.check_window = 5

    def __basic_average__(self, arr):
        """
        param: 1-D np array float type
        return average
        """
        return np.sum(arr) / len(arr)

    def __moving_average__(self, arr):
        """
        param: 1-D np array float type
        return estimated moving average(float)
        """
        if len(arr) > self.ma_window_size:
            window = np.ones(self.ma_window_size) / self.ma_window_size
            results = np.convolve(arr, window, mode='valid')
            results = self.__basic_average__(results)
        else:
            # if window size is bigger than arr
            # then just calculate avg of array 
            results = self.__basic_average__(arr)
        return results

    def __check_fluct__(self, g_history):
        g_check = g_history[-self.check_window:]
        max_g = np.max(g_check)
        min_g = np.min(g_check)
        bias = max_g - min_g
        return bias

    def moving_avg(self, g_history, team_history):
        """
        calculate estimated g using moving average alg.
        """
        return self.__moving_average__(g_history)

    def moving_exp_avg(self, g_history, team_history):
        """
        calculate ema using expotionential moving average
        """
        ema = g_history[0]
        alpha = 2. / (self.game_iter + 1)
        for iter in range(1, self.game_iter):
            ema = ema + alpha * (g_history[iter] - ema)
        return ema

    def random_fluctuation(self, pred, max_bias, exp_mea):
        """
        generate 2 numbers:
            one for disturbing the avg,
            the other for prediction
        """
        random_up_limit  = 40
        if max_bias < 2:
            random_float = random.uniform(10, random_up_limit)
            if pred < 50:
                disturb = pred + random_float
            else:
                disturb = pred - random_float
        else:
            # means no team is disturbing the data, we take risk
            disturb = exp_mea
        # set disturbing number
        # modify pred to fit the disturbing
        pred_modify = pred + (disturb - pred) / (self.team_num * 2) * 0.618
        return disturb, pred_modify

    def __detect_fluct__(self, g_history, team_history):
        """
        model every team's disturbing strategy
        goal: not be the last one
        """
        # get every iteration max offset, excluding first 20 iterations
        g_trans = g_history.reshape((1, len(g_history), 1))
        if self.game_iter > 30:
            bias = np.absolute(team_history - g_trans)[:,-20:]
        else:
            bias = np.absolute(team_history - g_trans)
        # get numbers which appear in every team max offset
        max_bias = np.amax(bias, axis=2).flatten()
        # some team will not use disturbing strategy, filter out
        filter_bias = max_bias[max_bias > self.regard_disturb]
        # get the average maxium offset, make sure the random disturbing
        # is under this average -- try not be the last one
        if len(filter_bias) == 0:
            avg_bias = 0
        else:
            avg_bias = np.sum(filter_bias) / len(filter_bias)
        return avg_bias

    def predict(self, g_history, team_history):
        """
        give final two numbers, should be called
        """
        # first submit
        if len(g_history) == 0:
            return 35., 15.
        # later submit
        else:
            #pred = self.moving_exp_avg(g_history, team_history)
            pred = self.moving_avg(g_history, team_history)
            exp_ema = self.moving_exp_avg(g_history, team_history)
            max_bias = self.__check_fluct__(g_history)
            return self.random_fluctuation(pred, max_bias, exp_ema)

