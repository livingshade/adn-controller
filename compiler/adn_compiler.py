import sys

from lark import Lark
from typing import List, Tuple, Union

from compiler.codegen.codegen import init_ctx
from compiler.codegen.context import Context
from compiler.codegen.finalizer import finalize
from compiler.codegen.generator import CodeGenerator
from compiler.frontend.parser import ADNParser, ADNTransformer
from compiler.graph.element import Element
from compiler.codegen.ir.builder import IRBuilder, IRContext
from compiler.codegen.ir.printer import IRPrinter
from compiler.codegen.ir.flow import Scanner, FlowGraph
import compiler.codegen.ir.node as ir
from compiler.protobuf import HelloProto, ExampleProtoMsg
from compiler.codegen.ir.rustgen import RustGenerator, RustContext

class ADNCompiler:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.parser = ADNParser()
        self.transformer = ADNTransformer()
        self.builder = None
        self.generator = CodeGenerator()
        self.rustgen = None 
        self._protomsg = None

    @property
    def protomsg(self):
        return self._protomsg
    
    @protomsg.setter
    def protomsg(self, protomsg):
        self._protomsg = protomsg

    def parse(self, sql):
        ast = self.parser.parse(sql)
        if self.verbose:
            print(ast)
        return self.transformer.transform(ast)

    def buildir(self, sql) -> ir.Root:
        self.builder = IRBuilder(self.protomsg)
        root = self.builder.visitRoot(sql)
        printer = IRPrinter()
        print(printer.visitRoot(root, 0))
        return root
    
    def analyze(self, root: ir.Root) -> dict:
        irctx = self.builder.ctx
        scanner = Scanner(irctx.table_map)
        ctx = FlowGraph(self.protomsg)
        root.accept(scanner, ctx)    
        rep = ctx.report()
        print(rep)
        read, write, drop = ctx.infer()
        return {
            "read": read,
            "write": write,
            "drop": drop,
        }
        
    def gen(self, sql, ctx: Context):
        return self.generator.visitRoot(sql, ctx)
        # return visit_root(sql, ctx)
        
    def gen_rust(self, root: ir.Root):
        ctx = RustContext()
        self.rustgen = RustGenerator()
        return self.rustgen.visitRoot(root, ctx)

    def finalize(self, engine: str, ctx: Context, output_dir: str):
        return finalize(engine, ctx, output_dir)

    def compile(self, elem: Element, output_dir: str):
        init, process = elem.sql
        ctx: Context = init_ctx()

        init, process = self.parse(init), self.parse(process)
        # todo verbose

        print("build ir")
        ir = self.buildir((init, process))
                
        res = self.analyze(ir)    
        print("Ana result: ", res)
        
        res = self.gen_rust(ir)   
        
