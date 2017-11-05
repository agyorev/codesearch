import os
import re
import yaml

from argumentparser import ArgumentParser
from subprocess import check_output, Popen, PIPE, CalledProcessError

__title__ = 'codesearch'
__version__ = '0.1'
__author__ = 'Aleksandar Gyorev'
__license__ = 'MIT License'
__copyright__ = 'Copyright 2017 Aleksandar Gyorev'


class CodeSearch(object):
  CONFIG_FILE = 'codesearch.yaml'

  # Config file attributes.
  EXTENSIONS = 'extensions'
  INCLUDE_FOLDERS = 'include_folders'
  EXCLUDE_FOLDERS = 'exclude_folders'

  def __init__(self):
    self.flags = ArgumentParser().get_flags()

    try:
      self.repo_root = check_output(['git', 'rev-parse', '--show-toplevel']).strip('\n')
    except CalledProcessError:
      print 'Try running codesearch from a valid git repository.'
      exit(1)

    # Parse the configuration file.
    self.config_path = os.path.join(self.repo_root, CodeSearch.CONFIG_FILE)
    self.config = {}
    if os.path.isfile(self.config_path):
      with open(self.config_path, 'r') as config_file:
        self.config = yaml.load(config_file)
    self.config = {key: [re.escape(item) for item in value] for key, value in self.config.items() if value}

    # Compose the regex for which folders to include in the search.
    self.config[CodeSearch.INCLUDE_FOLDERS] = \
        self.config[CodeSearch.INCLUDE_FOLDERS] if CodeSearch.INCLUDE_FOLDERS in self.config else ['\\.']
    self.include_folders_regex = \
        ['{}/.*'.format(folder) if folder != '\\.' else '[^/]*' for folder in self.config[CodeSearch.INCLUDE_FOLDERS]]
    self.include_folders_regex = '^({})'.format('|'.join(self.include_folders_regex))

    # Compose the regex for which files to look into, depending on their extension.
    if self.flags.extension:
      self.file_extension_regex = self.flags.extension
    else:
      self.config[CodeSearch.EXTENSIONS] = \
          self.config[CodeSearch.EXTENSIONS] if CodeSearch.EXTENSIONS in self.config else ['.*']
      self.file_extension_regex = '|'.join(self.config[CodeSearch.EXTENSIONS])
    self.file_extension_regex = '\.({})$'.format(self.file_extension_regex)

    # Compose the regex for which folders to exclude from the search.
    if CodeSearch.EXCLUDE_FOLDERS in self.config:
      self.exclude_folders_regex = '({})'.format('|'.join(self.config[CodeSearch.EXCLUDE_FOLDERS]))
    else:
      self.exclude_folders_regex = None

  def find(self):
    repo_files = Popen(
        ['git', 'ls-files'],
        stdout=PIPE,
        cwd=self.repo_root
    )
    pre_excluded_files = Popen(
        ['egrep', self.include_folders_regex + self.file_extension_regex],
        stdin=repo_files.stdout,
        stdout=PIPE
    )
    post_excluded_files = Popen(
        ['egrep', '-v', self.exclude_folders_regex if self.exclude_folders_regex else '$^'],
        stdin=pre_excluded_files.stdout,
        stdout=PIPE
    )
    post_file_name_match = Popen(
        ['egrep', self.flags.file_path if self.flags.file_path else ''],
        stdin=post_excluded_files.stdout,
        stdout=PIPE
    )
    post_spaces_processing = Popen(
        ['sed', 's/ /\\ /g'],
        stdin=post_file_name_match.stdout,
        stdout=PIPE
    )

    # Perform egrep on each of the remaining matching files for the input pattern.
    match_per_file_args = ['xargs', 'egrep', '--no-messages', '--color=auto', '-n', '-C', str(self.flags.context)]
    if self.flags.ignore_case:
      match_per_file_args += ['-i']
    match_per_file_args += ['--', self.flags.pattern]
    Popen(match_per_file_args, stdin=post_spaces_processing.stdout, cwd=self.repo_root)


def run():
  cs = CodeSearch()

  if cs.flags.version:
    print __title__ + ' v' + __version__, 'by', __author__
  else:
    cs.find()


if __name__ == '__main__':
  run()
