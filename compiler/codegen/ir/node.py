from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple, Union

class DataType(Enum):
    INT = 1
    FLOAT = 2
    STR = 3
    BOOL = 4
    UNKNOWN = 5
    
class ContainerType(Enum):
    VEC = 1
    HASH = 2
    ORDERED_MAP = 3
    FILE = 4
    STREAMING = 5

class ArithemeticOp(Enum):
    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4
    
class CompareOp(Enum):
    EQ = 1
    GT = 2
    LT = 3
    GE = 4
    LE = 5
    NEQ = 6

class LogicalOp(Enum):
    AND = 1
    OR = 2
    NOT = 3


class Reducer(Enum):
    COUNT = 1
    SUM = 2
    AVG = 3
    MIN = 4
    MAX = 5

class IRNode(ABC):
    def __init__(self):
        pass

    @property
    def classname(self) -> str:
        return self.__class__.__name__

    def __str__(self):
        return self.__class__.__name__

    def accept(self, visitor, ctx=None):
        class_list = type(self).__mro__
        for cls in class_list:
            func_name = "visit" + cls.__name__
            visit_func = getattr(visitor, func_name, None)
            if visit_func is not None:
                return visit_func(self, ctx)
        raise Exception(f"visit function for {self.name} not implemented")


#single value
class Value(IRNode):
    def __init__(self, val):
        super().__init__()
        self.val = val

    @abstractmethod
    def value(self):
        return self.val


class Column(Value):
    def __init__(self, table_name: str, column_name: str, dtype: DataType, val: Value):
        super().__init__(val)
        self.tname = table_name
        self.cname = column_name
        self.dtype = dtype


class Literal(Value):
    def __init__(self, dtype: DataType, val: Value):
        super().__init__(val)
        self.dtype = dtype

class Var(Value):
    def __init__(self, name: str, dtype: DataType, val: Value):
        super().__init__(val)
        self.name = name
        self.dtype = dtype
        
class FunctionDefiniton(IRNode):
    def __init__(self, name: str, params: List[DataType], ret: DataType):
        super().__init__()
        self.name = name
        self.params = params
        self.ret = ret

class FunctionCall(Value):
    def __init__(self, func: FunctionDefiniton, params: List[Value]):
        super().__init__(None)
        self.func = func
        self.params = params
    
    def value(self):
        # return the return value of the function
        raise NotImplementedError

class Expression(Value):
    def __init__(self, lhs: Value, rhs: Value, op: ArithemeticOp):
        super().__init__(None)
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
        
    def value(self):
        # return the value of the expression
        raise NotImplementedError

class Assignment(IRNode):
    def __init__(self, lhs: Union[Var, Column], rhs: Value):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs        

# multiple value

class StructType(IRNode):
    def __init__(self, name: str, fields: List[Tuple[str, Union[StructType,DataType]]]):
        super().__init__()
        self.name = name
        self.fields = fields

class StructValue(IRNode):
    def __init__(self, vals: List[Union[StructValue,Value]]):
        super().__init__()
        self.vals = vals
        
    @abstractmethod
    def values(self):
        return self.vals
    
class TableDefinition(IRNode):
    def __init__(self, name: str, schema: StructType, hint: str):
        super().__init__()
        self.name = name
        self.schema = schema  
        self.hint = hint  

class TableInstance(StructValue):
    def __init__(self, definition: TableDefinition, ctype: ContainerType, vals: List[StructValue]):
        super().__init__(vals)    
        self.definition = definition
        self.ctype = ctype


class Condition(IRNode):
    def __init__(self):
        super().__init__()

class AlgebraCondition(Condition):
    def __init__(self, lhs: Value, rhs: Value, op: CompareOp):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
        
class LogicalCondition(Condition):
    def __init__(self, lhs: Condition, rhs: Condition, op: LogicalOp):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
        if self.op == LogicalOp.NOT:
            assert self.rhs is None

class JoinCondition(Condition):
    def __init__(self, table_name: str, lhs: Column, rhs: Column):
        super().__init__()     
        self.tname = table_name
        self.lhs = lhs
        self.rhs = rhs   

class Operation(IRNode):
    def __init__(self):
        super().__init__()
            
class Copy(Operation, StructValue):
    def __init__(self, table_name: str, columns: StructType, join: JoinCondition = None, where: Condition = None, limit: Value = None):
        super(Operation, self).__init__()
        super(StructValue, self).__init__(None)
        self.tname = table_name
        self.columns = columns
        self.join = join
        self.where = where
        self.limit = limit

    def values(self):
        # return the values of the table
        raise NotImplementedError
    
class Insert(Operation):
    def __init__(self, table_name: str, vals: List[StructValue], select: Copy = None):
        super().__init__()
        self.tname = table_name
        self.vals = vals
        self.select = select
        if self.select is not None:
            assert self.vals is None
            
class Update(Operation):
    def __init__(self, table_name: str, assgins: List[Assignment], where: Condition = None):
        super().__init__()
        self.tname = table_name
        self.assigns = assgins
        self.where = where
        
class Move(Operation):
    def __init__(self, table_name: str, where: Condition = None):
        super().__init__()
        self.tname = table_name
        self.where = where
        
class Reduce(Operation, Value):
    def __init__(self, table_name: str, reducer: Reducer, columns: StructType, join: JoinCondition = None, where: Condition = None, limit: Expression = None):
        super(Operation, self).__init__()
        super(Value, self).__init__(None)
        self.tname = table_name
        self.reducer = reducer
        self.columns = columns
        self.join = join
        self.where = where
        self.limit = limit
        
    def value(self):
        # return the value of the reducer
        raise NotImplementedError

class Root(IRNode):
    def __init__(self, children: List[Operation]):
        super().__init__()
        self.children = children
        
    def __iter__(self):
        return iter(self.children)

TypeRPC = StructType("RPC", [StructType("meta", [("src", DataType.STR), ("dst", DataType.STR), ("type", DataType.STR)]), StructType("payload", [("data", DataType.STR)])])

InputTable = TableInstance(TableDefinition("input", TypeRPC, "reserved"), ContainerType.STREAMING, [])

OutputTable = TableInstance(TableDefinition("output", TypeRPC, "reserved"), ContainerType.STREAMING, [])