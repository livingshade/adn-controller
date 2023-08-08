"""
Module that defines the base type of visitor.
"""


from __future__ import annotations

from typing import Callable, List, Protocol, Sequence, TypeVar

from .node import *


def accept(visitor: Visitor, ctx) -> Callable:
    return lambda node: node.accept(visitor, ctx)


# collection chainmap
class Visitor(ABC):
    #  visit each class name in node.py 
    def visitIRNode(self, node: IRNode, ctx):
        raise Exception(f"visit function for {node.__class__.__name__} not implemented")
    def visitRoot(self, node: Root, ctx):
        pass
    def visitDataType(self, node: DataType, ctx):
        pass
    def visitColumn(self, node: Column, ctx):
        pass
    def visitLiteral(self, node: Literal, ctx):
        pass
    def visitVar(self, node: Var, ctx):
        pass
    def visitFunctionDefiniton(self, node: FunctionDefiniton, ctx):
        pass
    def visitFunctionCall(self, node: FunctionCall, ctx):
        pass
    def visitAssignment(self, node: Assignment, ctx):
        pass
    def visitExpression(self, node: Expression, ctx):
        pass
    def visitLogicalOp(self, node: LogicalOp, ctx):
        pass
    def visitCompareOp(self, node: CompareOp, ctx):
        pass
    def visitArithmeticOp(self, node: ArithmeticOp, ctx):
        pass
    def visitReducer(self, node: Reducer, ctx):
        pass
    def visitStructType(self, node: StructType, ctx):
        pass
    def visitTableInstance(self, node: TableInstance, ctx):
        pass
    def visitTableDefinition(self, node: TableDefinition, ctx):
        pass
    def visitOperation(self, node: Operation, ctx):
        pass
    def visitCopy(self, node: Copy, ctx):
        pass
    def visitInsert(self, node: Insert, ctx):
        pass
    def visitMove(self, node: Move, ctx):
        pass
    def visitReduce(self, node: Reduce, ctx):
        pass
    def visitUpdate(self, node: Update, ctx):
        pass
    def visitCondition(self, node: Condition, ctx):
        pass
    def visitLogicalCondition(self, node: LogicalCondition, ctx):
        pass
    def visitAlgebraCondition(self, node: AlgebraCondition, ctx):
        pass
    def visitJoinCondition(self, node: JoinCondition, ctx):
        pass

