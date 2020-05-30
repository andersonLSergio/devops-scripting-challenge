import argparse, tempfile, time, yaml
from git import RemoteProgress
from git.repo.base import Repo
from pyfiglet import Figlet

# Instantiate the Handler in order to provide parse progress information
class CloneProgress(RemoteProgress):
  def update(self, op_code, cur_count, max_count=None, message=''):
      if message:
          print(message)

def define_cli_args():
  parser = argparse.ArgumentParser("buildit4me", description="A simple CI tool for your CLI")
  parser.add_argument("pipeline_name", 
    help="a name for your current CI pipeline",
    metavar="PIPELINE_NAME")

  parser.add_argument("git_repo", 
    help="the git remote repo (HTTPS/SSH format)",
    metavar="GIT_REPO")
  global args
  args = parser.parse_args()

def parse_and_return_pipeline_yaml(location, name = "pipeline.yml"):
  """
  location (string): the *.yaml file location\n
  name (string) - the *.yaml file name
  """
  yaml_file = open(location + "/" + name)
  parsed_yaml_file = yaml.load(yaml_file, Loader=yaml.FullLoader)
  return parsed_yaml_file

# https://gitpython.readthedocs.io/en/stable/reference.html#module-git.remote
def clone_remote_repo(git_repo, tmpdirname):
  """
  git_repo (string): Git remote address (HTTP|SSH format)\n
  tmpdirname (string) - Location in the filesystem where to place the cloned repo
  """
  print('-> Creating temporary directory', tmpdirname)
  print(f"-> Cloning { git_repo } into temp dir '{ tmpdirname }'")
  Repo.clone_from(git_repo, tmpdirname, branch='master', progress=CloneProgress())  

def populate_build_arguments(tmpdirname):
  global build_branch, tasks, pipelines
  build_branch = parse_and_return_pipeline_yaml(tmpdirname)["branch"]
  tasks = parse_and_return_pipeline_yaml(tmpdirname)["tasks"]
  pipelines = parse_and_return_pipeline_yaml(tmpdirname)["pipelines"]

def return_task_cmd(task):
  for task_dict in tasks:
    for task_key, task_value in task_dict.items():
      if task == task_key:
        return task_value["cmd"]
  #print([task_dict.keys() for task_dict.keys() in tasks])
  return False

def is_valid_task(step_task):
  """
  step_task (string): task to lookup for inside the valid tasks list
  """
  valid_tasks = []
  for task_dict in tasks:
  #   for task_key, task_value in task_dict.items():
  #     valid_tasks.append(task_key)
  # return step_task in valid_tasks
    for task_key in task_dict.keys():
      valid_tasks.append(task_key)
  return step_task in valid_tasks
  #print([[valid_task for valid_task in task_dict.keys()] for task_dict in tasks])

def start_build():
  f = Figlet(font='standard')
  print(f.renderText("BuildIt4me!"))
  define_cli_args()
  print(f"-> The build for '{ args.pipeline_name }' has started!")
  # The temp directory for the cloned repo only survives inside the below "with" scope
  try:
    with tempfile.TemporaryDirectory() as tmpdirname:
      clone_remote_repo(args.git_repo, tmpdirname)
      populate_build_arguments(tmpdirname)
      print("Branch to build:",build_branch)
      print("Tasks List:",tasks)
      print("Pipelines list:", pipelines)
      print("-> Steps:")
      for step_dict in pipelines:
        for step_key, step_value in step_dict.items():
          print(f"\n*** { step_key.capitalize() } ***")
          for step_task in step_value:
            print(" Task: ", step_task)
            print(" Valid (DEBUG):", is_valid_task(step_task))
            if is_valid_task(step_task):
              print(" CMD:", return_task_cmd(step_task))
              print(" =================")
            else:
              raise ValueError(f"The task '{ step_task }' doesn't seem to be a valid task. Check your pipeline manifest and try again.")
            # for task_dict in tasks:
            #   for task_key, task_value in task_dict.items():
            #     if step_task == task_key:
            #       return True
            #     return False
              # else:
              #   print(f"The task '{ step_task }' doesn't seem to be a valid task. Check your pipeline manifest and try again.")
            # print(f"    command: '{value}'")

      #time.sleep(30)
      print('-> Removing temporary directory', tmpdirname)

  except OSError as err:
    print("Couldn't create temporary directory in local file system:", err)

# Start the building process
start_build()