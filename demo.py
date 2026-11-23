"""Small, reproducible educational experiment. See README for limitations."""
import json
from pathlib import Path
import numpy as np

def save(result, output):
    Path(output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result

PROBS=np.array([.15,.22,.30,.38])
def simulate(policy,seed,steps=3000):
    rng=np.random.default_rng(seed); counts=np.zeros(len(PROBS),dtype=int); sums=np.zeros(len(PROBS)); reward=0; regret=0.
    # Pre-generated arm-by-time potential outcomes give policies the same environment seed.
    outcomes=rng.random((steps,len(PROBS)))<PROBS
    for t in range(steps):
        if policy=="random": arm=int(rng.integers(len(PROBS)))
        elif np.any(counts==0): arm=int(np.flatnonzero(counts==0)[0])
        elif policy=="epsilon_greedy": arm=int(rng.integers(len(PROBS))) if rng.random()<.1 else int(np.argmax(sums/counts))
        elif policy=="ucb1": arm=int(np.argmax(sums/counts+np.sqrt(2*np.log(t+1)/counts)))
        else: raise ValueError(policy)
        r=int(outcomes[t,arm]); reward+=r; counts[arm]+=1; sums[arm]+=r
        regret+=float(PROBS.max()-PROBS[arm])
    return {"reward":reward,"pseudo_regret":regret,"arm_counts":counts.tolist()}
def run(output="results.json"):
    result={}
    for policy in ["random","epsilon_greedy","ucb1"]:
        runs=[simulate(policy,s) for s in range(20)]; rewards=np.array([r['reward'] for r in runs]); regrets=np.array([r['pseudo_regret'] for r in runs])
        result[policy]={"mean_reward":float(rewards.mean()),"reward_std":float(rewards.std(ddof=1)),"mean_pseudo_regret":float(regrets.mean()),"regret_std":float(regrets.std(ddof=1)),"per_seed":runs}
    return save({"seeds":list(range(20)),"steps_per_seed":3000,"arm_probabilities":PROBS.tolist(),"policies":result},output)

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
