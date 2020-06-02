# Buildit4me

A simple CI tool for your CLI

![Demo image](./assets/buildit4me.png)

## Usage

```bash
python3 buildit4me <PIPELINE_NAME> <GIT_REPO>
```

| Argument  |  Type |  Description | Positional | Required |
|:-----------|:-------:|:--------------|:--------:|:--------:|
| *<PIPELINE_NAME>* |  String  | Reference to the pipeline defined in the YAML declarative file  | Yes | Yes |
| *<GIT_REPO>*  |  String  | The git remote repo (HTTPS/SSH format) | Yes | Yes |
| *-d, --debug*  |  Flag  | Enables debug mode which prints out useful information for developers | No | No |
| *-h, --help*  |  Flag  | Prints out CLI help section | No | No |

### Requirements:

Make sure you have following Python dependencies:
- Python v3
- python3-pip

---

### Dev environment setup

After cloning this repo to your local working directory, prepare your dev environment like so:

1 - Create a virtual environment in order to isolate your Python workspace under your working directory:
```bash
python3 -m venv env && source env/bin/activate 
```

2 - Check if you are actually inside the Python Virtual Environment:
```bash
pip -V
```
> This should show you the path for your previous created Python `venv` directory

3 - Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Test it against a sample pipeline target

For such purpose there's a Shell script to make your life easier, it will make use of the [Dockerfile](./Dockerfile) present in this repo and take you directly inside a container (interactive mode) which includes all build dependencies for the [sample target Java application](https://github.com/PayCertify/devops-scripting-helloworld), such as JDK, Maven and zip.

Execute the `docker_activate.sh` script:
```bash
./docker_activate.sh
```

Once you are interacting with the container `sh`, issue the following:
```bash
python3 ./src/buildit4me/buildit4me.py build https://github.com/PayCertify/devops-scripting-helloworld.git
```
> *Note: You can replace `build` with `release` or `foo` in order to refer to different pipelines inside the [**pipeline.yaml**](https://github.com/PayCertify/devops-scripting-helloworld/blob/master/pipeline.yml) declarative file.*

<br />

## Unit Testing

In order to execute the script containing all unit tests proceed as follow:

Change to the src directory context:
```bash
cd ./src
```

<br />

Execute the `unit_tests.py` script:
```bash
python3 unit_tests.py
```

### Test Assets

In order for the tests to be more precise, there's a `./src/test_assets` directory designed to keep aux and mockup files, such as `pipeline.yml`.

---