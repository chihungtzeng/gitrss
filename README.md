## gitrss

gitrss can be used to monitor development activities in git repositories by generating rss feeds. Feed item include commit messages and diff.

## Getting Started

Once installed, simply run
```
python -m gitrss --repo /path/to/repo --output-file /tmp/repo_name.xml
```

### Prerequisites

GitPython and rfeed are required. People can use
```
pip -r requirements.txt --user to installed them in the local directory.
```

### Installing

Run the following command:
```
python setup.py install --user
```

## Authors

* Chih-Hung Tseng - *Initial work*
