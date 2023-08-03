import compiler.tree.visitor as SQLVisitor 
import compiler.tree.node as front
import node as ir
from .context import IRContext
from typing import List, Tuple, Union


def SQLType2IRType(sql_type: front.DataType) -> ir.DataType:
    if sql_type.sql_type() == "VARCHAR":
        return ir.DataType.STRING
    elif sql_type.sql_type() == "FILE":
        return ir.DataType.UNKNOWN
    elif sql_type.sql_type() == "TIMESTAMP":
        return ir.DataType.STRING
    else:
        raise ValueError("Unrecognized SQL type")

class IRBuilder(SQLVisitor):
    def __init__(self):
        self.ir = ir.Root([])
        self.ctx = IRContext()

    def visitRoot(self, node: List[front.Statement]) -> None:
        for statement in node:
            try:
                # print("visitRoot", statement)
                statement.accept(self)
            except Exception as e:
                print(statement)
                raise e

    def visitColumnValue(self, node: front.ColumnValue) -> ir.Column:
        return ir.Column(node.table_name, node.column_name, ir.DataType.UNKNOWN, None)

    def visitFunctionValue(self, node: front.FunctionValue):
        raise NotImplementedError

    def visitVariableValue(self, node: front.VariableValue):
        return ir.Var(node.value, ir.DataType.UNKNOWN, None)

    def visitStringValue(self, node: front.StringValue):
        return ir.Literal(ir.DataType.STRING, node.value)

    def visitNumberValue(self, node: front.NumberValue):
        return ir.Literal(ir.DataType.FLOAT, float(node.value))

    def visitLogicalOp(self, node: front.LogicalOp):
        if node == front.LogicalOp.AND:
            return ir.LogicalOp.AND
        elif node == front.LogicalOp.OR:
            return ir.LogicalOp.OR
        else:
            raise NotImplementedError

    def visitCompareOp(self, node: front.CompareOp):
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


    def visitArithmeticOp(self, node: front.ArithmeticOp):
        if node == front.ArithmeticOp.ADD:
            return ir.ArithmeticOp.ADD
        elif node == front.ArithmeticOp.SUB:
            return ir.ArithmeticOp.SUB
        elif node == front.ArithmeticOp.MUL:
            return ir.ArithemeticOp.MUL
        elif node == front.ArithmeticOp.DIV:
            return ir.ArithemeticOp.DIV
        else:
            raise NotImplementedError

    def visitCreateTableStatement(
        self, node: front.CreateTableStatement
    ) -> None:
        table_name = node.table_name
        if table_name.endswith("_file"):
            hint = "file"
            table_name = table_name[:-5]
        else:
            hint = "mem"
        columns = node.columns
        fields: List[(str, ir.DataType)] = []
        for c, t in columns:
            c = c.accept(self)
            t = SQLType2IRType(t)
            fields.append((c, t))
        schema = ir.StructType("Gen" + table_name, fields)
        if self.ctx.table_map.get(table_name) is not None:
            raise Exception(f"Table {table_name} already exists")
        table_def = ir.TableDefinition(table_name, columns, hint)
        table = ir.TableInstance(table_def,  ir.ContainerType.FILE if hint == "file" else ir.ContainerType.VEC, [])
        self.ctx.table_map[table_name] = table
        
    def visitCreateTableAsStatement(self, node: front.CreateTableAsStatement):
        table = node.table_name
        copy = node.select_stmt.accept(self)
        #todo
        
    def visitInsertSelectStatement(self, node: front.InsertSelectStatement):
        table = node.table_name
        columns = node.columns
        copy = node.select_stmt.accept(self)

    def visitSelectStatement(self, node: front.SelectStatement) -> Union[ir.Copy, ir.Reduce] :
        table = node.table_name
        if self.ctx.table_map.get(table) is None:
            raise Exception(f"Table {table} does not exist")
        table = self.ctx.table_map[table]
        columns: List[ir.Column] = [c.accept(self) for c in node.columns]
        #todo
        return ir.Copy(node.table_name, )

    def visitInsertValueStatement(self, node: front.InsertValueStatement) -> ir.Insert:
        table = node.table_name
        if self.ctx.table_map.get(table) is None:
            raise Exception(f"Table {table} does not exist")
        table = self.ctx.table_map[table]
        
        columns = node.columns
        columns = [c.accept(self) for c in columns]
        columns = [ir.Column(node.table_name, c.cname, c.dtype, None) for c in columns]

        svs = []
        for sv in node.values:
            vs = []
            for v in sv:
                li: ir.Literal = v.accept(self)
                vs.append(li)
            svs.append(ir.StructValue(vs))

        return ir.Insert(node.table_name, svs)
   

    def visitSetStatement(self, node: front.SetStatement) -> ir.Assignment:
        var = node.accept(self)
        expr = node.expr.accept(self)
        return ir.Assignment(var, expr)
        
    def visitSearchCondition(self, node: front.SearchCondition) -> ir.Condition:
        lhs = node.lvalue.accept(self)
        rhs = node.rvalue.accept(self)
        op = node.operator.accept(self)
        if isinstance(op, ir.CompareOp):
            return ir.AlgebraCondition(lhs, rhs, op)
        elif isinstance(op, ir.LogicalOp):
            return ir.LogicalCondition(lhs, rhs, op)
        else:
            raise Exception("Unrecognized condition type")
    
    def visitExpression(self, node: front.Expression) -> ir.Expression:
        lhs = node.lvalue.accept(self)
        rhs = node.rvalue.accept(self)
        op = node.operator.accept(self)
        return ir.Expression(lhs, rhs, op)
        
    
