import ast

class Matcher(ast.NodeVisitor):

    def match_operation(self, node):

        match node:
            case ast.Assign(
                    targets=[
                        ast.Name()],
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(),
                            attr='count',
                            ctx=ast.Load()),
                        args=[_])):
                return "Matched count assignment"

            case ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(),
                            attr='count'),
                        args=[_])):
                return "Matched count expression"

            case ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(),
                            attr='append',
                            ctx=ast.Load()),
                        args=[_])):
                return "Matched append expresion"

            case ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(),
                            attr='extend',
                            ctx=ast.Load()),
                        args=[_])):
                print("Matched extend expresion")
            
            case _:
                print("no match")



def main():
    v = Visitor()
    lines = [
        "z = x.count([1, 2, 3, {1, 2 ,3} ])",
        "test = x.count(5)",
        "x.count(5)",
        "lst.append(z)",
        "lst.append(y)",
        "lst.extend([1, 2, 3])"
    ]
    for line in lines:
        line = ast.parse(line.strip()).body[0]
        #print(ast.dump(line, indent=4))
        v.match_operation(line)

if __name__ == "__main__":
    main()