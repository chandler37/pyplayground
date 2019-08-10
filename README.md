# pyplayground

![ultracompelling logo](pyplayground.png)

This is a repository to help you learn Python.

## Renaming it from pyplayground to your chosen package name

Run `python3 rename_pyplayground.py --new-name=your-chosen-name`

If you do not have `python3` in your `PATH`, install
[Homebrew](https://brew.sh/) and then run `brew install python`.

## Committing

- git checkout master
- git pull --ff-only
- git checkout origin/master -b featurebranch
- git add newfile
- git add modifiedfile
- git commit
- git status
- verify that there are no files you forgot to commit
- git push origin HEAD
- use the URL it printed to create the pull request and merge it
- back to step 1!


## Installing

TODO: Make setup.py work so people can install this. You could even put this on
pypi; the directory structure is adequate.

[Homebrew](https://brew.sh/) is required.


## Developing

Run tests via `make test`

Run ipython via `make shell`

Or run the command-line interface:

```sh
$ (source venv/bin/activate && python pyplayground-runner.py cat .gitignore)
__pycache__
*.pyc
.DS_Store
/venv
.cache
```
