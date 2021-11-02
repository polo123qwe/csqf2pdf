# CSQF2PDF

Tool to generate a Graphviz text file and pdf based on a given topology and a report.
It outputs a .gv file that has the graphviz graph, and if possible also generates a .pdf of the topology.

You can also preview the topology at https://dreampuf.github.io/GraphvizOnline, just pasting the code generated in the .gv file.

### Installation
This package uses Python 3 and the `graphviz` package. To install it run:

```bash
pip install graphviz
```

### Usage
```bash
usage: csqf2pdf.py [-h] [-m [message]] [-t [topology]] [-r [report]] [-o [output]]

options:
  -h, --help            show this help message and exit
  -m [message], --message [message]
                        Message name (eg. F1)
  -t [topology], --topology [topology]
                        Topology file location
  -r [report], --report [report]
                        Report file location
  -o [output], --output [output]
                        Output directory
```

example:
```bash
python .\csqf2pdf.py -m F1 -t "test_cases\example\Input\Config.xml" -r "test_cases\example\Output\Report.xml" -o "test_output"
```

### Contributors
- Sergi Bernaus (s202372@student.dtu.dk)
- Tufan Usta (s212388@student.dtu.dk)
