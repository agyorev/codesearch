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

  def __config(self):
    """Parse the configuration file."""
    config_path = os.path.join(self.repo_root, CodeSearch.CONFIG_FILE)
    config = {}
    if os.path.isfile(config_path):
      with open(config_path, 'r') as config_file:
        config = yaml.load(config_file)
    config = {key: [re.escape(item) for item in value] for key, value in config.items() if value}
    return config

  def __include_folders_regex(self):
    """Compose the regex for which folders to include in the search."""
    if CodeSearch.INCLUDE_FOLDERS not in self.config:
      folder_regex_list = ['.*']
    else:
      folder_regex_list = ['{}/.+'.format(folder) if folder != '\\.' else '[^/]+'
                           for folder in self.config[CodeSearch.INCLUDE_FOLDERS]]
    return '^({})'.format('|'.join(folder_regex_list))

  def __file_extensions_regex(self):
    """Compose the regex for which files to look into, depending on their extension."""
    if self.flags.extension:
      file_extensions_regex_list = self.flags.extension
    else:
      file_extensions_regex_list = ['.+'] \
          if CodeSearch.EXTENSIONS not in self.config else '|'.join(self.config[CodeSearch.EXTENSIONS])
    return '\.({})$'.format(file_extensions_regex_list)

  def __exclude_folders_regex(self):
    """Compose the regex for which folders to exclude from the search."""
    if CodeSearch.EXCLUDE_FOLDERS not in self.config:
      folder_regex_list = ['$^']
    else:
      folder_regex_list = ['{}/.+'.format(folder) if folder != '\\.' else '[^/]+$'
                           for folder in self.config[CodeSearch.EXCLUDE_FOLDERS]]
    return '^({})'.format('|'.join(folder_regex_list))

  def __init__(self):
    self.flags = ArgumentParser().get_flags()

    # Because -v and -p options are mutually exclusive, there's no need to read and compute the config and regexes.
    if self.flags.version:
      return

    try:
      self.repo_root = check_output(['git', 'rev-parse', '--show-toplevel']).strip('\n')
    except CalledProcessError:
      print 'Try running codesearch from a valid git repository.'
      exit(1)

    self.config = self.__config()
    self.include_folders_regex = self.__include_folders_regex()
    self.file_extensions_regex = self.__file_extensions_regex()
    self.exclude_folders_regex = self.__exclude_folders_regex()

  def find(self):
    repo_files = Popen(
        ['git', 'ls-files'],
        stdout=PIPE,
        cwd=self.repo_root
    )
    pre_excluded_files = Popen(
        ['egrep', self.include_folders_regex + self.file_extensions_regex],
        stdin=repo_files.stdout,
        stdout=PIPE
    )
    post_excluded_files = Popen(
        ['egrep', '-v', self.exclude_folders_regex],
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
