from collections import namedtuple
from queue import Queue

n = 4
k = 5

State = namedtuple("State", ["clock", "is_player_turn"])

def shift(old_state):
    new_clock = old_state.clock[1:] + (old_state.clock[0],)
    return State(clock=new_clock, is_player_turn=new_clock[0] == k)

def player_zero(old_state):
    zeroed_clock = (0,) + old_state.clock[1:]
    return shift(State(clock=zeroed_clock, is_player_turn=old_state.is_player_turn))

def computer_increment(old_state):
    incremented = (old_state.clock[0] + 1,) + old_state.clock[1:]
    return shift(State(clock=incremented, is_player_turn=old_state.is_player_turn))

def is_max(s, cur_pos):
    rotations = [''.join(str(x) for x in reversed(s[i:] + s[:i])) for i in range(n)]
    values = [int(i, k + 1) for i in rotations]
    return max(values) == values[cur_pos]

def is_last(s):
    new_s = (s[0] + 1,) + s[1:]
    if all(i == 0 for i in new_s):
        return True

    i = 0
    while new_s[(i + n - 1) % n] == 0:
        i = (i + n - 1) % n

    return is_max(new_s, i)

def computer_resolve(old_state):
    if old_state.clock == (0,) * n:
        return State(clock=old_state.clock, is_player_turn=True)

    new_state = old_state
    while not new_state.is_player_turn:
        if is_last(new_state.clock):
            new_state = computer_increment(new_state)
        else:
            new_state = State(clock=new_state.clock, is_player_turn=True)
            if new_state.clock[0] == 0:
                new_state = shift(new_state)

    return new_state

def state_to_int(state):
    return int(''.join(str(i) for i in state.clock), k + 1)

def int_to_state(i):
    x = []
    for _ in range(n):
        x.append(i % (k + 1))
        i //= (k + 1)
    return State(clock=tuple(reversed(x)), is_player_turn=True)

def state_after_zero(old_state):
    return computer_resolve(player_zero(old_state))

def state_after_nothing(old_state):
    return computer_resolve(shift(old_state))

original_state = computer_resolve(State(clock=(0, ) * (n - 1) + (1,), is_player_turn=False))

visited = set()
queue = Queue()
queue.put((state_to_int(original_state), ''))

while not queue.empty():
    top, cmd = queue.get()
    if top == 0:
        print(cmd)
        break

    if top in visited:
        continue
    visited.add(top)

    queue.put((state_to_int(state_after_zero(int_to_state(top))), cmd + '0'))
    queue.put((state_to_int(state_after_nothing(int_to_state(top))), cmd + 'X'))
