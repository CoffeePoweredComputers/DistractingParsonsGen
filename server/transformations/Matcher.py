import ast

class Matcher(ast.NodeVisitor):

    def match_operation(self, node):

        match node:

            #######################
            # Collection Literals #
            #######################

            # {1, 2, 3, 4}
            case False:

                return "collection_func", "set_literal"

            # [1, 2, 3, 4]
            case False:

                return "collection_func", "list_literal"

            # s = {key1: val1, key2: val2}
            case False:

                return "collection_func", "dict_literal"

            # s = {1, 2, 3, 4}
            case False:

                return "collection_func", "set_create"

            # s = [1, 2, 3, 4]
            case False:

                return "collection_func", "list_create"

            # s = {key1: val1, key2: val2}
            case False:

                return "collection_func", "dict_create"

            ####################
            # collection _func #
            ####################

            # result = sequence.count(elem)
            case ast.Assign(
                    targets=[
                        ast.Name()],
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(),
                            attr='count',
                            ctx=ast.Load()),
                        args=[_])):

                return "collection_func", "count"

            # sequence.count(elem)
            case ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(),
                            attr='count'),
                        args=[_])):

                return "collection_func", "count"

            # lst.append(elem)
            case ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(),
                            attr='append',
                            ctx=ast.Load()),
                        args=[_])):

                return "collection_func", "append"

            # lst.extend(other_seq)
            case ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(),
                            attr='extend',
                            ctx=ast.Load()),
                        args=[_])):

                return "collection_func", "extend"

            # collection.pop(x)
            case ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(),
                        attr='pop',
                        ctx=ast.Load()),
                    args=[_])):
                return "collection_func", "pop"

            # res = collection.pop(x)
            case ast.Assign(
                targets=[ast.Name()],
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(),
                        attr='pop',
                        ctx=ast.Load()),
                    args=[_])):
                return "collection_func", "pop"

            # collection.remove(x)
            case ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(),
                        attr='remove',
                        ctx=ast.Load()),
                    args=[_])):
                return "collection_func", "remove"

            # i = collection.index(elem)
            case ast.Assign(
                targets=[
                    ast.Name()],
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(),
                        attr='index',
                        ctx=ast.Load()),
                    args=[_])):
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAaa")
                return "collection_func", "index"

            # collection.index(elem)
            case ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(),
                        attr='index',
                        ctx=ast.Load()),
                    args=[_])):
                return "collection_func", "index"

            # lst.insert(i, elem)
            case ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(),
                        attr='insert',
                        ctx=ast.Load()),
                    args=[_, _])):
                return "collection_func", "insert"

            # c1.update(c2)
            case ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(),
                        attr='update',
                        ctx=ast.Load()),
                    args=[_])):
                return "collection_func", "update"

            # del collection[x] or del collection[ast.Constant()]
            # TODO: Add more granular strucural comparison to help
            #       prevent improper code from being matched.
            case ast.Delete(
                targets=[
                    ast.Subscript(
                        value=ast.Name(),
                        slice=ast.Name() | ast.Constant(),
                        ctx=ast.Del())]):
                return "collection_func", "delete"

            # d[??] = ??
            case ast.Assign(
                targets=[
                    ast.Subscript(
                        value=ast.Name(),
                        slice=ast.Constant() | ast.Name(),
                        ctx=ast.Store())],
                value=ast.Constant() | ast.Name()):
                return "collection_func", "addchangepair"

            # ########### #
            #  For Loops  # 
            # ########### #

            # for i, item in enumerate(collection): pass
            case ast.For(
                    target=ast.Tuple(
                        elts=[
                            ast.Name(),
                            ast.Name()],
                        ctx=ast.Store()),
                    iter=ast.Call(
                        func=ast.Name(id='enumerate', ctx=ast.Load()),
                        args=[ast.Name() | ast.Constant()],
                        keywords=[]),
                    body=[
                        ast.Pass()]):

                return "forloop", "enumerate"

            # for num in range(end): pass
            case ast.For(
                    target=ast.Name(),
                    iter=ast.Call(
                        func=ast.Name(id='range', ctx=ast.Load()),
                        args=[ast.Name() | ast.Constant() | ast.Call()],
                        keywords=[]),
                    body=[ast.Pass()]):

                return "forloop", "range"

            # for num in range(start, end): pass
            case ast.For(
                    target=ast.Name(),
                    iter=ast.Call(
                        func=ast.Name(),
                        args=[
                            ast.Name() | ast.Constant() | ast.Call(),
                            ast.Name() | ast.Constant() | ast.Call()],
                        keywords=[]),
                    body=[
                        ast.Pass()]):

                return "forloop", "range"

            # for num in range(start, end, stride): pass
            case ast.For(
                    target=ast.Name(),
                    iter=ast.Call(
                        func=ast.Name(id='range', ctx=ast.Load()),
                        args=[
                            ast.Name() | ast.Constant() | ast.Call(),
                            ast.Name() | ast.Constant() | ast.Call(),
                            ast.Name() | ast.Constant() | ast.Call()],
                        keywords=[]),
                    body=[ast.Pass()]):
                return "forloop", "range"

            case ast.FunctionDef(
                    name=_,
                    args=_,
                    body=[ast.Pass()]):
                print("FUNCTION DEF FOUND")
                return "func_def", "def"

            case _:
                return None


