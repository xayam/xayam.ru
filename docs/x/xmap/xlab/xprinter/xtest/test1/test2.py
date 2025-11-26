import random

rand = random.SystemRandom()
nums = list(range(8))
data = [str(rand.choice(nums)).rjust(1, "0") for _ in range(8)]
s = ""
for d in data:
    s += d
data = int(s)
print(data)
