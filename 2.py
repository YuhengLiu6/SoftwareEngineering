import ast

undefined_vars = set() 
defined_vars = set() 
undefined_count = 0 
func_calls = dict()

undefined_vars2 = set() 
defined_vars2 = set() 
undefined_count2 = 0 
func_calls2 = dict()

class FirstScan(ast.NodeVisitor):
    def __init__(self):
        self.defined_vars = set()
        self.undefined_var_uses = 0
        self.function_calls = set()

    def visit_Name(self, node):
        # Check if the node is a variable being loaded and is not in the set of defined variables
        global undefined_count, undefined_vars, defined_vars
        if isinstance(node.ctx, ast.Load) and node.id not in defined_vars:
            undefined_vars.add(node.id) 


        #退出机制
        #不互通，不同层级

    def visit_Assign(self, node):
        # Add assigned variables to the set of defined variables
        global undefined_count, undefined_vars, defined_vars

        if isinstance(node.value, ast.BinOp):#等式右边为二/三元的操作
            if isinstance(node.value.left, ast.BinOp):#三元
                left_operand = node.value.left.left
                mid_operand = node.value.left.right
                right_operand = node.value.right
                #----------------------------------------------------
                left_operand_name = None
                if isinstance(left_operand, ast.Name):
                    left_operand_name = left_operand.id
                    if left_operand_name not in defined_vars:
                        undefined_vars.add(left_operand_name)
                        #-------------------
                        
                elif isinstance(left_operand, ast.Constant):
                    left_operand_name = left_operand.value

                mid_operand_name = None
                if isinstance(mid_operand, ast.Name):
                    mid_operand_name = mid_operand.id
                    if mid_operand_name not in defined_vars:
                        undefined_vars.add(mid_operand_name)
                        #-------------------
                       
                elif isinstance(mid_operand, ast.Constant):
                    mid_operand_name = mid_operand.value

                right_operand_name = None
                if isinstance(right_operand, ast.Name):
                    right_operand_name = right_operand.id
                    if right_operand_name not in defined_vars:
                        undefined_vars.add(right_operand_name)
                        #-------------------
                      
                elif isinstance(right_operand, ast.Constant):
                    right_operand_name = right_operand.value
                #----------------------------------------------------

                if left_operand_name not in defined_vars or right_operand_name not in defined_vars or mid_operand_name not in defined_vars:
                    undefined_vars.add(node.targets[0].id)
                    if node.targets[0].id in defined_vars:
                        defined_vars.discard(node.targets[0].id)
                else:
                    defined_vars.add(node.targets[0].id)
                    if node.targets[0].id in undefined_vars:
                        undefined_vars.discard(node.targets[0].id)
            elif isinstance(node.value.right, ast.BinOp):#第二种三元
                left_operand = node.value.left
                mid_operand = node.value.right.left
                right_operand = node.value.right.right
                #----------------------------------------------------
                left_operand_name = None
                if isinstance(left_operand, ast.Name):
                    left_operand_name = left_operand.id
                    if left_operand_name not in defined_vars:
                        undefined_vars.add(left_operand_name)
                        #-------------------
                       
                elif isinstance(left_operand, ast.Constant):
                    left_operand_name = left_operand.value

                mid_operand_name = None
                if isinstance(mid_operand, ast.Name):
                    mid_operand_name = mid_operand.id
                    if mid_operand_name not in defined_vars:
                        undefined_vars.add(mid_operand_name)
                        #-------------------
                       
                elif isinstance(mid_operand, ast.Constant):
                    mid_operand_name = mid_operand.value

                right_operand_name = None
                if isinstance(right_operand, ast.Name):
                    right_operand_name = right_operand.id
                    if right_operand_name not in defined_vars:
                        undefined_vars.add(right_operand_name)
                        #-------------------
                       
                elif isinstance(right_operand, ast.Constant):
                    right_operand_name = right_operand.value
                #----------------------------------------------------

                if left_operand_name not in defined_vars or right_operand_name not in defined_vars or mid_operand_name not in defined_vars:
                    undefined_vars.add(node.targets[0].id)
                    if node.targets[0].id in defined_vars:
                        defined_vars.discard(node.targets[0].id)
                else:
                    defined_vars.add(node.targets[0].id)
                    if node.targets[0].id in undefined_vars:
                        undefined_vars.discard(node.targets[0].id)
            else:#二元
                left_operand = node.value.left
                right_operand = node.value.right

                left_operand_name = None
                if isinstance(left_operand, ast.Name): #二元的左边为变量
                    left_operand_name = left_operand.id
                    #若为变量且不再defined——var中，则加入undefined
                    if left_operand_name not in defined_vars:
                        undefined_vars.add(left_operand_name)
                        #-------------
                    

                elif isinstance(left_operand, ast.Constant):#二元的左边为常熟
                    left_operand_name = left_operand.value

                right_operand_name = None
                if isinstance(right_operand, ast.Name):#二元的右边为变量
                    right_operand_name = right_operand.id
                    if right_operand_name not in defined_vars:
                        undefined_vars.add(right_operand_name)
                        #-------------
                  


                elif isinstance(right_operand, ast.Constant):#二元的右边为常熟
                    right_operand_name = right_operand.value

                #这里可能要考虑参数+常熟的情况
                if left_operand_name not in defined_vars and right_operand_name in defined_vars :
                    if isinstance(left_operand, ast.Num) :
                        defined_vars.add(node.targets[0].id)
                        if node.targets[0].id in undefined_vars:
                            undefined_vars.discard(node.targets[0].id)
                    else:
                        undefined_vars.add(node.targets[0].id)
                        
                        if node.targets[0].id in defined_vars:
                            defined_vars.discard(node.targets[0].id)
                elif right_operand_name not in defined_vars and left_operand_name in defined_vars:
                    if isinstance(right_operand, ast.Num) and left_operand_name in defined_vars:
                        defined_vars.add(node.targets[0].id)
                        if node.targets[0].id in undefined_vars:
                            undefined_vars.discard(node.targets[0].id)
                    else:
                        undefined_vars.add(node.targets[0].id)
                        
                        if node.targets[0].id in defined_vars:
                            defined_vars.discard(node.targets[0].id)
                elif right_operand_name not in defined_vars and left_operand_name not in defined_vars:
                    undefined_vars.add(node.targets[0].id)
                    if node.targets[0].id in defined_vars:
                        defined_vars.discard(node.targets[0].id)

        elif isinstance(node.value, ast.Constant):#等式右边为常数
            defined_vars.add(node.targets[0].id)
            if node.targets[0].id in undefined_vars:
                        undefined_vars.discard(node.targets[0].id)
        
        elif isinstance(node.value, ast.Name):#等式右边为单个变量
            if node.value.id in undefined_vars:
                undefined_vars.add(node.targets[0].id)
                #-------------------
              
                if(node.targets[0].id in defined_vars):
                    defined_vars.discard(node.targets[0].id)
            else:
                defined_vars.add(node.targets[0].id)
                if node.targets[0].id in undefined_vars:
                    undefined_vars.discard(node.targets[0].id)


    def visit_FunctionDef(self, node):
        pass

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            arg_indices = [i for i, arg in enumerate(node.args) if isinstance(arg, ast.Name) and arg.id not in defined_vars]
            func_calls[func_name] = []
            if not arg_indices:
                func_calls[func_name].append([])
            else:
                func_calls[func_name].append(arg_indices)
        # self.generic_visit(node)








#第二次扫描 

class SecondScan(ast.NodeVisitor):
    def __init__(self):
        self.defined_vars2 = set()
        self.undefined_var_uses2 = 0
        self.function_calls2 = set()

    def visit_Name(self, node):
        global undefined_count2, undefined_vars2, defined_vars2
        if isinstance(node.ctx, ast.Load) and node.id not in defined_vars2:
            undefined_vars2.add(node.id) 
            undefined_count2 += 1 

    def visit_Assign(self, node):
        # Add assigned variables to the set of defined variables
        global undefined_count2, undefined_vars2, defined_vars2

        if isinstance(node.value, ast.BinOp):#等式右边为二/三元的操作
            if isinstance(node.value.left, ast.BinOp):#三元
                left_operand = node.value.left.left
                mid_operand = node.value.left.right
                right_operand = node.value.right
                #----------------------------------------------------
                left_operand_name = None
                if isinstance(left_operand, ast.Name):
                    left_operand_name = left_operand.id
                    if left_operand_name not in defined_vars2:
                        undefined_vars2.add(left_operand_name)
                        #-------------------
                        undefined_count2 +=1
                elif isinstance(left_operand, ast.Constant):
                    left_operand_name = left_operand.value

                mid_operand_name = None
                if isinstance(mid_operand, ast.Name):
                    mid_operand_name = mid_operand.id
                    if mid_operand_name not in defined_vars2:
                        undefined_vars2.add(mid_operand_name)
                        #-------------------
                        undefined_count2 +=1
                elif isinstance(mid_operand, ast.Constant):
                    mid_operand_name = mid_operand.value

                right_operand_name = None
                if isinstance(right_operand, ast.Name):
                    right_operand_name = right_operand.id
                    if right_operand_name not in defined_vars2:
                        undefined_vars2.add(right_operand_name)
                        #-------------------
                        undefined_count2 +=1
                elif isinstance(right_operand, ast.Constant):
                    right_operand_name = right_operand.value
                #----------------------------------------------------

                if left_operand_name not in defined_vars2 or right_operand_name not in defined_vars2 or mid_operand_name not in defined_vars2:
                    undefined_vars2.add(node.targets[0].id)
                    if node.targets[0].id in defined_vars2:
                        defined_vars2.discard(node.targets[0].id)
                else:
                    defined_vars2.add(node.targets[0].id)
                    if node.targets[0].id in undefined_vars2:
                        undefined_vars2.discard(node.targets[0].id)
            else:#二元
                left_operand = node.value.left
                right_operand = node.value.right

                left_operand_name = None
                if isinstance(left_operand, ast.Name): #二元的左边为变量
                    left_operand_name = left_operand.id
                    #若为变量且不再defined——var中，则加入undefined
                    if left_operand_name not in defined_vars2:
                        undefined_vars2.add(left_operand_name)
                        #-------------
                        undefined_count2 +=1

                elif isinstance(left_operand, ast.Constant):#二元的左边为常熟
                    left_operand_name = left_operand.value

                right_operand_name = None
                if isinstance(right_operand, ast.Name):#二元的右边为变量
                    right_operand_name = right_operand.id
                    if right_operand_name not in defined_vars2:
                        undefined_vars2.add(right_operand_name)
                        #-------------
                        undefined_count2 +=1


                elif isinstance(right_operand, ast.Constant):#二元的右边为常熟
                    right_operand_name = right_operand.value

                #这里可能要考虑参数+常熟的情况
                if left_operand_name not in defined_vars2 and right_operand_name in defined_vars2 :
                    if isinstance(left_operand, ast.Num) :
                        defined_vars2.add(node.targets[0].id)
                        if node.targets[0].id in undefined_vars2:
                            undefined_vars2.discard(node.targets[0].id)
                    else:
                        undefined_vars2.add(node.targets[0].id)
                        
                        if node.targets[0].id in defined_vars2:
                            defined_vars2.discard(node.targets[0].id)
                elif right_operand_name not in defined_vars2 and left_operand_name in defined_vars2:
                    if isinstance(right_operand, ast.Num) and left_operand_name in defined_vars2:
                        defined_vars2.add(node.targets[0].id)
                        if node.targets[0].id in undefined_vars2:
                            undefined_vars2.discard(node.targets[0].id)
                    else:
                        undefined_vars2.add(node.targets[0].id)
                        
                        if node.targets[0].id in defined_vars2:
                            defined_vars2.discard(node.targets[0].id)
                elif right_operand_name not in defined_vars2 and left_operand_name not in defined_vars2:
                    undefined_vars2.add(node.targets[0].id)
                    if node.targets[0].id in defined_vars2:
                        defined_vars2.discard(node.targets[0].id)

        elif isinstance(node.value, ast.Constant):#等式右边为常数
            defined_vars2.add(node.targets[0].id)
            if node.targets[0].id in undefined_vars2:
                        undefined_vars2.discard(node.targets[0].id)
        
        elif isinstance(node.value, ast.Name):#等式右边为单个变量
            if node.value.id in undefined_vars2:
                undefined_vars2.add(node.targets[0].id)
                #-------------------
                undefined_count +=1
                if(node.targets[0].id in defined_vars2):
                    defined_vars2.discard(node.targets[0].id)
            else:
                defined_vars2.add(node.targets[0].id)
                if node.targets[0].id in undefined_vars2:
                    undefined_vars2.discard(node.targets[0].id)

    def visit_FunctionDef(self, node):
        global func_calls
        func_name = node.name
        # func_pos = func_calls[func_name]
        if func_name in func_calls:#只有在字典中找到了这个函数名字，才会进行下面的操作；否则就是没有调用
            func_pos = func_calls[func_name]#找到字典中对应函数名字的值,是list
            #获取当前函数的所有参数情况------------------------------------
            parameter_names = []
            # Positional arguments
            for arg in node.args.args:
                parameter_names.append(arg.arg)
            # Variable positional argument
            if node.args.vararg:
                parameter_names.append(node.args.vararg.arg)
            # Keyword-only arguments
            for arg in node.args.kwonlyargs:
                parameter_names.append(arg.arg)
            # Variable keyword argument
            if node.args.kwarg:
                parameter_names.append(node.args.kwarg.arg)
            
            
            #遍历直到这个func_calls为空----------------------------------
            while func_pos:
                # print("func_calls before pop", func_calls)
                arg_pos = func_pos.pop(0)
                #在每一次循环内，设置局部的定义和未定义变量
                local_defined_vars = set()
                local_undefined_vars = set()
                #根据位置信息，设置对应的defined和undefined
                for i in range(len(arg_pos)):
                    local_undefined_vars.add(parameter_names[arg_pos[i]])
                    local_defined_vars = [parameter_names[i] for i in range(len(parameter_names)) if i not in arg_pos]

                self.generic_visit(node)
                #遍历完后，将局部的defined和undefined加入全局????????是否需要，因为assign中已经对全局做了修改
                
            #此时func_calls为空，这个函数的所有调用遍历完毕
            
        else:
            pass

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            arg_indices = [i for i, arg in enumerate(node.args) if isinstance(arg, ast.Name) and arg.id not in defined_vars]
            func_calls[func_name] = []
            if not arg_indices:
                func_calls[func_name].append([])
            else:
                func_calls[func_name].append(arg_indices)

        

if __name__ == '__main__':
    code = input()
    code = "\n".join(code.split("\\n"))

    tree = ast.parse(code) 

    undefined_vars = set() 
    defined_vars = set() 
    undefined_count = 0 
    func_calls = dict()

    undefined_vars2 = set() 
    defined_vars2 = set() 
    undefined_count2 = 0 
    func_calls2 = dict()

    visitor1 = FirstScan() 
    visitor1.visit(tree) 
    visitor2 = SecondScan() 
    visitor2.visit(tree) 
    print(undefined_count2)
