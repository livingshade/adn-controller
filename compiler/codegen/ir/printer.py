from typing import Callable, List, Protocol, Sequence, TypeVar
from .visitor import Visitor, accept
from .node import *

class IRPrinter(Visitor):
    def __init__(self) -> None:
        pass
    
    def visitRoot(self, node: Root, ctx: int) -> str:
        ret = "Root:\n"
        ret += "  Def:\n"
        for ch in node.definition:
            ret += tab(ctx) + ch.accept(self, ctx + 1)
        ret += "  Init:\n"
        for ch in node.init:
            ret += tab(ctx) + ch.accept(self, ctx + 1)
        ret += "  Process:\n"
        for ch in node.process:
            ret += tab(ctx) + ch.accept(self, ctx + 1)
        return ret
    
    def visitDataType(self, node: DataType, ctx: int) -> str:
        return str(node)
    
    def visitColumn(self, node: Column, ctx: int) -> str:
        return f"Col: {node.tname}.{node.cname} {node.dtype.accept(self, ctx)}"
    
    def visitLiteral(self, node: Literal, ctx: int) -> str:
        return f"Lit: {node.val} {node.dtype.accept(self, ctx)}"
    
    def visitVar(self, node: Var, ctx: int) -> str:
        return f"Var: {node.name}"# {node.dtype.accept(self, ctx)}"
    
    def visitFunctionDefiniton(self, node: FunctionDefiniton, ctx: int) -> str:
        ret = f"FuncDef:\n {node.name}\n" + tab(ctx)
        for param in node.params:
            ret += param.accept(self, ctx + 1) + " "
        ret += '\n' + tab(ctx)
        ret += node.ret.accept(self, ctx + 1); 
        return ret
    
    def visitFunctionCall(self, node: FunctionCall, ctx: int) -> str:
        ret = f"Call: {node.func.name}" 

        if len(node.args) == 0:
            ret += '()'
        else:
            ret += '('
            for arg in node.args:
                ret += arg.accept(self, ctx + 1) + ","
            ret += ')'
        return ret
    
    def visitAssignment(self, node: Assignment, ctx: int) -> str:
        return f"Assign: {node.lhs.accept(self, ctx + 1)} := {node.rhs.accept(self, ctx + 1)}\n"
    
    def visitExpression(self, node: Expression, ctx: int) -> str:
        ret = f"({node.lhs.accept(self, ctx + 1)}" + '\n' + tab(ctx)
        ret += f"{node.op}" + '\n' + tab(ctx) 
        ret += f"{node.rhs.accept(self, ctx + 1)}"
        return ret + ")\n"
    
    def visitLogicalOp(self, node: LogicalOp, ctx: int) -> str:
        return str(node)
    
    def visitCompareOp(self, node: CompareOp, ctx: int) -> str:
        return str(node)
    
    def visitArithmeticOp(self, node: ArithmeticOp, ctx: int) -> str:
        return str(node)
    
    def visitReducer(self, node: Reducer, ctx: int) -> str:
        return str(node)
    
    def visitStructType(self, node: StructType, ctx: int) -> str:
        ret = f"Struct<{node.name}>\n" + tab(ctx) 
        for (name, f) in node.fields:
            ret += f"{name}:" + f.accept(self, ctx + 1) + " "
        return ret
    
    def visitStructValue(self, node: StructValue, ctx: int) -> str:
        ret = "("
        for val in node.vals:
            ret += val.accept(self, ctx + 1) + ", "
        return ret + ")"
    
    def visitTableInstance(self, node: TableInstance, ctx: int) -> str:
        ret = f"TableInstance: {node.ctype}\n" + tab(ctx)       
        ret += f"{node.definition.accept(self, ctx + 1)}\n" + tab(ctx) 
        for iv in node.initvals:
            ret += iv.accept(self, ctx + 1) + " "
        return ret
    
    def visitTableDefinition(self, node: TableDefinition, ctx: int) -> str:
        ret = f"TableDefinition: {node.name}\n" + tab(ctx)
        ret += f"{node.schema.accept(self, ctx + 1)}\n"
    
    def visitOperation(self, node: Operation, ctx: int) -> str:
        return f"Operation: {node.op}"
    
    def visitCopy(self, node: Copy, ctx: int) -> str:
        ret =  f"Copy: {node.tname}" + '\n' + tab(ctx)
        ret += f"{node.columns.accept(self, ctx + 1)}\n" + tab(ctx)
        if node.join is not None:
            ret += f"{node.join.accept(self, ctx + 1)}" + '\n' + tab(ctx)
        if node.where is not None:
            ret += f"{node.where.accept(self, ctx + 1)}" + '\n' + tab(ctx)
        if node.limit is not None:
            ret += f"limit = {node.limit.accept(self, ctx + 1)}" + '\n' + tab(ctx)
        return ret + '\n'
    
    def visitInsert(self, node: Insert, ctx: int) -> str:
        ret = f"Insert: {node.tname}" + '\n' + tab(ctx)
        if node.vals is not None:
            for val in node.vals:
                ret += val.accept(self, ctx + 1) + '\n' + tab(ctx)
        if node.select is not None:
            ret += node.select.accept(self, ctx + 1)
        return ret
    
    def visitMove(self, node: Move, ctx: int) -> str:
        ret =  f"Move: {node.tname}" + '\n' + tab(ctx)
        if node.where is not None:
            ret += node.where.accept(self, ctx + 1) + '\n' + tab(ctx)
        return ret

    def visitReduce(self, node: Reduce, ctx: int) -> str:
        ret =  f"Reduce: {node.tname} {node.reducer}" + '\n' + tab(ctx)
        ret += f"{node.columns.accept(self, ctx + 1)}\n" + tab(ctx)
        if node.join is not None:
            ret += node.join.accept(self, ctx + 1) + '\n' + tab(ctx)
        if node.where is not None:
            ret += node.where.accept(self, ctx + 1) + '\n' + tab(ctx)
        if node.limit is not None:
            ret += "limit= " + node.limit.accept(self, ctx + 1) + '\n' + tab(ctx)    
        return ret + '\n'
            
    def visitUpdate(self, node: Update, ctx: int) -> str:
        ret =  f"Update: {node.tname}\n"
        for assign in node.assigns:
            ret += tab(ctx)+  f"{assign.accept(self, ctx + 1)}\n"
        if node.where is not None:
            ret += tab(ctx) + "where: " + f"{node.where.accept(self, ctx + 1)}\n"
        return ret
    
    def visitCondition(self, node: Condition, ctx: int) -> str:
        return f"Condition: {node.op}"
    
    def visitLogicalCondition(self, node: LogicalCondition, ctx: int) -> str:
        ret = f"LogicCond:\n" + tab(ctx)
        #t1 = node.lhs.accept(self, ctx + 1)
        ret += f"{node.lhs.accept(self, ctx + 1)}\n" + tab(ctx)
        ret += f"{node.op}" + '\n' + tab(ctx)
        ret += f"{node.rhs.accept(self, ctx + 1)}"
        return ret    
    
    def visitAlgebraCondition(self, node: AlgebraCondition, ctx: int) -> str:
        ret = f"AlgebraCond:\n" + tab(ctx)
        ret += f"{node.lhs.accept(self, ctx + 1)}\n" + tab(ctx)
        ret += f"{node.op}" + '\n' + tab(ctx)
        ret += f"{node.rhs.accept(self, ctx + 1)}"  
        return ret  
    
    def visitJoinCondition(self, node: JoinCondition, ctx: int) -> str:
        ret = f"JoinOn: {node.tname}\n" + tab(ctx)
        ret += f"{node.lhs.accept(self, ctx + 1)}\n" + tab(ctx)
        ret += "EQ" + '\n' + tab(ctx)
        ret += f"{node.rhs.accept(self, ctx + 1)}"
        return ret
    
def tab(x: int) -> str:
    return "\t" * x
    