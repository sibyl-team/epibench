# Data format for the files

  

Each folder contains a different network and instances of the epidemies, with different data formats and encoding.

  

## File list

  

- all_epid.npz: Epidemies of all the instances in compressed Numpy Array format

  

- all_obs.json.bz2: All the observations of all the instances, in a json compressed with bzip2

  

- contacts.csv.bz2: The contact matrix, in CSV format, compressed with bzip2

  

- instance_nnn.tar.bz2: This bzip2 archive contains the observation and the epidemy of the instance 'nnn', in CSV format

  

- parameters.json: This JSON file lists all the parameter which were used in the creation of the epidemies

  

## Description of each type of data

  

### Epidemy files

  

An epidemy is given as a matrix, where each row represents a successive time instant, and each column corresponds to a node, starting from 0.

  

The status of each node at each time instant is encoded with a number, 0 corresponding to Susceptible, 1 to Infected, 2 to Recovered

  

The epidemies are given both in CSV format, inside each instance_iii.tar.bz2 archive, or packed all together in a npz compressed Numpy Array.

  

### Observations

  

The observations are given in CSV, inside each instance_iii.tar.bz2.

Each row represents an observation, of node i, at time t, with state 'obs'.

  

For convenience, they are also packed all together in a bzip2-compressed JSON file, in a nested tree structure, whose keys represent in the following order: instance -> state of observation (S, I or R) -> time of observation -> list of nodes with that state.

  

### Contacts

  

The contacts are in form of a matrix, each row corresponding to a single contact, and each element/column corresponding, in order, to:

  

- time of contact

- origin node of contact

- target node of contact

- probability of infection of the contact
