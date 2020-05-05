# Data format for the files

Each folder contains a different sets of instances of epidemies.

## File list

- `epidemy.gz`: configuration of the system at every discrete time, compressed with gzip.  
- `contacts.gz`: The contact matrix, in CSV format, compressed with gzip
- `obs_[n].gz`: Contains a set of partial observations of the individuals, in CSV format, compressed with gzip.

- `parameters.json`: This JSON file lists all the parameter which were used in the creation of the epidemies

## Description of each type of data

  

### Epidemy files

An epidemy is given as a matrix, where each row represents a successive time instant, and each column corresponds to a node, starting from 0.

The status of each node at each time instant is encoded with a number, 0 corresponding to Susceptible, 1 to Infected, 2 to Recovered

The epidemies are given both in CSV format.

### Observations

The observations are given in CSV.

Each row represents an observation, of node "i", at time "t_test", with state 'state'.

### Contacts

The contacts are in form of a matrix, each row corresponding to a single contact, and each element/column corresponding, in order, to (the contacts are considered directed (origin->target):

- time of contact

- origin node of contact

- target node of contact

- probability of infection of the contact
