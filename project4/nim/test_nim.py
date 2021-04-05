import pytest

from nim import NimAI, Nim


def test_get_q_value_in_dict():
    player = NimAI()
    player.q = {((1, 1, 3, 5), (3, 1)): 0.48}
    state = [1, 1, 3, 5]
    action = (3, 1)
    assert player.get_q_value(state, action) == 0.48


def test_get_q_value_not_in_dict():
    player = NimAI()
    state = [1, 1, 3, 5]
    action = (3, 1)
    assert player.get_q_value(state, action) == 0


def test_best_future_reward_no_actions():
    player = NimAI()
    state = [0, 0, 0, 0]
    reward = player.best_future_reward(state)
    assert reward == 0


def test_best_future_reward_all_negative():
    player = NimAI()
    state = [0, 2, 2, 0]
    player.q = {
        ((0, 2, 2, 0), (1, 1)): -0.25,
        ((0, 2, 2, 0), (1, 2)): -0.50,
        ((0, 2, 2, 0), (2, 1)): -0.75,
        ((0, 2, 2, 0), (2, 2)): -0.99
    }
    reward = player.best_future_reward(state)
    assert reward == -0.25


def test_best_future_reward_positive():
    player = NimAI()
    state = [0, 1, 2, 0]
    player.q = {
        ((0, 1, 2, 0), (1, 1)): 0.25,
        ((0, 1, 2, 0), (2, 1)): 0.75,
        ((0, 1, 2, 0), (2, 2)): 0.99
    }
    reward = player.best_future_reward(state)
    assert reward == 0.99


def test_best_future_reward_missing_key():
    player = NimAI()
    state = [0, 2, 2, 0]
    player.q = {
        # ((0, 2, 2, 0), (1, 1)): -0.25,
        ((0, 2, 2, 0), (1, 2)): -0.50,
        ((0, 2, 2, 0), (2, 1)): -0.75,
        ((0, 2, 2, 0), (2, 2)): -0.99
    }
    reward = player.best_future_reward(state)
    assert reward == 0


def test_update_q_value():
    player = NimAI()
    player.q = {
        ((1, 1, 3, 5), (3, 1)): 0.48,
        ((1, 1, 3, 4), (0, 1)): 0.5080425738634211,
        ((0, 1, 3, 4), (3, 2)): 0.999969482421875
    }
    state = [1, 1, 3, 5]
    action = (3, 1)
    old_q = player.get_q_value(state, action)
    # most likely action taken by other player
    # ((1, 1, 3, 4), (0, 1)): 0.5080425738634211
    # so we find ourselves in new_state = [0, 1, 3, 4]
    # for which the best action is
    # ((0, 1, 3, 4), (3, 2)): 0.999969482421875
    future_rewards = 0.999969482421875
    player.update_q_value(state,
                          action,
                          old_q,
                          reward=0,
                          future_rewards=future_rewards)
    # Q(s, a) <- old value estimate
    #                + alpha * (new value estimate - old value estimate)
    expected_q_value = old_q + (player.alpha * (future_rewards + 0 - old_q))
    key = (tuple(state), action)
    assert player.q[key] == expected_q_value


def test_choose_action_explore():
    player = NimAI()
    state = [0, 1, 2, 0]
    player.q = {
        ((0, 1, 2, 0), (1, 1)): 0.25,
        ((0, 1, 2, 0), (2, 1)): 0.75,
        ((0, 1, 2, 0), (2, 2)): 0.99
    }
    # what's the right way to test randomness?
    action = player.choose_action(state, epsilon=True)
    assert action in {(1, 1), (2, 1), (2, 2)}

def test_choose_action_exploit():
    player = NimAI()
    state = [0, 1, 2, 0]
    player.q = {
        ((0, 1, 2, 0), (1, 1)): 0.25,
        ((0, 1, 2, 0), (2, 1)): 0.75,
        ((0, 1, 2, 0), (2, 2)): 0.99
    }
    action = player.choose_action(state, epsilon=False)
    assert action == (2, 2)