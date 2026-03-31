from laborix.demo import run_demo

print(run_demo(__import__("pathlib").Path("bandit-output"))["regret"])
