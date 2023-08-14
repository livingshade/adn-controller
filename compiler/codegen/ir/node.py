from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple, Union

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


class EnumOP(Enum):
    def __eq__(self, other: EnumOP):
        return self.value == other.value

    def accept(self, visitor, ctx):
        class_list = type(self).__mro__
        for cls in class_list:
            func_name = "visit" + cls.__name__
            visit_func = getattr(visitor, func_name, None)
            if visit_func is not None:
                return visit_func(self, ctx)
        raise Exception(f"visit function for {self.name} not implemented")

class DataType(EnumOP):
    INT = 1
    FLOAT = 2
    STR = 3
    BOOL = 4
    UNKNOWN = 5
    
    def __str__(self):
        return self.name.lower()
    
class ContainerType(EnumOP):
    VEC = 1
    HASH = 2
    ORDERED_MAP = 3
    FILE = 4
    STREAMING = 5
    
    def __str__(self):
        return self.name.lower()

class ArithmeticOp(EnumOP):
    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4
    
    def __str__(self):
        return self.name
    
class CompareOp(EnumOP):
    EQ = 1
    GT = 2
    LT = 3
    GE = 4
    LE = 5
    NEQ = 6
    
    def __str__(self) -> str:
        return self.name

class LogicalOp(EnumOP):
    AND = 1
    OR = 2
    NOT = 3
    
    def __str__(self) -> str:
        return self.name


class Reducer(EnumOP):
    COUNT = 1
    SUM = 2
    AVG = 3
    MIN = 4
    MAX = 5
    
    def __str__(self) -> str:
        return self.name

#single value
class SingleValue(IRNode):
    def __init__(self):
        super().__init__()

class Column(SingleValue):
    def __init__(self, table_name: str, column_name: str, dtype: DataType):
        super().__init__()
        self.tname = table_name
        self.cname = column_name
        self.dtype = dtype

    def __str__(self):
        return f"{self.__class__.__name__}:{self.tname}.{self.cname} {self.dtype}"

class Literal(SingleValue):
    def __init__(self, dtype: DataType, val):
        super().__init__()
        self.dtype = dtype
        self.val = val
    
    def __str__(self):
        return f"{self.__class__.__name__}:{self.val} {self.dtype}"

class Var(SingleValue):
    def __init__(self, name: str, dtype: DataType):
        super().__init__()
        self.name = name
        self.dtype = dtype
    
    def __str__(self):
        return f"{self.__class__.__name__}:{self.name} {self.dtype}"
    
class FunctionDefiniton(IRNode):
    def __init__(self, name: str, params: List[DataType], ret: DataType):
        super().__init__()
        self.name = name
        self.params = params
        self.ret = ret
        
    def __str__(self):
        return f"{self.__class__.__name__}:{self.name} {self.params} -> {self.ret}"

class FunctionCall(SingleValue):
    def __init__(self, func: FunctionDefiniton, params: List[SingleValue]):
        super().__init__()
        self.func = func
        self.params = params
    
    def value(self):
        # return the return value of the function
        raise NotImplementedError

    def __str__(self):
        return f"{self.__class__.__name__}:{self.func.name} {self.params}"

class Expression(SingleValue):
    def __init__(self, lhs: SingleValue, rhs: SingleValue, op: ArithmeticOp):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
        
    def value(self):
        # return the value of the expression
        raise NotImplementedError
    
    def __str__(self):
        return f"{self.__class__.__name__}:{self.lhs} {self.op} {self.rhs}"

class Assignment(IRNode):
    def __init__(self, lhs: Union[Var, Column], rhs: SingleValue):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs
        
    def __str__(self):
        return f"{self.__class__.__name__}:{self.lhs} := {self.rhs}"        

# multiple value
class MultipleValue(IRNode):
    def __init__(self):
        super().__init__()


class StructType(IRNode):
    def __init__(self, name: str, fields: List[Tuple[str, Union[StructType,DataType]]]):
        super().__init__()
        self.name = name
        self.fields = fields
        
    def __str__(self):
        return f"{self.__class__.__name__}:{self.name} {self.fields}"

class StructValue(MultipleValue):
    def __init__(self, vals: List[Union[StructValue, SingleValue]]):
        super().__init__()
        self.vals = vals
        
    def __str__(self):
        return f"{self.__class__.__name__}:{self.vals}"
    
class TableDefinition(IRNode):
    def __init__(self, name: str, schema: StructType, hint: str):
        super().__init__()
        self.name = name
        self.schema = schema  
        self.hint = hint  
        
    def __str__(self):
        return f"{self.__class__.__name__}:{self.name} {self.schema} {self.hint}"

class TableInstance(MultipleValue):
    def __init__(self, definition: TableDefinition, ctype: ContainerType, initvals: List[StructValue]):
        super().__init__()    
        self.definition = definition
        self.ctype = ctype
        self.initvals = initvals
        
    def __str__(self):
        return f"{self.__class__.__name__}:{self.definition} {self.ctype} {self.initvals}"


class Condition(IRNode):
    def __init__(self):
        super().__init__()
        self.read = []

    def getread(self):
        return self.read

class AlgebraCondition(Condition):
    def __init__(self, lhs: SingleValue, rhs: SingleValue, op: CompareOp):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
        self.read = []
        if isinstance(self.lhs, Column):
            self.read += [self.lhs]
        elif isinstance(self.lhs, Condition):
            self.read += self.lhs.read
        if isinstance(self.rhs, Column):
            self.read += [self.rhs]
        elif isinstance(self.rhs, Condition):
            self.read += self.rhs.read
        
    def __str__(self):
        return f"{self.__class__.__name__}:{self.lhs} {self.op} {self.rhs}"
        
class LogicalCondition(Condition):
    def __init__(self, lhs: Condition, rhs: Condition, op: LogicalOp):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
        self.read = []
        if self.op == LogicalOp.NOT:
            self.read = self.lhs.read
            assert(isinstance(self.lhs, Condition))
            assert self.rhs is None
        else:
            if isinstance(self.lhs, Column):
                self.read += [self.lhs]
            elif isinstance(self.lhs, Condition):
                self.read += self.lhs.read
            if isinstance(self.rhs, Column):
                self.read += [self.rhs]
            elif isinstance(self.rhs, Condition):
                self.read += self.rhs.read

    def __str__(self):
        return f"{self.__class__.__name__}:{self.lhs} {self.op} {self.rhs}"

class JoinCondition(Condition):
    def __init__(self, table_name: str, lhs: Column, rhs: Column):
        super().__init__()     
        self.tname = table_name
        self.lhs = lhs
        self.rhs = rhs   
        self.read = [self.lhs, self.rhs]

    def __str__(self):
        return f"{self.__class__.__name__}:{self.tname} {self.lhs} = {self.rhs}"

class Operation(IRNode):
    def __init__(self):
        super().__init__()
            
class Copy(Operation, MultipleValue):
    def __init__(self, table_name: str, columns: StructType, join: JoinCondition = None, where: Condition = None, limit: SingleValue = None):
        super().__init__()
        self.tname = table_name
        self.columns = columns
        self.join = join
        self.where = where
        self.limit = limit

    def values(self):
        # return the values of the table
        raise NotImplementedError
    
    def __str__(self):
        return f"{self.__class__.__name__}:{self.tname} Cols:{self.columns}\n {self.join if self.join is not None else ''} {self.where if self.where is not None else ''} {self.limit if self.limit is not None else ''}"
    
class Insert(Operation):
    def __init__(self, table_name: str, vals: List[StructValue], select: Copy = None):
        super().__init__()
        self.tname = table_name
        self.vals = vals
        self.select = select
        if self.select is not None:
            assert self.vals is None
    
    def __str__(self):
        if self.vals is not None:
            return f"{self.__class__.__name__}:{self.tname}{self.vals}"
        else:
            return f"{self.__class__.__name__}:{self.tname}{self.select}"
            
class Update(Operation):
    def __init__(self, table_name: str, assgins: List[Assignment], where: Condition = None):
        super().__init__()
        self.tname = table_name
        self.assigns = assgins
        self.where = where
        
    def __str__(self):
        return f"{self.__class__.__name__}:{self.tname} {self.assigns} {self.where}"
        
class Move(Operation):
    def __init__(self, table_name: str, where: Condition = None):
        super().__init__()
        self.tname = table_name
        self.where = where
        
    def __str__(self):
        return f"{self.__class__.__name__}:{self.tname} {self.where}"
        
class Reduce(Operation, SingleValue):
    def __init__(self, table_name: str, reducer: Reducer, columns: StructType, join: JoinCondition = None, where: Condition = None, limit: Expression = None):
        super.__init__()
        self.tname = table_name
        self.reducer = reducer
        self.columns = columns
        self.join = join
        self.where = where
        self.limit = limit
        
    def value(self):
        # return the value of the reducer
        raise NotImplementedError
    
    def __str__(self):
        return f"{self.__class__.__name__}:{self.tname} {self.reducer} {self.columns} {self.join} {self.where} {self.limit}"

class Root(IRNode):
    def __init__(self, children: List[Operation]):
        super().__init__()
        self.children = children
        
    def __iter__(self):
        return iter(self.children)
    
    def __str__(self):
        return f"{self.__class__.__name__}:" + "".join(["\n\t" + str(c) for c in self.children])

TypeRPC = StructType("RPC", [("meta", StructType("meta", [("src", DataType.STR), ("dst", DataType.STR), ("type", DataType.STR)])), ("payload", StructType("payload", [("data", DataType.STR)]))])

InputTable = TableInstance(TableDefinition("input", TypeRPC, "reserved"), ContainerType.STREAMING, [])

OutputTable = TableInstance(TableDefinition("output", TypeRPC, "reserved"), ContainerType.STREAMING, [])