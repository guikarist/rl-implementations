from collections import defaultdict
from utils.logger import Logger

import numpy as np
import random


class QLearning:

    def __init__(self, env, epsilon, gamma, alpha, log_frequency=100):
        """
        Initialization
        :param env: A initialized gym (or gym-like) environment.
        :param epsilon: Epsilon
        :param gamma: Discounted factor
        :param alpha: Learning rate
        :param log_frequency: The frequency of logging
        """
        self._env = env
        self._epsilon = epsilon
        self._gamma = gamma
        self._alpha = alpha
        self._log_frequency = log_frequency

        # Initialize Q function.
        self._q_func = defaultdict(lambda: np.zeros(self._env.action_space.n))

    def train(self, num_steps):
        rewards = []

        with Logger(num_steps, self._log_frequency, rewards) as logger:
            step_count = 0

            while step_count < num_steps:
                state = self._env.reset()

                reward_sum = 0  # Sum of reward in an episode
                while True:
                    step_count += 1

                    # Select action using epsilon greedy policy.
                    action = self._policy(state)
                    next_state, reward, done, _ = self._env.step(action)
                    reward_sum += reward

                    # Update Q Function using TD target.
                    next_action = np.argmax(self._q_func[next_state])
                    target = reward + self._gamma * self._q_func[next_state][next_action]
                    self._q_func[state][action] += self._alpha * (target - self._q_func[state][action])

                    state = next_state

                    # Logging
                    if step_count % self._log_frequency == 0:
                        logger.update(self._log_frequency)

                    if done or step_count >= num_steps:
                        break
                rewards.append(reward_sum)

    def test(self, num_episodes, render=True):
        rewards = []

        for _ in range(num_episodes):
            state = self._env.reset()
            done = False

            reward_sum = 0
            while not done:
                if render:
                    self._env.render()

                action = np.argmax(self._q_func[state])
                state, reward, done, _ = self._env.step(action)
                reward_sum += reward

            rewards.append(reward_sum)

        print('Avg Reward: %.2f' % (sum(rewards) / len(rewards)))

    def _policy(self, state):
        if random.random() < self._epsilon:
            return self._env.action_space.sample()
        else:
            return np.argmax(self._q_func[state])
