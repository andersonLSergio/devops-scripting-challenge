import unittest

from buildit4me.buildit4me import parse_and_return_pipeline_yaml

class TestParseAndReturnPipelineYaml(unittest.TestCase):
  def test_yaml_is_parsed(self):
    """
    Test that it can parse and retrieve a yaml file
    """
    yaml_file = "pipeline.yml"
    location = "./test_assets"
    result = parse_and_return_pipeline_yaml(location, yaml_file)
    self.assertEqual(result.type(), "dict")

if __name__ == '__main__':
  unittest.main()