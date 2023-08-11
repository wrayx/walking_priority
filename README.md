# To Start

1. Put Google Maps API key into `api_key.txt`. Click the [link](https://developers.google.com/maps/documentation/javascript/directions) to see tutorial.

2. Create the environment, most packages come with the `osmnx` installation.
    ```
        
        $ conda create -n ox_env -c conda-forge --strict-channel-priority osmnx

    ```
3. To activate project environment:
    ```

        $ conda activate ox_env

    ```
4. Install additional package:
    ```

        $ conda install -c conda-forge googlemaps notebook

    ```
5. To deactivate an active environment:
    ```

        $ conda deactivate

    ```

If program encountered any problem that relates the environment, please check your Python version or other packages version with the `environment.yml`.


## Running the programs

1. Compute the Google Maps `wk_weight` for RQ1:

    ```

        $ python3 run.py

    ```

4. Statistical graphs for RQ2 are plotted in `plot_stats.ipynb`.

<!-- 2. Google Maps directions data are presented and plotted in `plan_route.ipynb`. -->

3. Start Jupyter notebook session and run `plan_route.ipynb` for the custom route planner in RQ3 and RQ4. New origins and destination can be set from the notebook file.



## Libraries

- Python client library for Google Maps API Web Services [google-maps-services](https://github.com/googlemaps/google-maps-services-python)

- Python library that built on top of NetworkX and GeoPandas, and interacts with OpenStreetMap APIs to model street networks and different travel mode. [osmnx](https://osmnx.readthedocs.io/en/stable/getting-started.html)


<!-- ## Notes 
Export requirements.yml using Conda

```

$ conda ox_env export > environment.yml

``` -->