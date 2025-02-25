
#Random Sampling
print("=" * 45)
print("Random Sample Example")
import numpy as np

#setup generator for reproducibility

random_generator = np.random.default_rng(2020)

population = np.arange(1, 10 + 1)

sample = random_generator.choice(
    population, #sample from population
    size = 3, #number of samples to take
    replace=False #only allow to sample individuals once
)

print(f"numpy array: {sample}")
print("=" * 45)
print("Stratified Random Sample Example")

#setup generator for reproducibility
random_generator = np.random.default_rng(2020)
population = [
    1, "A", 3, 4,
    5, 2, "D", 8,
    "C", 7, 6, "B"
]

#group strata
strata = {
    'number' : [],
    'string' : []
}

for item in population:
    if isinstance(item, int):
        strata["number"].append(item)
    else:
        strata["string"].append(item)

#fraction of population to sample
sample_fraction = 0.5

#random sample from strata

sampled_strata = {}

for group in strata:
    sample_size = int(
        sample_fraction * len(strata[group])
    )
    sampled_strata[group] = random_generator.choice(
        strata[group],
        size=sample_size,
        replace=False
    )

print(f"Random Sampled Strata: {sampled_strata}")
