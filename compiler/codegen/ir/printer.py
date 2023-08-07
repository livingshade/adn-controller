from typing import Callable, List, Protocol, Sequence, TypeVar
from .visitor import Visitor, accept
from .node import *
class IRPrinter(Visitor):
    def __init__(self) -> None:
        pass
    
    def visitRoot(self, node: Root, ctx: int) -> str:
        ret = "Root:\n"
        for stmt in node.statements:
            ret += stmt.accept(self, ctx)
        return ret
    
    def visitDataType(self, node: DataType, ctx: int) -> str:
        return node.name
    
    def visitColumn(self, node: Column, ctx: int) -> str:
        return f"Column: {node.tname}.{node.cname} {node.dtype.accept(self, ctx)}"
    
    def visitLiteral(self, node: Literal, ctx: int) -> str:
        return f"Literal: {node.val} {node.dtype.accept(self, ctx)}"
    
    def visitVar(self, node: Var, ctx: int) -> str:
        return f"Var: {node.name} {node.dtype.accept(self, ctx)}"
    
    def visitFunctionDefiniton(self, node: FunctionDefiniton, ctx: int) -> str:
        return f"FuncDef: {node.name} {node.params} {node.ret.accept(self, ctx)}"
    
    def visitFunctionCall(self, node: FunctionCall, ctx: int) -> str:
        return f"Call: {node.name} {node.params}"
    
    def visitAssignment(self, node: Assignment, ctx: int) -> str:
        return f"Assignment: {node.name} {node.value.accept(self, ctx)}"
    
    def visitExpression(self, node: Expression, ctx: int) -> str:
        return f"Expression: {node.op} {node.left.accept(self, ctx)} {node.right.accept(self, ctx)}"
    
    def visitLogicalOp(self, node: LogicalOp, ctx: int) -> str:
        return f"LogicalOp: {node.op}"
    
    def visitCompareOp(self, node: CompareOp, ctx: int) -> str:
        return f"CompareOp: {node.op}"
    
    def visitArithmeticOp(self, node: ArithmeticOp, ctx: int) -> str:
        return f"ArithmeticOp: {node.op}"
    
    def visitReducer(self, node: Reducer, ctx: int) -> str:
        return f"Reducer: {node.op}"
    
    def visitStructType(self, node: StructType, ctx: int) -> str:
        return f"StructType: {node.name} {node.fields}"
    
    def visitTableInstance(self, node: TableInstance, ctx: int) -> str:
        return f"TableInstance: {node.tname} {node.alias}"
    
    def visitTableDefinition(self, node: TableDefinition, ctx: int) -> str:
        return f"TableDefinition: {node.tname} {node.fields}"
    
    def visitOperation(self, node: Operation, ctx: int) -> str:
        return f"Operation: {node.op}"
    
    def visitCopy(self, node: Copy, ctx: int) -> str:
        return f"Copy: {node.src} {node.dst}"
    
    def visitInsert(self, node: Insert, ctx: int) -> str:
        return f"Insert: {node.table} {node.values}"
    
    def visitMove(self, node: Move, ctx: int) -> str:
        return f"Move: {node.src} {node.dst}"
    
    def visitReduce(self, node: Reduce, ctx: int) -> str:
        return f"Reduce: {node.table} {node.reducer}"
    
    def visitUpdate(self, node: Update, ctx: int) -> str:
        return f"Update: {node.table} {node.assignments}"
    
    def visitCondition(self, node: Condition, ctx: int) -> str:
        return f"Condition: {node.op} {node.left.accept(self, ctx)} {node.right.accept(self, ctx)}"
    
    def visitLogicalCondition(self, node: LogicalCondition, ctx: int) -> str:
        return f"LogicalCondition: {node.op} {node.left.accept(self, ctx)} {node.right.accept(self, ctx)}"
    
    def visitAlgebraCondition(self, node: AlgebraCondition, ctx: int) -> str:
        return f"AlgebraCondition: {node.op} {node.left.accept(self, ctx)} {node.right.accept(self, ctx)}"
    
    
def tab(x: int) -> str:
    return "\t" * x
    