import argparse, tempfile, time, yaml, subprocess
from git.remote import RemoteProgress
from git.repo.base import Repo
from pyfiglet import Figlet

## Global Variables ##
YAML_FILE = "pipeline.yml"
######################

# Handler intance responsible for providing parse progress information
class CloneProgress(RemoteProgress):
  def update(self, op_code, cur_count, max_count=None, message=''):
      if message:
          print(message)

# Define and grab all args for CLI
def define_cli_args():
  parser = argparse.ArgumentParser("buildit4me", description="A simple CI tool for your CLI")
  parser.add_argument("pipeline_name", 
    help="reference to the pipeline defined in the YAML declarative file",
    metavar="PIPELINE_NAME")

  parser.add_argument("git_repo", 
    help="the git remote repo (HTTPS/SSH format)",
    metavar="GIT_REPO")

  parser.add_argument("-d", "--debug", 
    help="enables debug mode which prints out useful information for developers",
    action="store_true")
  global args
  args = parser.parse_args()

def parse_and_return_pipeline_yaml(location, name=YAML_FILE):
  """
  location (string): the *.yaml file location\n
  name (string) - the *.yaml file name
  return - Dict
  """
  yaml_file = open(location + "/" + name)
  parsed_yaml_file = yaml.load(yaml_file, Loader=yaml.FullLoader)
  return parsed_yaml_file

def return_task_cmd(task, tasks):
  """
  task (string): pipeline to lookup for inside the valid pipelines iterable
  pipelines (list): list to iterate through in order to lookup for pipeline
  return formats:
    - String containing the command itself
    - Boolean False stating that the command wasn't found
  """
  # extracts both task name and its corresponding command based on provided task
  # expecting a command key named as 'cmd'
  for task_dict in tasks:
    for task_key, task_value in task_dict.items():
      if task == task_key:
        try:
          return task_value["cmd"]
        except KeyError as err:
          print("Invalid syntax. Missing key from declarative file:", err)
          raise
  return False

def is_valid_pipeline(pipeline_name, pipelines):
  """
  pipeline_name (string): pipeline to lookup for inside the valid pipelines iterable
  pipelines (list): list to iterate through in order to lookup for pipeline
  return: Boolean
  """
  # use list comprehension to extract a list containing all pipeline names from the pipelines data structure
  return pipeline_name in [valid_pipeline for pipeline_dict in pipelines for valid_pipeline in pipeline_dict.keys()]

def is_valid_task(pipeline_task, tasks):
  """
  pipeline_task (string): task to lookup for inside the valid tasks iterable
  tasks (list): list to iterate through in order to lookup for pipeline_task
  return: Boolean
  """
  # use list comprehension to extract a list containing all task names from the tasks data structure
  return pipeline_task in [valid_task for task_dict in tasks for valid_task in task_dict.keys()]

def start_build():
  f = Figlet(font='standard')
  print(f.renderText("BuildIt4me!"))
  define_cli_args()
  if args.debug:
    print("*** DEBUG MODE ***")
  print(f"-> Pipeline '{ args.pipeline_name }' has started!")
  
  try:
    # The temp directory for the cloned repo is only kept inside the below "with" scope
    with tempfile.TemporaryDirectory() as tmpdirname:
      print('-> Creating temporary directory', tmpdirname)
      print("-> Checking out from SCM")
      print(f"-> Cloning { args.git_repo } into temp dir '{ tmpdirname }'")
      # get the instance of the git object while cloning the remote repo
      # https://gitpython.readthedocs.io/en/stable/reference.html#module-git.remote
      git_repo = Repo.clone_from(args.git_repo, tmpdirname, branch='master', progress=CloneProgress())
      # retrieve the branch where the build should run from
      build_branch = parse_and_return_pipeline_yaml(tmpdirname)["branch"]
      # return the defined tasks from the parsed yaml file
      tasks = parse_and_return_pipeline_yaml(tmpdirname)["tasks"]
      # return the defined pipelines from the parsed yaml file
      pipelines = parse_and_return_pipeline_yaml(tmpdirname)["pipelines"]

      # if DEBUG global variable is set to True, print parsed complex data strucure for tasks and pipelines
      if args.debug:
        print("[DEBUG] - Tasks Data Structure:", tasks)
        print("[DEBUG] - Pipelines Data Structure:", pipelines)

      print("\nBuild from branch:", build_branch)
      # checks out local git branch
      git_repo.git.checkout(build_branch)
      # checks if the provided pipeline is valid
      if is_valid_pipeline(args.pipeline_name, pipelines):
        # iterate through all dictionaries represented by {'pipeline_name': ['task1', 'task2']}
        for pipeline_dict in pipelines:
          # split the dictionary between pipeline_name and its corresponding tasks list
          for pipeline_key, pipeline_value in pipeline_dict.items():
            # checks if the current pipeline name matches the provided pipeline
            if pipeline_key == args.pipeline_name:
              # iterate through every task from the tasks list
              for pipeline_task in pipeline_value:
                print(f"\n*** { pipeline_task.capitalize() } ***")
                # checks if the current task is valid,
                # grabs its corresponding command from the tasks list
                # then the command is executed in the Shell subprocess module
                if is_valid_task(pipeline_task, tasks):
                    print(" CMD:", return_task_cmd(pipeline_task, tasks))
                    cmd_call = subprocess.call(return_task_cmd(pipeline_task, tasks), 
                      shell=True, cwd=tmpdirname)
                    # if the subprocess exit code is other than 0 raise an error
                    if cmd_call:
                      raise ValueError("Provided CMD doesn't work. Subprocess returned with error", cmd_call)
                else:
                  raise ValueError(f"The task '{ pipeline_task }' doesn't seem to be a valid task. Check your pipeline manifest and try again.")
      else:
        raise ValueError(f"'{ args.pipeline_name }' doesn't seem to be a valid pipeline. Check your pipeline manifest and try again.")

      # just announcing the temp dir removal, since it's going to be removed by the end of the 'with' block lifecycle
      print("\n-> Post run housekeeping: Removing temporary directory", tmpdirname)
      print("\nThe pipeline finished without any errors!\n")

  except OSError as err:
    print("Couldn't create temporary directory in local file system:", err)
    print("Error code:", err.errno)

if __name__ == "__main__":
  # Start the building process
  start_build()