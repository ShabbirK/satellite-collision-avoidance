
import pykep as pk
import numpy as np
import pandas as pd


class TableAgent:
    """ Agent implements an agent to communicate with space Environment.

        Agent can make actions to the space environment by taking it's state
        after the last action.

    """

    def __init__(self, table_path="actions_table.csv"):
        """
        Args:
            table_path (str): path to table of actions (.csv).

        """
        self.table = pd.read_csv(table_path, index_col=0).values

    def get_action(self, state):
        """ Provides action for protected object.

        Args:
            state (dict): environment state
                {'coord' (dict):
                    {'st' (np.array with shape (1, 6)): satellite r and Vx, Vy, Vz coordinates.
                     'debr' (np.array with shape (n_items, 6)): debris r and Vx, Vy, Vz coordinates.}
                'trajectory_deviation_coef' (float).
                'epoch' (pk.epoch): at which time environment state is calculated.
                'fuel' (float): current remaining fuel in protected SpaceObject. }.

        Returns:
            action (np.array([dVx, dVy, dVz, pk.epoch, time_to_req])): vector of deltas for
                protected object, maneuver time and time to request the next action.

        """
        epoch = state["epoch"].mjd2000
        print(epoch)
        action = np.array([0, 0, 0, epoch, 0])  # : default action
        if self.table.size:
            if (epoch >= self.table[0, 0]):
                action = np.hstack(
                    [self.table[0, 1:], epoch, 0])
                print("maneuver!:", action)
                self.table = np.delete(self.table, 0, axis=0)
        return action


class Agent:

    """ Agent implements an agent to communicate with space Environment.
    Agent can make actions to the space environment by taking it's state
    after the last action.
    """

    def __init__(self):
        """"""

    def get_action(self, state):
        """ Provides action for protected object.
        Args:
            state (dict): environment state
                {'coord' (dict):
                    {'st' (np.array with shape (1, 6)): satellite r and Vx, Vy, Vz coordinates (meters).
                     'debr' (np.array with shape (n_items, 6)): debris r and Vx, Vy, Vz coordinates (meters).}
                'trajectory_deviation_coef' (float).
                'epoch' (pk.epoch): at which time environment state is calculated.
                'fuel' (float): current remaining fuel in protected SpaceObject. }
        Returns:
            action (np.array([dVx, dVy, dVz, pk.epoch, time_to_req])):
                vector of deltas for protected object (m/s),
                maneuver time (mjd2000) and step in time
                when to request the next action (mjd2000).
        """
        dVx, dVy, dVz = 0, 0, 0  # m/s
        epoch = state["epoch"].mjd2000
        time_to_req = 0.001  # mjd2000
        action = np.array([dVx, dVy, dVz, epoch, time_to_req])

        return action
