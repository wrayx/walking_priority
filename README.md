## Python Environment
1. put Google Maps API key obtained from Google Cloud Platform into `api_key.txt` 

2. Create the environment, most packages come with the `osmnx` installation.
    ```
        
        $ conda create -n ox -c conda-forge --strict-channel-priority osmnx

    ```
3. Install additional package:
    ```

        $ conda install -c conda-forge googlemaps

    ```
4. To activate project environment:
    ```

        $ conda activate ox

    ```
5. To deactivate an active environment:
    ```

        $ conda deactivate

    ```

If program encountered any problem that relates the environment, please check your Python version or other packages version with the `environment.yml`.


## Running the programs

1. Compute the Google Maps `wk_weight`

    ```

        $ python3 run.py

    ```

2. Start Jupyter notebook session and run `nav_london.ipynb` for the custom `osmnx` version of routing tool. New origins and destination can be set from the notebook file.

## Libraries

- Python client library for Google Maps API Web Services [__GitHub__](https://github.com/googlemaps/google-maps-services-python)


## Notes 
Export requirements.yml using Conda

```

$ conda ox export > environment.yml

```