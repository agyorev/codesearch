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

You can first search of all of the occurrences of `'editUser'` in your `js` files, like:
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
