import argparse, tempfile, time, yaml
from git import RemoteProgress
from git.repo.base import Repo

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

def parse_pipeline_yaml(location, name = "pipeline.yml"):
  """
  location (string): the *.yaml file location\n
  name (string) - the *.yaml file name
  """
  yaml_file = open(location + "/" + name)
  parsed_yaml_file = yaml.load(yaml_file, Loader=yaml.FullLoader)
  return parsed_yaml_file

# https://gitpython.readthedocs.io/en/stable/reference.html#module-git.remote
def clone_remote_repo():
  with tempfile.TemporaryDirectory() as tmpdirname:
    print('-> Creating temporary directory', tmpdirname)
    print(f"-> Cloning { args.git_repo } into temp dir '{ tmpdirname }'")
    Repo.clone_from(args.git_repo, tmpdirname, branch='master', progress=CloneProgress())
    print(parse_pipeline_yaml(tmpdirname))

    time.sleep(30)
    print('-> Removing temporary directory', tmpdirname)
    

def start_build():
  #print(f"-> The build for { args.pipeline_name } has started!")
  define_cli_args()
  clone_remote_repo()

# Start the building process
start_build()