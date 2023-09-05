import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import random
import json
import argparse
import os
import shutil

folder = "../results"
if os.path.exists(folder):
    shutil.rmtree(folder)
os.mkdir(folder)

file_match1 = "../data/match_1.json"
file_match2 = "../data/match_2.json"

df_match1 = pd.read_json(file_match1)
df_match2 = pd.read_json(file_match2)

index_to_action = {0: 'shot', 1: 'dribble', 2: 'rest', 3: 'walk', 4: 'run', 5: 'tackle', 6:'pass', 7:'cross'}


def get_proba_next_action(df):
    """
    Get the probabilities of the next action according to the current one
    df: Dataframe containing all the values
    Return: Dictionnary with the current action and the probabilities of the
    next one
    """
    d = df["label"].tolist()
    final_dict = {}
    for action in range(len(d) - 1):
        current_action = d[action]
        next_action = d[action + 1]
        if current_action not in final_dict:
            final_dict[current_action] = {"count": 1, "next": {next_action: 1}}
        elif next_action not in final_dict[current_action]["next"]:
            final_dict[current_action]["next"][next_action] = 0
        final_dict[current_action]["count"] += 1
        final_dict[current_action]["next"][next_action] += 1

    for key, value in final_dict.items():
        count = value["count"]
        for next_action in value["next"]:
            value["next"][next_action] /= count
    return final_dict


def choose_next_action(next_action_dict):
    """
    Select the next action according to the previous one
    next_action_dict: Dictionnary containing the probability of the next action
    accordong to the previous one
    Return: The next action
    """
    actions = list(next_action_dict.keys())
    action_probs = [next_action_dict[action] for action in actions]
    next_action = np.random.choice(actions, p=action_probs)
    return next_action


def get_mu_sigma_dict(df):
    """
    Get the dictionnary of mean and standard deviation for all the action
    df: Dataframe containing the values
    Return: Dictionnary containing the values of mean and standard deviation
    for all the action
    """
    dict_mu_sigma = {}
    for key, value in index_to_action.items():
        # We get the all the value of a selected action
        data = df[df["label"] == value]["norm"].tolist()
        # We change the number of dimension of the data to 1
        data1dim = [elt for tmp in data for elt in tmp]
        mu, sigma = norm.fit(data1dim)
        action_dict = {"mu": mu, "sigma": sigma, "norm_list": data1dim}
        dict_mu_sigma[value] = action_dict
    return dict_mu_sigma


def get_match(dict_mu_sigma, dict_proba_next_action, match_duration):
    """
    Create the full match using probability. In each iteration we select the
    next action type and we create a norm list according to the action
    dict_mu_sigma: A dictionnary containing the mean and standard deviation of
                   every action norm
    dict_proba_next_action: A dictionnary containing the probability of the
                   next action type according to the previous one
    match_duration: duration of the match (number of norm)
    Return: The final result
    """
    final_result = []
    # The first action is always walk
    current_action = "walk"
    total_acceleration = 0
    while total_acceleration < match_duration:
        # Random size between 0.02s and 3s
        size = random.randint(1, 150)
        total_acceleration += size
        # We calculate the norm according to the mean and standard deviation
        # values
        acceleration_norm = norm.rvs(loc=dict_mu_sigma[current_action]["mu"], scale=dict_mu_sigma[current_action]["sigma"], size=size).tolist()
        # We remove the value < 0
        acceleration_norm = [i for i in acceleration_norm if i > 0]
        new_dict = {"label": current_action, "norm": acceleration_norm}
        final_result.append(new_dict)
        # We select the next action
        current_action = choose_next_action(dict_proba_next_action[current_action]["next"])
    return final_result

def main(nbr_match, time):
    """
    Main function, take the number of match we want to create and to time
    (in second). It will write the result in a file
    """
    for count in range(nbr_match):
        dict_mu_sigma = get_mu_sigma_dict(df_match1)
        dict_proba_next_action = get_proba_next_action(df_match1)
        result_json = get_match(dict_mu_sigma, dict_proba_next_action, time)
        with open(f"../results/match{count}.json", "w") as file:
            json.dump(result_json, file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="create football match")
    parser.add_argument("nbr_match", type=int, nargs='?', default=1)
    parser.add_argument("time", type=int, nargs='?',  default=10)
    args = parser.parse_args()
    if args.nbr_match < 0 or args.nbr_match > 50 or args.time > 90 or args.time < 5:
        print("the number of match should be between 1 and 50 and the duration bewteen 5 and 90 minutes")
    else:
        # Simple cross product
        time_in_hz = args.time * 30000 / 10
        main(args.nbr_match, time_in_hz)
