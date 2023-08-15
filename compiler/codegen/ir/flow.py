from typing import Callable, List, Protocol, Sequence, TypeVar, Dict
from .visitor import Visitor, accept
from .node import *
from compiler.protobuf import *

class Edge():
    def __init__(self, u: int, v: int, conds: List[Condition], trans: List[Tuple[str, str]] = []) -> None:
        self.u = u
        self.v = v
        self.conds = conds
        self.trans = trans

class Node():
    def __init__(self, name: str, idx: int, temp: bool) -> None:
        self.name = name
        self.idx = idx
        self.temp = temp
        self.edge_out = []
        self.edge_in = []
        
    def add_edge(self, e: Edge) -> None:
        if e.u == self.idx:
            self.edge_out.append(e)
        elif e.v == self.idx:
            self.edge_in.append(e)
        else:
            raise Exception("Edge not connected to node")
    
    
def newnode() -> int:
    x = 0
    while True:
        yield x
        x = x + 1

class FlowGraph():
    def __init__(self) -> None:
        self.gen = newnode()
        self.nodes: List[Node] = []
        self.n2id: dict[str, int] = {}
        self.t2n: dict[str, List[str]] = {}
        
    def has_node(self, name: str) -> bool:
        return name in self.n2id.keys()
    
    def add_node(self, node: Node) -> None:
        assert(not self.has_node(node.name))
        while len(self.nodes) <= node.idx:
            self.nodes.append(None)
        self.nodes[node.idx] = node   
        self.n2id[node.name] = node.idx
        
    def link(self, u: str, v: str, conds: List[Condition]) -> None:
        assert(self.has_node(u))
        assert(self.has_node(v))
        l = self.n2id[u]
        r = self.n2id[v]
        e = Edge(l, r, conds) 
        self.nodes[l].add_edge(e)
        self.nodes[r].add_edge(e)
    
    def reg_table(self, tname: str) -> str:
        if tname not in self.t2n.keys():
            idx = next(self.gen)
            name = f"{tname}_{idx}"
            self.t2n[tname] = [name]
            self.add_node(Node(name, idx, False))
        return self.t2n[tname][-1]
    
    # returns (newname, oldname)
    def update_table(self, tname: str, note: str = "") -> Tuple[str, str]:
        assert(tname in self.t2n.keys())
        idx = next(self.gen)
        name = f"{tname}_{idx}_{note}"
        self.t2n[tname].append(name)
        self.add_node(Node(name, idx, False))
        return self.t2n[tname][-1], self.t2n[tname][-2]
    
    def retrieve_table(self, tname: str) -> str:
        if not tname in self.t2n.keys():
            raise Exception(f"Table {tname} not registered")
        return self.t2n[tname][-1]
    
    def report(self) -> str:
        ret = ""
        for n in self.nodes:
            for e in n.edge_out:
                u = self.nodes[e.u].name
                v = self.nodes[e.v].name
                conds = [str(i.__class__.__name__) for i in e.conds]
                ret += f"{u} -> {v} {conds}\n"
        return ret
    
    def column2field(self, col: Column) -> str:
        pass
    
    def backtrace(self, cond: Condition):
        pass            
    
    def infer(self, proto: ProtoMessage) -> Tuple[List[str], List[str], bool]:
        
        input_id = self.t2n["input"]
        assert(len(input_id) == 1)
        input_id = self.n2id[input_id[0]]
        
        output_id = self.t2n["output"][-1]
        output_id = self.n2id[output_id]
        
        read = set()
        written = set()
        drop = True

        # read & write
        visited = set()
        q = [input_id]
        while len(q) > 0:
            u = q.pop()
            if u in visited:
                continue
            visited.add(u)
            node = self.nodes[u]
            for e in node.edge_out:
                v = e.v
                if v not in visited:
                    q.append(v)
                for cond in e.conds:
                    if isinstance(cond, Condition):
                        read_cols: List[Column] = cond.getread()
                        for col in read_cols:
                            # todo consider chorno order
                            # the tid it refers to may not be the latest
                            tid = self.n2id[self.t2n[col.tname][-1]]
                            if tid in visited:
                                proto_field = proto.from_name(col.cname)
                                if proto_field is not None:
                                    read.add(proto_field)
                                else:
                                    raise Exception(f"Field {col.cname} not in proto message!")
        
        # drop                        
        visited = set()
        q = [input_id]
        while len(q) > 0:
            u = q.pop()
            if u in visited:
                continue
            visited.add(u)
            node = self.nodes[u]
            for e in node.edge_out:
                v = e.v
                if len(e.conds) > 0:
                    continue
                if v not in visited:
                    q.append(v)
        drop = output_id not in visited
        
        return list(read), list(written), drop   
    
class Scanner(Visitor):
    def __init__(self, tables: List[TableInstance]) -> None:
        self.read = []
        self.write = []
        self.possible_drop = True
        self.tables: Dict[str, TableInstance] = tables
        
    def visitRoot(self, node: Root, ctx: FlowGraph) -> None:
        for t in self.tables.values():
            t.accept(self, ctx)
        
        for ch in node.children:
            ch.accept(self, ctx)
    
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
        pass
    
    def visitExpression(self, node: Expression, ctx: int) -> str:
        raise NotImplementedError
    
    def visitEnumOp(self, node: EnumOP, ctx) -> None:
        pass
    
    def visitStructType(self, node: StructType, ctx):
        pass
    
    def visitStructValue(self, node: StructValue, ctx):
        pass
    
    def visitTableInstance(self, node: TableInstance, ctx: FlowGraph) -> str:
        name = node.definition.name
        node_name = ctx.reg_table(name)
        return node_name
    
    def visitTableDefinition(self, node: TableDefinition, ctx: int) -> str:
        return node.tname
    
    def visitOperation(self, node: Operation, ctx: int) -> str:
        raise NotImplementedError
    
    def visitCopy(self, node: Copy, ctx: FlowGraph) -> str:
        conds = []
        table_node = ctx.retrieve_table(node.tname)
        if node.join is not None:
            join_table = node.join.accept(self, ctx)
            idx_pre = next(ctx.gen)
            idx_after = next(ctx.gen)
            pre_node = Node(f"pre_join_{node.tname}_{join_table}_{idx_pre}", idx_pre, True)
            after_node = Node(f"after_join_{node.tname}_{join_table}_{idx_after}", idx_after, True)

            ctx.add_node(pre_node)
            ctx.add_node(after_node)
            ctx.link(table_node, pre_node.name, [])
            ctx.link(join_table, pre_node.name, [])
            ctx.link(pre_node.name, after_node.name, [node.join] if node.where is None else [node.join, node.where])
            return after_node.name
        else:
            if node.where is not None:
                conds.append(node.where)
            if node.limit is not None:
                conds.append(node.limit)
            idx = next(ctx.gen)
            temp_node = Node(f"copy_{node.tname}_{idx}", idx, True)
            ctx.add_node(temp_node)
            ctx.link(table_node, temp_node.name, conds)   
        return temp_node.name 
    
    def visitInsert(self, node: Insert, ctx: FlowGraph) -> None:
        table_node = ctx.retrieve_table(node.tname)
        if node.vals is not None:
            return;
        if node.select is not None:
            temp_node_name = node.select.accept(self, ctx)
            ctx.link(temp_node_name, table_node, [])
        return;
    
    def visitMove(self, node: Move, ctx: FlowGraph) -> str:
        conds = []
        table_node = ctx.retrieve_table(node.tname)
        if node.where is not None:
            conds.append(node.where)
        idx = next(ctx.gen)
        temp_node = Node(f"move_{node.tname}_{idx}", idx, True)
        ctx.add_node(temp_node)
        ctx.link(table_node, temp_node.name, conds)
        return temp_node.name

    def visitReduce(self, node: Reduce, ctx: FlowGraph) -> str:
        raise NotImplementedError
            
    def visitUpdate(self, node: Update, ctx: FlowGraph) -> str:
        raise NotImplementedError
    
    def visitCondition(self, node: Condition, ctx: int):
        pass
    
    def visitLogicalCondition(self, node: LogicalCondition, ctx: int) -> str:
        pass  
    
    def visitAlgebraCondition(self, node: AlgebraCondition, ctx: int) -> str:
        pass
    
    def visitJoinCondition(self, node: JoinCondition, ctx: int) -> str:
        tname = node.tname
        return ctx.retrieve_table(tname)
    