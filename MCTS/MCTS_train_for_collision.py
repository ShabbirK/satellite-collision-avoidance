# Train agent for collision at time 6600.

import argparse
import sys
import numpy as np

from simulator import Simulator, read_space_objects
from api import Environment, MAX_FUEL_CONSUMPTION
from MCTS.MCTS import DecisionTree

import pykep as pk

START_TIME = 6599.95
SIMULATION_STEP = 0.0001
END_TIME = 6600.05


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-n_i", "--n_iterations", type=int,
                        default=10, required=False)
    parser.add_argument("-n_s", "--n_steps_ahead", type=int,
                        default=2, required=False)
    parser.add_argument("-start", "--start_time", type=float,
                        default=START_TIME, required=False)
    parser.add_argument("-end", "--end_time", type=float,
                        default=END_TIME, required=False)
    parser.add_argument("-s", "--step", type=float,
                        default=SIMULATION_STEP, required=False)
    parser.add_argument("-save_path", "--save_action_table_path", type=str,
                        default="data/action_table_MCTS.csv", required=False)
    parser.add_argument("-print", "--print_out", type=str,
                        default="False", required=False)

    args = parser.parse_args(args)

    n_iterations, n_steps_ahead = args.n_iterations, args.n_steps_ahead
    start_time, end_time, step = args.start_time, args.end_time, args.step
    save_action_table_path = args.save_action_table_path
    print_out = args.print_out.lower() == "true"

    osc = read_space_objects("data/collision.osc", "osc")
    protected = osc[0]
    debris = [osc[1]]

    max_fuel_cons = MAX_FUEL_CONSUMPTION
    fuel_level = protected.get_fuel()

    action_table = DecisionTree(
        protected, debris, start_time, end_time, step, max_fuel_cons, fuel_level)
    action_table.train(n_iterations, n_steps_ahead, print_out)
    action_table.save_action_table(save_action_table_path)

    return

if __name__ == "__main__":
    main(sys.argv[1:])
