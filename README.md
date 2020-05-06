# epibench
The evolution of the 2019–20 coronavirus pandemic has made clear the need to quickly contain the outbreaks of infections. One of the strategies used is to trace the contacts of people found positive and quickly isolate the new found infected. Governments and institutions are working to implement contact tracing through IT technologies and mobile apps. The purpose of this repository is to provide a common database where inference algorithms can be tested. The inference problems addressed rely on having detailed contact information among individuals observed. We assume that compartmental models (like SIS, SIR, SEIR etc..) govern the viral propagation through the population. We provide several benchmark instances for different inference problems.

## Inference problems

We provide a database of instances to address the following inference problems:

1. **Infer the current state of the individuals from partial observations.** The temporal list of contacts between individuals is known. A list of partial observations of the past state of individuals generate from simulated cascades are provided. The compartmental model that generates the epidemic cascade could be known or not. We want to infer the current states of individuals (at the last time of the dynamics) in order to identify the infected one among not yet tested individuals.

1. **Patient zero problem.** The temporal list of contacts between individuals is known. A list of partial observations of the state of individuals generated from simulated cascades is provided.  The compartmental model that generates the epidemic cascade is known. We want to infer the sources of the partially observed epidemic outbreak.

1. **Inferring the parameter of the compartmental models** The temporal list of contacts between individuals is known. A list of partial observation of the state of individuals are provided. We want to infer the parameters of the compartmental model that generates the epidemic cascade.

1. More coming...

## Using the data

The data format is specified in the [README](./data/README.md) in the folder ```./data/```

For reference and for convenience, a Python script can be found in the `lib` folder which can be used to save and load the different instances.

## Results
In the folder ```results``` are the results obtained by various techniques on the instances proposed. If you want to add yours  make a pull request or write us: [sybil-team](mailto:sibylteam@gmail.com?subject=[GitHub]%20Source%20epibench).

### list of results:
* OpenABM instances: 
    * T_25: [results](results/OpenABM/T_25/results.ipynb) of [sib]() and local tracing algorithm.
    * T_35: [results]() of [sib](results/OpenABM/T_35/results.ipynb) and local tracing algorithm.


## Credits:

1. The instances of ```OpenABM``` are generated with [OpenABM]() github repository gently provided by [Luca Ferretti](https://www.bdi.ox.ac.uk/Team/luca-ferretti).


## Mainteiners:
[sybil-team](https://github.com/sibyl-team)
