import ast

code = input()
code = "\n".join(code.split("\\n"))


tree = ast.parse(code)

for i, node in enumerate(ast.iter_child_nodes(tree)):
    if isinstance(node, ast.stmt):
        node.lineno = i+1

#函数定义列表
func_defs =[]
#全局变量列表
global_vars = []

for node in tree.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                global_vars.append(target.id)

# 遍历语法树，替换操作符
for node in ast.walk(tree):
    if isinstance(node, ast.BinOp):
        if isinstance(node.op, ast.Add):
            node.op = ast.Sub()
        elif isinstance(node.op, ast.Sub):
            node.op = ast.Add()
        elif isinstance(node.op, ast.Mult):
            node.op = ast.Div()
        elif isinstance(node.op, ast.Div):
            node.op = ast.Mult()
    elif isinstance(node, ast.Compare):
        if isinstance(node.ops[0], ast.GtE):
            node.ops[0] = ast.Lt()
        elif isinstance(node.ops[0], ast.LtE):
            node.ops[0] = ast.Gt()
        elif isinstance(node.ops[0], ast.Gt):
            node.ops[0] = ast.LtE()
        elif isinstance(node.ops[0], ast.Lt):
            node.ops[0] = ast.GtE()
    elif isinstance(node, ast.FunctionDef):
        func_defs.append(node)
    elif isinstance(node, ast.Global):
        for name in node.names:
            if not any(isinstance(n, ast.FunctionDef) and n.name == node.name for n in ast.walk(node)):
                global_vars.append(name)

#Delete Unused Function Definitions
for func in func_defs:
    isused = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if node.func.id == func.name:
                isused = True
                break
    if not isused:
        tree.body.remove(func)


# print(global_vars)
#添加打印全局变量的语句
for var in set(global_vars):
    print_stmt = ast.Expr(value=ast.Call(func=ast.Name(id='print', ctx=ast.Load()),
                                        args=[ast.Name(id=var, ctx=ast.Load())],
                                        keywords=[]))
    tree.body.append(print_stmt)


print(ast.unparse(tree))





