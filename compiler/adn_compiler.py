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
from compiler.protobuf import HelloProto

class ADNCompiler:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.parser = ADNParser()
        self.transformer = ADNTransformer()
        self.builder = IRBuilder()
        self.generator = CodeGenerator()

    def parse(self, sql):
        ast = self.parser.parse(sql)
        if self.verbose:
            print(ast)
        return self.transformer.transform(ast)

    def buildir(self, sql) -> ir.Root:
        root = self.builder.visitRoot(sql)
        printer = IRPrinter()
        ctx = self.builder.ctx
        print(printer.visitRoot(root, 0))
        return root
    
    def analyze(self, root: ir.Root):
        irctx = self.builder.ctx
        scanner = Scanner(irctx.table_map)
        ctx = FlowGraph()
        root.accept(scanner, ctx)    
        rep = ctx.report()
        print(rep)
        read, write, drop = ctx.infer(HelloProto.from_name("HelloRequest"))
        print(f"read: {read}, write: {write}, drop: {drop}")
        
    def gen(self, sql, ctx: Context):
        return self.generator.visitRoot(sql, ctx)
        # return visit_root(sql, ctx)

    def finalize(self, engine: str, ctx: Context, output_dir: str):
        return finalize(engine, ctx, output_dir)


    def compile(self, elem: Element, output_dir: str):
        init, process = elem.sql
        ctx: Context = init_ctx()

        init, process = self.parse(init), self.parse(process)
        # todo verbose

        print("build ir init")
        init = self.buildir(init)
        
        print("build ir process")
        process = self.buildir(process) 
        
        self.analyze(process)       
        # init = self.gen(init, ctx)
        # while ctx.empty() is False:
        #     ctx.init_code.append(ctx.pop_code())
        # ctx.current = "process"
        # process = self.gen(process, ctx)
        # while ctx.empty() is False:
        #     ctx.process_code.append(ctx.pop_code())
        # return finalize(elem.name, ctx, output_dir)
