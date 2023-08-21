from compiler.tree.visitor import Visitor as SQLVisitor
import compiler.tree.node as front
import compiler.codegen.ir.node as ir
from compiler.protobuf import Proto
from .context import IRContext
from typing import List, Tuple, Union, Dict
from compiler.protobuf import ProtoMessage

def SQLType2IRType(sql_type: front.DataType) -> ir.DataType:
    if sql_type.sql_type() == "VARCHAR":
        return ir.DataType.STR
    elif sql_type.sql_type() == "FILE":
        return ir.DataType.UNKNOWN
    elif sql_type.sql_type() == "TIMESTAMP":
        return ir.DataType.STR
    elif sql_type.sql_type() == "INT":
        return ir.DataType.INT
    else:
        raise ValueError("Unrecognized SQL type")

class IRBuilder(SQLVisitor):
    def __init__(self, proto: ProtoMessage):
        self.proto = proto
        self.ctx = IRContext()
        self.cur_table = []
        self.funcs: Dict[str, ir.FunctionDefiniton] = {
            "MIN": ir.FunctionDefiniton("MIN", [ir.DataType.UNKNOWN, ir.DataType.UNKNOWN], ir.DataType.UNKNOWN),
            "CUR_TS": ir.FunctionDefiniton("CUR_TS", [], ir.DataType.FLOAT),
            "TIME_DIFF": ir.FunctionDefiniton("TIME_DIFF", [ir.DataType.FLOAT, ir.DataType.FLOAT], ir.DataType.FLOAT),
            "RANDOM": ir.FunctionDefiniton("RANDOM", [], ir.DataType.FLOAT),
        }

    def visitRoot(self, node: Tuple[List[front.Statement], List[front.Statement]], ctx = None) -> ir.Root:
        init_code, process_code = [], []
        init, process = node
        for statement in init:
            try:
                # print("visitRoot", statement)
                ret = statement.accept(self)
                if ret is not None:
                    init_code.append(ret)
            except Exception as e:
                print("Error on init:", statement)
                raise e
            
        for statement in process:
            try:
                # print("visitRoot", statement)
                ret = statement.accept(self)
                if ret is not None:
                    process_code.append(ret)
            except Exception as e:
                print("Error on process:", statement)
                raise e
            
        table_instances = list(self.ctx.table_map.values())
        func_def = list(self.funcs.values())
        defs = table_instances + func_def
        
        return ir.Root(self.proto, defs, init_code, process_code)
    

    def visitColumnValue(self, node: front.ColumnValue, ctx = None) -> ir.Column:
        if node.table_name != "":
            return ir.Column(node.table_name, node.column_name, ir.DataType.UNKNOWN)
        elif len(self.cur_table) > 0:
            return ir.Column(self.cur_table[-1].definition.name, node.column_name, ir.DataType.UNKNOWN)
        else:
            return ir.Column(None, node.column_name, ir.DataType.UNKNOWN)
        
    def visitFunctionValue(self, node: front.FunctionValue, ctx = None) -> ir.FunctionCall:
        fname = node.value
        if self.funcs.get(fname) is None:
            raise Exception(f"Function {fname} not found")
        func = self.funcs[fname]
        
        return ir.FunctionCall(func, [a.accept(self) for a in node.parameters])

    def visitVariableValue(self, node: front.VariableValue, ctx = None) -> ir.Var:
        return ir.Var(node.value, ir.DataType.UNKNOWN)

    def visitStringValue(self, node: front.StringValue, ctx = None) -> ir.Literal:
        return ir.Literal(ir.DataType.STR, node.value)

    def visitNumberValue(self, node: front.NumberValue, ctx = None) -> ir.Literal:
        return ir.Literal(ir.DataType.FLOAT, float(node.value))

    def visitLogicalOp(self, node: front.LogicalOp, ctx = None) -> ir.LogicalOp:
        if node == front.LogicalOp.AND:
            return ir.LogicalOp.AND
        elif node == front.LogicalOp.OR:
            return ir.LogicalOp.OR
        else:
            raise NotImplementedError

    def visitCompareOp(self, node: front.CompareOp, ctx = None) -> ir.CompareOp:
        if node == front.CompareOp.EQ:
            return ir.CompareOp.EQ
        elif node == front.CompareOp.NE:
            return ir.CompareOp.NE
        elif node == front.CompareOp.LT:
            return ir.CompareOp.LT
        elif node == front.CompareOp.LE:
            return ir.CompareOp.LE
        elif node == front.CompareOp.GT:
            return ir.CompareOp.GT
        elif node == front.CompareOp.GE:
            return ir.CompareOp.GE
        else:
            raise NotImplementedError

    def visitArithmeticOp(self, node: front.ArithmeticOp, ctx = None) -> ir.ArithmeticOp:
        if node == front.ArithmeticOp.ADD:
            return ir.ArithmeticOp.ADD
        elif node == front.ArithmeticOp.SUB:
            return ir.ArithmeticOp.SUB
        elif node == front.ArithmeticOp.MUL:
            return ir.ArithmeticOp.MUL
        elif node == front.ArithmeticOp.DIV:
            return ir.ArithmeticOp.DIV
        else:
            raise NotImplementedError

    def visitAggregator(self, node: front.Aggregator, ctx = None) -> ir.Reducer:
        if node == front.Aggregator.COUNT:
            return ir.Reducer.COUNT
        elif node == front.Aggregator.SUM:
            return ir.Reducer.SUM
        elif node == front.Aggregator.AVG:
            return ir.Reducer.AVG
        elif node == front.Aggregator.MIN:
            return ir.Reducer.MIN
        elif node == front.Aggregator.MAX:
            return ir.Reducer.MAX

    def visitCreateTableStatement(
        self, node: front.CreateTableStatement, ctx = None
    ) -> None:
        table_name = node.table_name
        if table_name.endswith("_file"):
            hint = "file"
        else:
            hint = "mem"
        columns = node.columns
        fields: List[(str, ir.DataType)] = []
        for c, t in columns:
            c = c.accept(self)
            t = SQLType2IRType(t)
            fields.append((c.cname, t))
        schema = ir.StructType("Gen" + table_name, fields)
        if self.ctx.table_map.get(node.table_name) is not None:
            raise Exception(f"Table {node.table_name} already exists")
        
        table_def = ir.TableDefinition(table_name, schema, hint)
        table = ir.TableInstance(table_def,  ir.ContainerType.FILE if hint == "file" else ir.ContainerType.VEC, [])
        
        self.ctx.table_map[node.table_name] = table
        
    def visitCreateTableAsStatement(self, node: front.CreateTableAsStatement, ctx = None) -> ir.Insert:
        table = node.table_name
        copy = node.select_stmt.accept(self)
        #todo
        raise NotImplementedError
        
    def visitInsertSelectStatement(self, node: front.InsertSelectStatement, ctx = None) -> ir.Insert:
        table = node.table_name
        if self.ctx.table_map.get(table) is None:
            raise Exception(f"Table {table} does not exist")
        table = self.ctx.table_map[table]
        self.cur_table.append(table)
        columns = node.columns
        copy = node.select_stmt.accept(self)
        assert(isinstance(copy, ir.Copy))
        self.cur_table.pop()
        return ir.Insert(node.table_name, None, copy)

    def visitSelectStatement(self, node: front.SelectStatement, ctx = None) -> Union[ir.Copy, ir.Reduce]:
        table = node.from_table
        if self.ctx.table_map.get(table) is None:
            raise Exception(f"Table {table} does not exist")
        table = self.ctx.table_map[table]
        self.cur_table.append(table)
        columns: List[ir.Column] = [c.accept(self) for c in node.columns]
        
        newtype = ir.StructType("GenCopy" + node.from_table, [(c.cname, c.dtype) for c in columns])
        if len(node.columns) == 1 and node.columns[0] == front.Asterisk:
            newtype = table.definition.schema
        #todo check whether columns match

        join_cond = node.join_clause.accept(self) if node.join_clause is not None else None
        where_cond = node.where_clause.accept(self) if node.where_clause is not None else None
        limit = node.limit.accept(self) if node.limit is not None else None

        self.cur_table.pop()
        if node.aggregator is not None:
            return ir.Reduce(node.from_table, node.aggregator.accept(self), newtype, join_cond, where_cond, limit)
        else:
            return ir.Copy(node.from_table, newtype, join_cond, where_cond, limit)

    def visitInsertValueStatement(self, node: front.InsertValueStatement, ctx = None) -> ir.Insert:
        table = node.table_name
        if self.ctx.table_map.get(table) is None:
            raise Exception(f"Table {table} does not exist")
        table = self.ctx.table_map[table]
        self.cur_table.append(table)
        
        columns = node.columns
        columns = [c.accept(self) for c in columns]
        columns = [ir.Column(node.table_name, c.cname, c.dtype) for c in columns]

        svs = []
        for sv in node.values:
            vs = []
            for v in sv:
                li: ir.Literal = v.accept(self)
                vs.append(li)
            svs.append(ir.StructValue(vs))
        
        self.cur_table.pop()
        return ir.Insert(node.table_name, svs)
   
    def visitDeleteStatement(self, node: front.DeleteStatement, ctx = None) -> ir.Move:
        table = node.table_name
        if self.ctx.table_map.get(table) is None:
            raise Exception(f"Table {table} does not exist")
        table = self.ctx.table_map[table]
        self.cur_table.append(table)
        
        where = node.where_clause.accept(self) if node.where_clause is not None else None
        
        self.cur_table.pop()
        return ir.Move(node.table_name, where)

    def visitUpdateStatement(self, node: front.UpdateStatement, ctx = None) -> ir.Update:
        table = node.table_name
        if self.ctx.table_map.get(table) is None:
            raise Exception(f"Table {table} does not exist")
        table = self.ctx.table_map[table]
        self.cur_table.append(table)
        
        assigns = [a.accept(self) for a in node.assigns]
        where = node.where_clause.accept(self) if node.where_clause is not None else None
        
        self.cur_table.pop()
        return ir.Update(node.table_name, assigns, where)

    def visitSetStatement(self, node: front.SetStatement, ctx = None) -> ir.Assignment:
        var = node.variable.accept(self)
        expr = node.expr.accept(self)
        return ir.Assignment(var, expr)
        
    def visitWhereClause(self, node: front.WhereClause, ctx = None) -> ir.Condition:
        return node.search_condition.accept(self)
    
    def visitJoinClause(self, node: front.JoinClause, ctx = None) -> ir.JoinCondition:
        tname = node.table_name
        cond = node.search_condition.accept(self)
        assert(cond.op == ir.CompareOp.EQ)
        return ir.JoinCondition(tname, cond.lhs, cond.rhs)
        
    def visitSearchCondition(self, node: front.SearchCondition, ctx = None) -> ir.Condition:
        lhs = node.lvalue.accept(self)
        rhs = node.rvalue.accept(self)
        op = node.operator.accept(self)
        if isinstance(op, ir.CompareOp):
            return ir.AlgebraCondition(lhs, rhs, op)
        elif isinstance(op, ir.LogicalOp):
            return ir.LogicalCondition(lhs, rhs, op)
        else:
            raise Exception("Unrecognized condition type")
    
    def visitExpression(self, node: front.Expression, ctx = None) -> ir.Expression:
        lhs = node.lvalue.accept(self)
        rhs = node.rvalue.accept(self)
        op = node.operator.accept(self)
        return ir.Expression(lhs, rhs, op)
        
    
