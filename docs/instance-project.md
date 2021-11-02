# Quartile REST API

Grow your product sales with Quartile’s e-commerce advertising solutions across Amazon, Instacart, and other leading online marketplaces.

[MKDocs](https://squidfunk.github.io/mkdocs-material/getting-started/)

## Dependencies

* [Python Version >= 3.8](https://www.python.org/)
* [Poetry](https://python-poetry.org/docs/#installation)


## Edit documentation


1. Clone the project.
    <div class="termy">

    ```console
    $ git clone https://...com/QD_OPEN_API/_git/QD_OPEN_API.git

    Cloning into 'QD_OPEN_API'...
    remote: Enumerating objects: 142, done.
    remote: Counting objects: 100% (142/142), done.
    remote: Compressing objects: 100% (98/98), done.
    remote: Total 142 (delta 39), reused 126 (delta 27), pack-reused 0
    Receiving objects: 100% (142/142), 848.58 KiB | 1.54 MiB/s, done.
    Resolving deltas: 100% (39/39), done.
    ```
    </div>


2. Access the folder.
    <div class="termy">

    ```console
    $ cd QD_OPEN_API/documentation/
    ```
    </div>


3. Create and activate a new virtualenv using poetry.
    <div class="termy">

    ```console
    $ poetry shell

    Spawning shell within /home/username/.cache/pypoetry/virtualenvs/documentation-CgtZZHXK-py3.8
    . /home/username/.cache/pypoetry/virtualenvs/documentation-CgtZZHXK-py3.8/bin/activate
    ```
    </div>



4. Install requirements.
    <div class="termy">

    ```console
    $ poetry install

    Installing dependencies from lock file
    ...
    ...
    ```
    </div>

5. Up project.
    <div class="termy">

    ```console
    $ mkdocs serve

    INFO     -  Building documentation...
    INFO     -  Cleaning site directory
    INFO     -  Documentation built in 0.78 seconds
    INFO     -  [10:17:42] Serving on http://127.0.0.1:8000/
    ```
    </div>

6. Access your local endpoint documentation.
    * Link: http://127.0.0.1:8000/