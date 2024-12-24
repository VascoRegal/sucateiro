# Sucateiro

Sucateiro is a Python-based web scrapping tool that extracts data from web pages based on configuration YAMLs. Sucateiro provides an uniform configuration appliable to multiple web pages, handling pagination and dynamic placeholders in URLs.

You define what you want to extract from a web page's layout in a config file and Sucateiro extracts it!

## Examples

The ```examples/``` folder contains some YAML configuration examples and ```outputs/``` contains their respective results.

For example, running:

```
$ python3 sucateiro.py examples/exampleITJobs.yml
```

Dumps as JSON ITJob's first 5 pages of job posts for DevOps (file outputs/itjobs.json).


And

```
$ python3 sucateiro.py examples/exampleOLXIphones.yml
```

Dumps OLX's search results for Iphones on sale.


The scrapping is done with the same python code, defined by the configuration files.

## TODO

- Support for AJAX Pagination (infinite scrolling)
- Support for defining lambda functions in the configuration files for custom item retrievals
- CSS and By Attribute Selectors
- General Documentation (specially Configuration Files)
- Use Async libs for faster processing
- Implement more outputs formats
