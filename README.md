# Provenance-Aware Regular Path Queries (RPQ) Engine

The RPQ engine is an RPQ-to-SQLite compiler that parses the regular expression to SQLite query, and runs the query on the database.

The engine supports the following standard regular expression symbols:
- literal
- concatenation “.”
- alternation “|”
- transitive closure “∗”
- positive transitive closure “+”
- inverse “−”
- optional “?”
- grouping "()"

An application to the RPQ engine is to query a provenance graph. The graph is stored in the database as a table with three columns: "startNode", "endNode", and "label".
A literal in RPQ corresponding to an edge label in a graph.

The RPQ engine also allows query to go through particular nodes in the graph by adding a bracket "[]" around the node name. For example, `[Alice](knows)` can be a query that returns the people that Alice knows, where in the corresponding graph, name is a node, and relationship type is the label of the edge.

The hamming number example is in the [hamming folder](https://github.com/qwang70/rpq-engine-project/example/hamming). `cd` to this folder. Run either `python ../../query_compiler.py hamming.db sail` to query "sail" graph, or `python ../../query_compiler.py hamming.db fish` to query "fish" graph with an interactive shell. [What is sail and fish?](https://github.com/qwang70/rpq-engine-project/from-data-to-knowledge-with-workflows-provenance-85-638.jpg). `make.sh` contains some sample rpq queries.

A provenance example can be checked out in the [C3C4 folder](https://github.com/qwang70/rpq-engine-project/example/C3C4). `cd` to this folder. Open or run `./make.sh`. Note that the example depends on YesWorkflow.

## Usage
```
python query_compiler.py -h
usage: query_compiler.py [-h] [-debug] [-c C [C ...]] database table

Regular Path Query Engine

positional arguments:
database      SQL Database to query
table         Table name in the database

optional arguments:
-h, --help    show this help message and exit
-debug        Debug Mode
-c C [C ...]  command line mode
```

