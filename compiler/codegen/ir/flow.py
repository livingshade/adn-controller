from typing import Callable, List, Protocol, Sequence, TypeVar
from .visitor import Visitor, accept
from .node import *

def newnode() -> int:
    x = 0
    while True:
        x = x + 1
        yield x

class Edge():
    def __init__(self, u: int, v: int, conds: List[Condition]) -> None:
        u = u
        v = v
        conds = conds

class Node():
    def __init__(self, name: str, temp: bool) -> None:
        self.name = name
        self.idx = newnode()
        self.edges = []
        self.temp = temp
        
    def add_edge(self, e: Edge) -> None:
        assert(e.u == self.idx)
        self.edges.append(e)

class FlowGraph():
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
    def has_node(self, name: str) -> bool:
        return name in self.nodes
    def add_node(self, name: str, temp: bool) -> None:
        assert(not self.has_node(name))
        self.nodes[name] = Node(name, temp)    
    

class Scanner(Visitor):
    def __init__(self) -> None:
        read = []
        write = []
        possible_drop = True
    
    def visitRoot(self, node: Root, ctx: FlowGraph) -> None:
        for ch in node.children:
            ret += ch.accept(self, ctx)
    
    def visitDataType(self, node: DataType, ctx: FlowGraph) -> None:
        pass
    
    def visitColumn(self, node: Column, ctx: FlowGraph) -> None:
        pass
    
    def visitLiteral(self, node: Literal, ctx):
        pass
    
    def visitVar(self, node: Var, ctx):
        pass
    
    def visitFunctionDefiniton(self, node: FunctionDefiniton, ctx):
        pass
    
    def visitFunctionCall(self, node: FunctionCall, ctx):
        pass
    
    def visitAssignment(self, node: Assignment, ctx: FlowGraph) -> None:
        #todo read from assignment
        raise NotImplementedError
    
    def visitExpression(self, node: Expression, ctx: int) -> str:
        raise NotImplementedError
    
    def visitEnumOp(self, node: EnumOP, ctx) -> None:
        pass
    
    def visitStructType(self, node: StructType, ctx):
        pass
    
    def visitStructValue(self, node: StructValue, ctx):
        pass
    
    def visitTableInstance(self, node: TableInstance, ctx: FlowGraph) -> str:
        if not ctx.has_node(node.tname):
            ctx.add_node(node.tname, False)        
        return node.definition.accept(self, ctx)
    
    def visitTableDefinition(self, node: TableDefinition, ctx: int) -> str:
        return node.tname
    
    def visitOperation(self, node: Operation, ctx: int) -> str:
        raise NotImplementedError
    
    def visitCopy(self, node: Copy, ctx: FlowGraph) -> str:
        conds = []
        ret =  f"Copy: {node.tname}" + '\n' + tab(ctx)
        ret += f"{node.columns.accept(self, ctx + 1)}\n" + tab(ctx)
        if node.join is not None:
            conds += node.join
        if node.where is not None:
            conds += node.where
        if node.limit is not None:
            raise NotImplementedError
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
        ret += f"{node.columns.accept(self, ctx + 1)}\n" + tab(ctx)
        if node.where is not None:
            ret += node.where.accept(self, ctx + 1) + '\n' + tab(ctx)

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
        return f"Update: {node.table} {node.assignments}"
    
    def visitCondition(self, node: Condition, ctx: int) -> str:
        return f"Condition: {node.op}"
    
    def visitLogicalCondition(self, node: LogicalCondition, ctx: int) -> str:
        ret = f"LogicCond:\n" + tab(ctx)
        ret += {node.lhs.accept(self, ctx + 1)} + '\n' + tab(ctx)
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
    