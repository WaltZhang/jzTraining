JunZheng data and workflow simulator tool.
1. main.py is the command entry.
2. connectors.py is the the connection factory of training database.
3. data.py is the generator for simulating data.
4. generators.py introduces many static methods for customer information's simulation.
5. models.py defines the table structures.
6. setting.py is for configurations.
7. workflow.py is for workflow's nodes.

usage: main.py [-h] [-c {workflow,export}] [-x [{interview,branch}]] [N]

JunZheng training simulator CLI tool.

positional arguments:
  N                     the record count of simulating data

optional arguments:
  -h, --help            show this help message and exit
  -c {workflow,export}  training tool's commands
  -x [{interview,branch}]
                        exported file name if -c assigned with export, other
                        wise flow node


