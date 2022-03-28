import ast

class Matcher(ast.NodeVisitor):

    def match_operation(self, node):

        match node:

            #######################
            # Collection Literals #
            #######################

            # {1, 2, 3, 4}
            case :

                return "collection_func", "set_literal"

            # [1, 2, 3, 4]
            case :

                return "collection_func", "list_literal"

            # s = {key1: val1, key2: val2}
            case :

                return "collection_func", "dict_literal"

            # s = {1, 2, 3, 4}
            case :

                return "collection_func", "set_create"

            # s = [1, 2, 3, 4]
            case :

                return "collection_func", "list_create"

            # s = {key1: val1, key2: val2}
            case :

                return "collection_func", "dict_create"

            ####################
            # collection _func #
            ####################

            # result = lst.count(elem)
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

            # lst.count(elem)
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

            # 
            case:

            # 
            case:

            # 
            case:

            # 
            case:

            # 
            case:

            # 
            case:

            # 
            case:

            # 
            case:
            
            case _:
                return None


