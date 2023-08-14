from .node import *
from typing import Dict, List, Union
from compiler.protobuf import *

class IRContext():
    def __init__(self) -> None:
        self.table_map: Dict[str, TableInstance] = {
            "input": InputTable,
            "output": OutputTable,
        }
        self.func_map: Dict[str, FunctionDefiniton] = {}
        self.var_map: Dict[str, Var] = {
        }
