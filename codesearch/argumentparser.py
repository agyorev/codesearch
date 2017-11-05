import argparse


class ArgumentParser(object):
  def __init__(self):
    self.parser = argparse.ArgumentParser()
    self.parser.add_argument('-f', '--file-path',
                             type=str,
                             help='Filter based on a matching pattern in the file path name.')
    self.parser.add_argument('-e', '--extension',
                             type=str,
                             help='Filter based on the extension type of the file.')
    self.parser.add_argument('-i', '--ignore-case',
                             dest='ignore_case',
                             action='store_true',
                             help='Case insensitive pattern match.')
    self.parser.add_argument('-c', '--context',
                             type=int,
                             default=0,
                             help='Number of (context) lines to show around the matches.')

    self.group = self.parser.add_mutually_exclusive_group(required=True)
    self.group.add_argument('-p', '--pattern',
                            type=str,
                            help='The text pattern to find in the code. Regex enabled.')
    self.group.add_argument('-v', '--version',
                            dest='version',
                            action='store_true',
                            help='Display the active version of the tool.')

  def get_flags(self):
    return self.parser.parse_args()
