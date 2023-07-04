# Google Maps Directions Analysis

### Do directions provided by Google Maps have a bias against walking?

The goal is to find trips where google provides a path that uses **few walking** but is actually **longer than necessary** (e.g. it prefers to walk very few to **a closeby subway station**, but then spend a lot of time on the subway, than walking to **a slighly more distant station** that gets you to the destination quicker). After building the dataset, we will attempt to do the following:

- [ ] Estimate google's path-cost formula (e.g. if "time_walking * weight_walking + time_transport" then what is the value that google uses for "weight_walking"?)
- [ ] Implement the transportation network as a graph and check if google is ignoring stations far away from start when computing the shortest paths
- [ ] Implement a walking-and-transportation graph and planner that priviledges walking (provides better routes on your dataset)


## TODOs

- [x] Create classes for storing directions
- [x] Connect to Google Maps API
- [ ] Implement Network X
- [ ] Update `environment.yml`

## Environment

Create the environment
```
    
    $ conda env create -f environment.yml # conda environment

    $ conda create -n gm_analysis python=3.11.0  --file requirements.txt # pip

```
To activate project environment, use
```

    $ conda activate gm_analysis

```
To deactivate an active environment, use
```

    $ conda deactivate

```
Export requirements.yml using Conda
```

    $ conda gm_analysis export > environment.yml

```

## Libraries

- Python client library for Google Maps API Web Services [__GitHub__](https://github.com/googlemaps/google-maps-services-python)


## Example output

### Transportation Route
```

Input Start:    Bush House Aldwych London
Input End:      Holborn Station

Start address:  30 Aldwych, London WC2B 4BG, UK
End address:    Holborn, Underground Ltd, Holborn Station, Kingsway, London WC2B 6AA, UK

Steps are as follows:
========================
STEP 1
travel mode:    WALKING
distance:       0.068 km
time taken:     0:00:59
========================
STEP 2
travel mode:    Bus
depart at:      Aldwych / Drury Lane
arrive at:      Holborn Station (Stop P)
distance:       0.549 km
time taken:     0:03:00
========================
STEP 3
travel mode:    WALKING
distance:       0.099 km
time taken:     0:01:32
========================

[In total]
distance:       0.716 km
time taken:     0:05:48

```

### Walking Route
```

Input Start:    Bush House Aldwych London
Input End:      Holborn Station

Start address:  30 Aldwych, London WC2B 4BG, UK
End address:    Holborn, Underground Ltd, Holborn Station, Kingsway, London WC2B 6AA, UK

travel mode:    walking

[In total]
distance:       0.506 km
time taken:     0:06:55

```
