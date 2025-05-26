"""
score.py
"""

class Score:
    def __init__(self):
        self.value = 0

    def increment(self, amount=100):
        self.value += amount
        print(f"Score: {self.value}")

    def reset(self):
        self.value = 0
        print("Score reset.")
        
score = Score()

def euclidean_rhythm(pulses, steps):
    if pulses < 0 or steps <= 0:
        raise ValueError("`pulses` must be >= 0 and `steps` must be > 0")
    if pulses > steps:
        raise ValueError("`pulses` cannot exceed `steps`")
    if pulses == 0:
        return [0] * steps
    if pulses == steps:
        return [1] * steps

    counts = []
    remainders = [pulses]
    divisor = steps - pulses
    level = 0

    while True:
        counts.append(divisor // remainders[level])
        remainders.append(divisor % remainders[level])
        divisor = remainders[level]
        level += 1
        if remainders[level] <= 1:
            break
    counts.append(divisor)

    def build(level):
        if level == -1:
            return [0]
        if level == -2:
            return [1]
        pattern = []
        for i in range(counts[level]):
            pattern += build(level - 1)
        if remainders[level] != 0:
            pattern += build(level - 2)
        return pattern

    pattern = build(level)
    pattern.reverse()
    return pattern[:steps]


def check_rhythm(input_sequence, pattern):
    if input_sequence == pattern:
        score.increment()
        return True
    return False


if __name__ == "__main__":
    pattern = euclidean_rhythm(5, 8)
    print("Pattern:", pattern)
    test_seq = [0, 1, 1, 0, 1, 1, 0, 1]
    # test_seq = [1, 0, 0, 1, 0, 0, 1, 0] # 3,8
    # test_seq = [1, 0, 1, 0, 1, 0, 1, 0] # 4,8
    print("Match:", check_rhythm(test_seq, pattern))
    print("Final score:", score.value)
