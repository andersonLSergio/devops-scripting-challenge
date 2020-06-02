import unittest

from buildit4me.buildit4me import *

YAML_FILE = "pipeline.yml"
ASSETS_LOCATION = "./test_assets"

class TestParseAndReturnPipelineYaml(unittest.TestCase):

  def test_yaml_is_parsed(self):
    """
    Test if the function is able to parse and retrieve a yaml file
    """
    result1 = parse_and_return_pipeline_yaml(ASSETS_LOCATION, YAML_FILE)
    result2 = parse_and_return_pipeline_yaml(ASSETS_LOCATION, YAML_FILE)["tasks"]
    self.assertEqual(str(type(result1)), "<class 'dict'>")
    self.assertEqual(str(type(result2)), "<class 'list'>")

class TestReturnTaskCmd(unittest.TestCase):

  def test_return_valid_cmd(self):
    """
    Test if the function is able to retrieve a task corresponding command
    """
    task_name = "build"
    tasks_iterable = parse_and_return_pipeline_yaml(ASSETS_LOCATION, YAML_FILE)["tasks"]
    result = return_task_cmd(task_name, tasks_iterable)
    self.assertEqual(result, "mvn clean install")

  def test_for_undefined_task(self):
    """
    Test if the function is able to handle it if the task provided isn't defined in the YAML file
    """
    task_name = "invalid"
    tasks_iterable = parse_and_return_pipeline_yaml(ASSETS_LOCATION, YAML_FILE)["tasks"]
    result = return_task_cmd(task_name, tasks_iterable)
    self.assertEqual(result, False)

  def test_return_invalid_cmd(self):
    """
    Test if the function is able to handle incompatible CMD definition (e.g. cmd key typo)
    """
    task_name = "cmdless_task"
    tasks_iterable = parse_and_return_pipeline_yaml(ASSETS_LOCATION, YAML_FILE)["tasks"]
    self.assertRaises(KeyError, return_task_cmd, task_name, tasks_iterable)

class TestIsValidPipeline(unittest.TestCase):

  def test_return_valid_pipeline(self):
    """
    Test if the function is able to confirm a valid pipeline
    """
    valid_pipeline = "release"
    pipelines_iterable = parse_and_return_pipeline_yaml(ASSETS_LOCATION, YAML_FILE)["pipelines"]
    result = is_valid_pipeline(valid_pipeline, pipelines_iterable)
    self.assertEqual(result, True)

  def test_return_invalid_pipeline(self):
    """
    Test if the function is able to confirm an invalid pipeline
    """
    valid_pipeline = "imatypo"
    pipelines_iterable = parse_and_return_pipeline_yaml(ASSETS_LOCATION, YAML_FILE)["pipelines"]
    result = is_valid_pipeline(valid_pipeline, pipelines_iterable)
    self.assertEqual(result, False)

class TestIsValidTask(unittest.TestCase):

  def test_return_valid_task(self):
    """
    Test if the function is able to confirm a valid task
    """
    valid_task = "compress"
    tasks_iterable = parse_and_return_pipeline_yaml(ASSETS_LOCATION, YAML_FILE)["tasks"]
    result = is_valid_task(valid_task, tasks_iterable)
    self.assertEqual(result, True)

  def test_return_invalid_task(self):
    """
    Test if the function is able to confirm an invalid task
    """
    valid_task = "invalid"
    tasks_iterable = parse_and_return_pipeline_yaml(ASSETS_LOCATION, YAML_FILE)["tasks"]
    result = is_valid_task(valid_task, tasks_iterable)
    self.assertEqual(result, False)

if __name__ == '__main__':
  unittest.main()