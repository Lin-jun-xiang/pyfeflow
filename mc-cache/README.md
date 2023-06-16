# MonteCarlo-Cache

### Introduction

* Optimizing Monte Carlo Simulation:
    * In the [Monte Carlo section](../mc/), we learned that thousands or even tens of thousands of simulations are often performed. Let's say each simulation takes 1 minute (which is common in transient simulations). If we want to perform 10,000 simulations, it would take nearly 7 days...

    * However, have you ever thought that among these 10,000 simulations, some simulation parameters are repeated hundreds or even thousands of times? In other words, we are repeating the same parameter simulations hundreds or thousands of times in these 10,000.

* Cache concept:
    * In Python, we can use `@lru_cache` to store the parameters and the corresponding results for each function call.
    
    * Every time we perform a simulation, we cache the simulation parameters and results. When we call the simulation function next time, we check if the simulation parameters have appeared before. If they have, instead of performing the simulation again, we directly retrieve the cached result.

    * In the following example, since the simulation parameters 1 and 2 appear twice, we can save two simulation runs using the cache.
        ```python
        
        @lru_cache(maxsize=None)
        def monte_carlo(a):
            print(a, 'simulating...') # suppose the time of simulation spend 1 min...

            return ...

        res = [monte_carlo(parameter) for parameter in [1, 2, 1, 2]]

        """
        1 simulating...
        2 simulating...
        """
        ```

### Demo

* [monteCarlo_cache.py](./monteCarlo_cache.py)