```
usage: lvenv [-h] [--system-site-packages] [--symlinks | --copies] [--clear] [--upgrade] [--without-pip]
             [--prompt PROMPT] [--upgrade-deps]
             ENV_DIR

Creates virtual Python environments in one or more target directories. Overrides the root logger in such away that
all logging.info, logging.warnings, ... calls are written to a file in the project directory / .log

positional arguments:
  ENV_DIR               A directory to create the environment in.

optional arguments:
  -h, --help            show this help message and exit
  --system-site-packages
                        Give the virtual environment access to the system site-packages dir.
  --symlinks            Try to use symlinks rather than copies, when symlinks are not the default for the platform.
  --copies              Try to use copies rather than symlinks, even when symlinks are the default for the platform.
  --clear               Delete the contents of the environment directory if it already exists, before environment
                        creation.
  --upgrade             Upgrade the environment directory to use this version of Python, assuming Python has been
                        upgraded in-place.
  --without-pip         Skips installing or upgrading pip in the virtual environment (pip is bootstrapped by default)
  --prompt PROMPT       Provides an alternative prompt prefix for this environment.
  --upgrade-deps        Upgrade core dependencies: pip setuptools to the latest version in PyPI
```
