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

            # 
            case False:
                pass

            # 
            case False:
                pass
            
            case _:
                return None


