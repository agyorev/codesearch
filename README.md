## 🔎 codesearch

Search for patterns and phrases in your git repository code base.

All this tool is is a glorified and sugar-coated `egrep`. However, the difference it makes in productivity and getting around a code base is surprising.

### Installation
```bash
$ brew update  # optional
$ brew install agyorev/tools/codesearch
```

### Use Case
Let's take an example where the tools really shines. Say you're trying to find out how some RPC action, called `'editUser'` maps from a JavaScript frontend to a Python backend. 

You can first search for all of the occurrences of `'editUser'` in your `js` files, like:
```bash
$ codesearch -e js -p "'editUser'"
```

Then you can look up the same string literal, with some context around it, in your Python files, and see where the action is being registered:
```bash
$ codesearch -e py -c 1 -p "'editUser'"
```

Or maybe you want to look up all of the `edit*` actions. In this case just use a normal regular expression:
```bash
$ codesearch -e py -c 1 -p "'edit[^']+'"
```

### Config (optional)
In case you don't want to look through your whole git repository, maybe there are some irrelevant folders (`node_modules`, for example), or you don't want to look through _all_ file types. 

If this sounds like something you'd like, you should create a file called `codesearch.yaml` and put it in the root of your git repository. 

Currently the following properties are allowed:
```yaml
extensions:  # only match against files with these extensions, unless specifically set with the -e option.
  - ...

include_folders:  # only show matches from the following folders
  - ...

exclude_folders:  # exclude all files from the following folders from the search
  - ...
```

You can check out the example [config file](https://github.com/agyorev/codesearch/blob/master/codesearch.yaml), for reference.

### Usage
Run within a git repository folder.

```
$ codesearch --help
usage: codesearch [-h] [-f FILE_PATH] [-e EXTENSION] [-i] [-c CONTEXT]
                  (-p PATTERN | -v)

optional arguments:
  -h, --help            show this help message and exit
  -f FILE_PATH, --file-path FILE_PATH
                        Filter based on a matching pattern in the file path
                        name.
  -e EXTENSION, --extension EXTENSION
                        Filter based on the extension type of the file.
  -i, --ignore-case     Case insensitive pattern match.
  -c CONTEXT, --context CONTEXT
                        Number of (context) lines to show around the matches.
  -p PATTERN, --pattern PATTERN
                        The text pattern to find in the code. Regex enabled.
  -v, --version         Display the active version of the tool.
```
