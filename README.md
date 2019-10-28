# url-loader

A simple tool for downloading a list of urls. 

## requirements
- python 3.7 or above
- the `coverage` tool to generate a coverage report. Execute `make init` to install it via `pip`.

## usage
```
$ ./url-loader.py -h                                                                                                                                                                                                                                                                                                                                 [19:56:02]
usage: url-loader.py [-h] [-d DIR] [--continue-on-error] [-v] urls

positional arguments:
  urls                 the file containing the list of source urls

optional arguments:
  -h, --help           show this help message and exit
  -d DIR, --dir DIR    the output directory (default: current working
                       directory)
  --continue-on-error  let ./url-loader.py continue if one url download fails
                       (default: false)
  -v, --verbose        verbose output
```

To execute the tests call `make test`. For a coverage report execute `make coverage`. A simple end-to-end test can be executed with `make e2e-test`.