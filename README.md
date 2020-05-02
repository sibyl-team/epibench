# epibench
The evolution of the 2019–20 coronavirus pandemic has made clear the need to quickly contain the outbreaks of infections. One of the strategies used is to trace the contacts of people found positive and quickly isolate the new infected founds. Governments and institutions are working to implement contact tracking through IT technologies and mobile apps. The purpose of this repository is to provide a common database where inference algorithms can be tested. The inference problems addressed rely on having detailed contacts information among individuals observed. We assume that compartmental models (like SIS, SIR, SEIR etc..) govern the dynamics of the systems. We provide several different instances for several different inference problems.

## inference problems

We provide a database of instances to address the following inference problems:

1. **Infer the current state of the individuals from partial observations.** The temporal list of contacts between individuals is known. A list of partial observations of the past state of individuals generate from simulated cascades are provided. The compartmental model that generate the epidemics cascade could be known or not. We want to infer the current states of individuals (at the last time of the dynamics) in order to identify the infected not yet tested.

1. **Patient zero problem.** The temporal list of contacts between individuals is known. A list of partial observations of the state of individuals generate from simulated cascades are provided.  The compartmental model that generate the epidemics cascade is known. We want to infer the sources of the epidemic observed.

1. **Inferring the parameter of the compartmental models** The temporal list of contacts between individuals is known. A list of partial observation of the state of individuals are provided. We want to infer the parameters of the compartmental model that generates the epidemic cascade.

1. More coming...

## Database structures

See the [README](./data/README.md) in the folder ```./data/```

## Credits:

1. The contacts lists of i_bird_days_20 is derived from: ...
2. The contacts lists of sp_work13 is derived from the work: ....