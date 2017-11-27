import re
import numpy as np
import pandas as pd

colorToFunc = {"#FFFFCC": "data", "#CCFFCC": "computation", "#FCFCFC": "param",\
                "#FFFFFF": "in/output"}
node_type = {}
node_pattern = re.compile( r"""
     node                # Start of a numeric entity reference
     [.*
       fillcolor=\"[#0-9a-fA-F]+
       \"
       .*
     ]
    """)
node_pattern = re.compile( r"node\[.*fillcolor=\"([#a-zA-Z0-9_]+)\".*\]")
ID_pattern = re.compile(r"^(?!node|edge|graph|digraph|subgraph|strict)(\w+)( \[.*\])?;?\n$")
diedge_pattern = re.compile(r"^(\w+) -> (\w+)")
test_string = "provided_greeting [sss]\n"
m = ID_pattern.search(test_string)

# initialize values
curr_node_type = ""
# first element is startNode, second element is endNode, third element is label
edge = []
# parse dot file
#with open("Greeting.dot",'r') as f:
with open("parleocar.gv",'r') as f:
    for line in f:
        if node_pattern.search(line) is not None:
            m = node_pattern.search(line)
            curr_node_type = m.group(1)
        elif re.match(ID_pattern, line) is not None:
            key = ID_pattern.search(line).group(1)
#            if "_input_port" not in key and "_output_port" not in key:
            if curr_node_type in colorToFunc:
                node_type[key] = colorToFunc[curr_node_type]
            else:
                node_type[key] = curr_node_type
        elif diedge_pattern.search(line) is not None:
            m = diedge_pattern.search(line)
            left = m.group(1)
            right = m.group(2)
            edge.append([left, right, node_type[left]+"-"+node_type[right] ])

df = pd.DataFrame(data=np.array(edge), columns = ["startNode", "endNode", "weight"])
print(df)
