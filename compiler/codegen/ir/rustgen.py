"""
Module that defines the base type of visitor.
"""


from __future__ import annotations

from typing import Callable, List, Sequence, TypeVar, Dict
from .visitor import Visitor
from .node import *
from compiler.backend.mrpc import *
from compiler.protobuf import ProtoMessage
from collections import ChainMap

# collection chainmap
class RustGenerator(Visitor):
    #  visit each class name in node.py 
    def visitIRNode(self, node: IRNode, ctx: RustContext):
        raise Exception(f"visit function for {node.__class__.__name__} not implemented")
    
    def visitRoot(self, node: Root, ctx: RustContext):
        
        for decl in node.definition:
            try:
                code = decl.accept(self, ctx)
            except Exception as e:
                print("Error on def: ", e)
                continue
            ctx.def_code.append(code)
            
        for i in node.init:
            try:
                code = i.accept(self, ctx)
            except Exception as e:
                print("Error on init: ", e)
                continue
            ctx.init_code.append(code)
            
        for p in node.process:
            try:
                code = p.accept(self, ctx)
            except Exception as e:
                print("Error on process: ", e)
                continue
            ctx.process_code.append(code)
            
        return;
        
    def visitDataType(self, node: DataType, ctx: RustContext) -> RustBasicType:
        if node == DataType.INT:
            return RustBasicType("i32")
        elif node == DataType.FLOAT:
            return RustBasicType("f32")
        elif node == DataType.STRING:
            return RustBasicType("String")
        elif node == DataType.BOOL:
            return RustBasicType("bool")
        elif node == DataType.UNKNOWN:
            raise Exception("unknown data type")
        
    def visitColumn(self, node: Column, ctx: RustContext):
        pass
    
    def visitLiteral(self, node: Literal, ctx: RustContext) -> str:
        if node.dtype == DataType.INT:
            return node.val
        elif node.dtype == DataType.FLOAT:
            return f"({node.val} as f32)"
        else:
            return node.val
    
    def visitVar(self, node: Var, ctx: RustContext) -> str:
        if ctx.n2rv.get(node.name) is None:
            raise Exception(f"variable {node.name} not defined")
        var = ctx.n2rv[node.name]
        return var.name 
    
    def visitFunctionDefiniton(self, node: FunctionDefiniton, ctx: RustContext)-> None:
        if ctx.f2rf.get(node.name) is None:
            ctx.f2rf[node.name] = RustFunctionType(node.name, [a.accept(self, ctx) for a in node.args], node.ret.accept(self, ctx))
        else:
            raise Exception(f"function {node.name} already defined")
    
    def visitFunctionCall(self, node: FunctionCall, ctx: RustContext) -> str:
        if ctx.f2rf.get(node.name) is None:
            raise Exception(f"function {node.name} not defined")
        else:
            func = ctx.f2rf[node.name]
            return f"{func.name}({','.join([a.accept(self, ctx) for a in node.args])})"
    
    def visitAssignment(self, node: Assignment, ctx: RustContext) -> str:
        return f"{node.lhs.accept(self, ctx)} = {node.rhs.accept(self, ctx)};";
    
    def visitExpression(self, node: Expression, ctx: RustContext):
        return f"{node.lhs.accept(self, ctx)} {node.op.accept(self, ctx)} {node.rhs.accept(self, ctx)}"
    
    def visitLogicalOp(self, node: LogicalOp, ctx: RustContext):
        if node == LogicalOp.AND:
            return "&&"
        elif node == LogicalOp.OR:
            return "||"
        elif node == LogicalOp.NOT:
            return "!"
        else:
            raise Exception("unknown logical operator")
        
    def visitCompareOp(self, node: CompareOp, ctx: RustContext):
        if node == CompareOp.EQ:
            return "=="
        elif node == CompareOp.NE:
            return "!="
        elif node == CompareOp.GT:
            return ">"
        elif node == CompareOp.GE:
            return ">="
        elif node == CompareOp.LT:
            return "<"
        elif node == CompareOp.LE:
            return "<=" 
        else:
            raise Exception("unknown compare operator")           
        
    def visitArithmeticOp(self, node: ArithmeticOp, ctx: RustContext):
        if node == ArithmeticOp.ADD:
            return "+"
        elif node == ArithmeticOp.SUB:
            return "-"
        elif node == ArithmeticOp.MUL:
            return "*"
        elif node == ArithmeticOp.DIV:
            return "/"
    
    def visitReducer(self, node: Reducer, ctx: RustContext):
        raise NotImplementedError
    
    def visitStructType(self, node: StructType, ctx: RustContext):
        pass
    
    def visitTableInstance(self, node: TableInstance, ctx: RustContext) -> str:
        name = node.definition.name
        if ctx.t2rc.get(name) is None:
            raise Exception(f"table {name} not defined")
        else:
            table = ctx.t2rc[name]
            return f"{table.name}"
    
    def visitTableDefinition(self, node: TableDefinition, ctx: RustContext) -> None:
        if ctx.t2rc.get(node.name) is None:
            #todo
            ctx.t2rc[node.name] = RustContainerType(node.name, [a.accept(self, ctx) for a in node.columns])
        else:
            raise Exception(f"table {node.name} already defined")
        
    def visitOperation(self, node: Operation, ctx: RustContext):
        raise NotImplementedError
    
    def visitCopy(self, node: Copy, ctx: RustContext):
        tname = node.table.name
        if ctx.t2rc.get(tname) is None:
            raise Exception(f"table {tname} not defined")
        tname = ctx.t2rc[tname].name
        
        print("Column: ", node.columns) 
        raise NotImplementedError
    
    def visitInsert(self, node: Insert, ctx: RustContext) -> str:
        tname = node.table.name
        if ctx.t2rc.get(tname) is None:
            raise Exception(f"table {tname} not defined")
        tname = ctx.t2rc[tname].name
        
        if node.select is not None:
            select = node.select.accept(self, ctx)
            code = f"for event in {select} {{\n"
            code += f"{tname}.push(event);\n"
            code += "}\n"
        else:
            code = ""
            for vals in node.values:
                code += f"{tname}.push({vals.accept(self, ctx)});\n"
        return code
    
    def visitMove(self, node: Move, ctx: RustContext):
        pass
    
    def visitReduce(self, node: Reduce, ctx: RustContext):
        pass
    
    def visitUpdate(self, node: Update, ctx: RustContext):
        pass
    
    def visitCondition(self, node: Condition, ctx: RustContext):
        raise NotImplementedError
    
    def visitLogicalCondition(self, node: LogicalCondition, ctx: RustContext) -> str:
        return f"{node.lhs.accept(self, ctx)} {node.op.accept(self, ctx)} {node.rhs.accept(self, ctx)}"
    
    def visitAlgebraCondition(self, node: AlgebraCondition, ctx: RustContext) -> str:
        return f"{node.lhs.accept(self, ctx)} {node.op.accept(self, ctx)} {node.rhs.accept(self, ctx)}"
    
    def visitJoinCondition(self, node: JoinCondition, ctx: RustContext) -> str:
        return f"{node.lhs.accept(self, ctx)} == {node.rhs.accept(self, ctx)}"

class RustContext:
    def __init__(
        self, tables: List[str], vars: List[Var], protomsg: ProtoMessage,
    ):
        self.t2rc: Dict[str, RustContainerType] = {};
        self.n2rv: Dict[str, RustVariable] = {};
        self.f2rf: Dict[str, RustFunctionType] = {};
        self._def_code = []
        self._init_code = []
        self._process_code = []
        self._temp_code = []
        self._rust_cons = {}
        self._rust_vars = {}
        self._temp_vars = {}
        self.protomsg = protomsg
        
        self.scope = ChainMap({
            "ns": "",
            "var": "",
            "struct": "",  
        })
        
    @property
    def def_code(self) -> List[str]:
        return self._def_code

    @def_code.setter
    def def_code(self, value: List[str]):
        self._def_code = value

    @property
    def init_code(self) -> List[str]:
        return self._init_code

    @init_code.setter
    def init_code(self, value: List[str]):
        self._init_code = value

    @property
    def process_code(self) -> List[str]:
        return self._process_code

    @process_code.setter
    def process_code(self, value: List[str]):
        self._process_code = value

    @property
    def tables(self) -> Dict[str, RustContainerType]:
        return self._tables

    @tables.setter
    def tables(self, value: Dict[str, RustContainerType]):
        self._tables = value

    @property
    def rust_vars(self) -> Dict[str, RustVariable]:
        return self._rust_vars

    @rust_vars.setter
    def rust_vars(self, value: Dict[str, RustVariable]):
        self._rust_vars = value

