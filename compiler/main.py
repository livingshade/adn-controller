import argparse
import os
import pathlib
import re
import sys

from graph import Graph
from graph.element import Element

from compiler.adn_compiler import ADNCompiler
from compiler.codegen.codegen import *
from compiler.codegen.finalizer import finalize_graph
from compiler.config import ADN_ROOT, COMPILER_ROOT
from compiler.frontend.printer import Printer
from compiler.tree.visitor import *


def preprocess(sql_file: str) -> Tuple[str, str]:
    with open(os.path.join(ADN_ROOT, f"elements/{sql_file}"), "r") as file:
        sql_file_content = file.read()
    print(sql_file, ":")
    print(sql_file_content)
    # Remove comments from the SQL file
    sql_file_content = re.sub(
        r"/\*.*?\*/", "", sql_file_content, flags=re.DOTALL
    )  # Remove /* ... */ comments

    sql_statements = sql_file_content.split("--processing--")
    # Split Init and Process statements
    assert len(sql_statements) == 2

    sql_statements = [
        re.sub(r"--.*", "", i) for i in sql_statements
    ]  # Remove -- comments and split statements
    # Remove empty statements and leading/trailing whitespace

    return sql_statements[0], sql_statements[1]


def compile_single(engine: str, compiler: ADNCompiler, mrpc_dir: str, verbose: bool):
    os.system("rm -rf ./generated/")
    os.system("mkdir -p ./generated")

    init, process = preprocess(f"{engine}.sql")

    init, process = compiler.transform(init), compiler.transform(process)

    printer = Printer()
    printer.visitRoot(ast_init)
    printer.visitRoot(ast_process)
    print("Compiling...")
    ctx = init_ctx()

    init = compiler.gen(init, ctx)
    process = compiler.gen(process, ctx)

    print("Generating intermediate code...")
    with open(os.path.join(COMPILER_ROOT, f"generated/{engine_name}.rs"), "w") as f:
        f.write("// def code\n")
        f.write("\n".join(ctx.def_code))
        f.write("// init code\n")
        f.write("\n".join(ctx.init_code))
        f.write("// process code\n")
        f.write("\n".join(ctx.process_code))

    compiler.finalize(engine, ctx, mrpc_dir)


if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e", "--engine", type=str, help="(Engine_name ',') *", required=True
    )
    parser.add_argument("--verbose", help="Print Debug info", action="store_true")
    parser.add_argument(
        "--mrpc_dir",
        type=str,
        default=f"../../phoenix/experimental/mrpc",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output type: ast, ir, mrpc", default="mrpc"
    )
    args = parser.parse_args()
    mrpc_dir = os.path.abspath(args.mrpc_dir)

    engine_name = [i.strip() for i in args.engine.split("->")]
    print("Engines:", engine_name)
    print("Output:", args.output)
    compiler = ADNCompiler(args.verbose)

    elems: List[Element] = []
    elem_name: List[str] = []
    for engine in engine_name:
        name = f"gen_{engine}_{len(elem_name)}"
        elem_name.append(name)
        elem = Element(name, preprocess(f"{engine}.sql"), HelloProto)
        elems.append(elem)

    edges: List[Tuple[str, str]] = []
    for i in range(len(elem_name) - 1):
        edges.append((elem_name[i], elem_name[(i + 1) % len(elem_name)]))

    graph = Graph(elems, edges)

    printer = Printer()

    for elem in graph:
        if args.output == "ast":
            print(elem.name, ":")
            init, process = elem.sql
            init, process = compiler.transform(init), compiler.transform(process)
            printer.visitRoot(init)
            printer.visitRoot(process)
        elif args.output == "ir":
            print(elem.name, ":")
            init, process = elem.sql
            init, process = compiler.transform(init), compiler.transform(process)
            ctx = init_ctx()
            init = compiler.gen(init, ctx)
            process = compiler.gen(process, ctx)
            ctx.explain()
            os.system("mkdir -p ./generated/ir")
            with open(
                os.path.join(COMPILER_ROOT, f"generated/ir/{engine_name}.rs"), "w"
            ) as f:
                f.write("// def code\n")
                f.write("\n".join(ctx.def_code))
                f.write("// init code\n")
                f.write("\n".join(ctx.init_code))
                f.write("// process code\n")
                f.write("\n".join(ctx.process_code))
        else:
            print(elem.name, ":")
            compiler.compile(elem, mrpc_dir)

    # if args.output == "mrpc":
    #     ctx = graph.gen_toml()
    #     finalize_graph(ctx, mrpc_dir)

    print("Done!")
