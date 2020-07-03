# JSGame

File is at `pref-max--game.html`. Solution is at `a.py`.

While you can solve this mathematically (I kind of did that by noticing that
you can increase the number, read counter-clockwise, until 2222 and then
reducing them to 0000), I am going to propose an alternate solution.

Basically, model this game as a graph, where the nodes are the states of the game
and the edges connect two nodes if you can bring a state to the other by a
player move (and possibly a number of computer moves). Once you have done this,
you can run the breadth-first search algorithm and traverse through the state
space.

We start by defining the constants, as well as what a state is:
```python
n = 4
k = 2

State = namedtuple("State", ["clock", "is_player_turn"])
```

Here, `clock` is a tuple of `n` elements which represents the numbers in the
clock, starting from the current clock hand, clockwise. `is_player_turn` is a
boolean which is `True` if and only if it is the current player's turn.

The next few functions are copied from the implementation. In retrospect,
using Javascript would have been faster as you can just use the implementations
in the HTML file itself.
```python
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
```

The hardest part is to define what the next state is after a series of computer
movements:
```python
def computer_resolve(old_state):
    if old_state.clock == (0,):
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
```

The next part is just some convenience functions. `state_to_int` and
`int_to_state` is useful to "pack" the state into an integer, so that it can
be hashed faster. I suppose you can actually just dump the `State` object into
the visited set later, but oh well.
```python
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
```

Finally, the breadth first search algorithm. The original state is whatever
that has been resolved by the computer from the initial state of `(0, 0, 0, 1)`.
```python
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

```

Basically, in the queue, we store the state of the game (represented as an
integer), as well as the series of commands to reach that state from the
beginning (where `X` is doing nothing and `0` is putting zero).

Running this will give `0XXX000X0XXX00XXX0XXXXX0XXX00XXX0XXXXX0XXXXX0000`
which, indeed, corresponds to the shortest sequence of moves to win the game.
This approach might be better if you are more inclined to programming.

As a bonus, since this code is general enough (I abstracted the `k` and `n`
variable away since I am doing this after the CTF so I have plenty of time :p)
we can change `n` and `k` to a big number and get the solution as well: with
`k = 5` and `n = 4` the solution is
```
0XXX000X0XXX00XXX0XXXXX0XXX00XXX0XXXXX0XXXXX000XX0XXXXX0XXXXX00XXXXX0XXXXXXXX0XXXXXXXX0XXX00XXXXX0XXXXXXXX0XXXXXXXX0XXXXXX00XXXXX0XXXXXXXX0XXXXXXXX0XXXXXXXX000XXX0XXXXXXX0XXXXXXX0XXXXXXX00XXXXXXX0XXXXXXXXXXX0XXXXXXXXXXX0XXXXXXXXXXX0XXX00XXXXXXX0XXXXXXXXXXX0XXXXXXXXXXX0XXXXXXXXXXX0XXXXXX00XXXXXXX0XXXXXXXXXXX0XXXXXXXXXXX0XXXXXXXXXXX0XXXXXXXXX00XXXXXXX0XXXXXXXXXXX0XXXXXXXXXXX0XXXXXXXXXXX0XXXXXXXXXXX000XXXX0XXXXXXXXX0XXXXXXXXX0XXXXXXXXX0XXXXXXXXX00XXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0XXX00XXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0XXXXXX00XXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXX00XXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXX00XXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0XXXXXXXXXXXXXX0000
```

You can convince yourself that it is true :)
