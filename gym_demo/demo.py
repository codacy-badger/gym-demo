#!/usr/bin/env python

"""Usage: gym_demo.py [--steps=NN --no-render --observations] ENV_NAME

Show a random agent playing in a given OpenAI environment.

Arguments:
  ENV_NAME          Name of the Gym environment to run

Options:
  -h --help
  --steps=<STEPS>   How many iteration to run for.  [default: 5000]
  --no-render       Don't render the environment graphically.
  --observations    Print environment observations.

"""
import re
from itertools import zip_longest
from time import sleep
from typing import List, Text

import gym
from docopt import docopt


def get_environment_names() -> List[Text]:
    """Return a list of names of registered Open AI Gym environments."""
    return sorted(spec.id for spec in gym.envs.registry.all())


def get_space_description(space: gym.Space) -> Text:
    """Return a textual description of gym.Space object."""
    description = repr(space)
    if isinstance(space, gym.spaces.Box):
        description += "\nLow values: {0}".format(space.low)
        description += "\nHigh values: {0}".format(space.high)
    return description


def print_environment_description(env: gym.Env) -> None:
    """Output the Gym environment description to standard out."""
    print("Environment: {0}\n".format(env.spec.id))
    print(
        "Observation Space: {0}\n".format(get_space_description(env.observation_space))
    )
    print("Action Space: {0}".format(get_space_description(env.action_space)))
    if hasattr(env.unwrapped, "get_action_meanings"):
        print("Action meanings:", env.unwrapped.get_action_meanings())
    print("\n")


def list_to_columns(strings: List[Text]) -> Text:
    """Prepare multi-column output string from a list of strings."""
    strings_in_columns = ""
    for col1, col2, col3 in zip_longest(
        strings[::3], strings[1::3], strings[2::3], fillvalue=""
    ):
        strings_in_columns += "{0:<50}{1:<50}{2:<}\n".format(col1, col2, col3)
    return strings_in_columns


def run_environment(
    env: gym.Env,
    steps_count: int = 1000,
    render: bool = True,
    print_observation: bool = False,
) -> None:
    """Execute main environment run loop.

    Renders environment state graphically and outputs environment information to
    standard out.

    :param env: the environment to run
    :param steps_count: how many steps to run for?
    :param render: should the environment be rendered graphically?
    :param print_observation: should the full observed state be output to std out?
    """
    env.reset()
    print("Running environment demonstration...")
    print("Unique environment information is output to standard out:")
    prev_env_output = None
    for step in range(steps_count):
        observation, reward, done, info = env.step(env.action_space.sample())

        if render:
            env.render()
            sleep(0.01)

        if (reward, done, info) != prev_env_output:
            print("Reward: {0}, Done: {1}, Info: {2}".format(reward, done, info))
            prev_env_output = (reward, done, info)

        if print_observation:
            print("Observation: {0}".format(observation))

        if done:
            break

    env.close()


def main() -> None:
    """Process script argument and run."""
    environment_names = get_environment_names()

    help_string = "{0}\n\nAvailable environments:\n\n{1}".format(
        __doc__, list_to_columns(environment_names)
    )
    arguments = docopt(help_string)

    steps = int(arguments.get("--steps"))
    render_env = not arguments.get("--no-render")
    print_observations = arguments.get("--observations")
    env_name = arguments.get("ENV_NAME")

    if env_name in environment_names:
        environment = gym.make(env_name)
        print_environment_description(environment)
        run_environment(environment, steps, render_env, print_observations)

    else:
        print("ERROR: Environment with requested ID not found.")
        regex = re.compile(".*{0}.*".format(env_name), re.IGNORECASE)
        environment_names = [
            spec.id for spec in gym.envs.registry.all() if regex.match(spec.id)
        ]
        if len(environment_names):
            print("\nPerhaps you were looking for:")
            print(list_to_columns(environment_names))


if __name__ == "__main__":
    main()
