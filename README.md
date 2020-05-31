Buildit4me

A simple CI tool for your CLI

## Usage

```
buildit4me <PIPELINE_NAME> <GIT_REPO>
```

| Argument  |  Type |  Description |
|:-----------|:-------:|:--------------|
|  <PIPELINE_NAME> |  String  | Reference to the pipeline defined in the YAML declarative file  |
| <GIT_REPO>  |  String  | the git remote repo (HTTPS/SSH format) |

Requirements:

Make sure you have following Python dependencies:
- Python v3
- python3-pip

### Dev environment setup

After cloning this repo to your local working directory, prepare your dev environment like so:

1 - Create a virtual environment in order to isolate your Python workspace under your working directory:
```
python3 -m venv env && source env/bin/activate 
```

2 - Check if you are actually inside the Python Virtual Environment:
```
pip -V
```
> This should show you the path for your previous created Python `venv` directory

3 - Install Python dependencies:
```
pip install -r requirements.txt
```

### Using the script from source

In order to see the script in action without compiling a binary, you can make use of the present `Dockerfile`. 

For such purpose there's a Shell script to make your life easier, which you bring you directly inside the container (interactive mode) that includes all build dependencies for the [sample target Java application](https://github.com/PayCertify/devops-scripting-helloworld), such as JDK, Maven and zip.

Execute the `docker_activate.sh` script:
```
./docker_activate.sh
```

Once you are interacting with the container `sh`, issue the following:
```
python3 ./src/buildit4me/buildit4me.py build https://github.com/PayCertify/devops-scripting-helloworld.git
```
> *Note: Replace `build` with `release` or `foo` in order to refer to different pipelines inside the [**pipeline.yaml**](https://github.com/PayCertify/devops-scripting-helloworld/blob/master/pipeline.yml) declarative file.*