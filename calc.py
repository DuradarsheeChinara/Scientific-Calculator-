import ast
import math
import operator as op

# Stores current angle mode
ANGLE_MODE = "rad"

# Stores previous calculations
HISTORY = []


# Changes angle mode between degrees and radians
def set_angle_mode(mode):
    global ANGLE_MODE

    if mode.lower() in ["deg", "rad"]:
        ANGLE_MODE = mode.lower()
    else:
        raise ValueError("Mode must be deg or rad")


# Converts degrees to radians for trig functions
def wrap_angle(func):

    def wrapped(x):
        if ANGLE_MODE == "deg":
            x = math.radians(x)

        return func(x)

    return wrapped


# Allowed calculator functions
NAMES = {
    "pi": math.pi,
    "e": math.e,

    "sin": wrap_angle(math.sin),
    "cos": wrap_angle(math.cos),
    "tan": wrap_angle(math.tan),

    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "abs": abs,
    "pow": pow,
}


# Allowed operators
OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
}


# Safely evaluates math expressions
def evaluate(node):

    # Expression node
    if isinstance(node, ast.Expression):
        return evaluate(node.body)

    # Numbers
    if isinstance(node, ast.Constant):
        return node.value

    # Binary operations
    if isinstance(node, ast.BinOp):

        left = evaluate(node.left)
        right = evaluate(node.right)

        operator_type = type(node.op)

        if operator_type in OPS:
            return OPS[operator_type](left, right)

    # Unary operations like -5
    if isinstance(node, ast.UnaryOp):

        value = evaluate(node.operand)

        if isinstance(node.op, ast.USub):
            return -value

        if isinstance(node.op, ast.UAdd):
            return +value

    # Function calls
    if isinstance(node, ast.Call):

        if not isinstance(node.func, ast.Name):
            raise TypeError("Invalid function")

        func_name = node.func.id

        if func_name not in NAMES:
            raise NameError("Function not allowed")

        func = NAMES[func_name]

        args = []

        for arg in node.args:
            args.append(evaluate(arg))

        return func(*args)

    # Variables like pi or e
    if isinstance(node, ast.Name):

        if node.id in NAMES:
            return NAMES[node.id]

        raise NameError("Unknown variable")

    raise TypeError("Invalid expression")


# Converts user text into AST and evaluates it
def calculate(expression):

    tree = ast.parse(expression, mode="eval")

    return evaluate(tree)


# Displays help information
def show_help():

    print("\nAvailable functions:")

    for name in NAMES:
        print("-", name)

    print("\nCommands:")
    print(":mode deg")
    print(":mode rad")
    print(":history")
    print(":help")
    print(":exit")


# Runs the calculator loop
def repl():

    print("Scientific Calculator")
    print("Type :help for commands")

    while True:

        user_input = input("calc> ").strip()

        if not user_input:
            continue

        # Commands
        if user_input.startswith(":"):

            parts = user_input[1:].split()

            command = parts[0]

            if command == "exit":
                break

            elif command == "help":
                show_help()

            elif command == "history":

                for item in HISTORY:
                    print(item)

            elif command == "mode":

                if len(parts) > 1:

                    try:
                        set_angle_mode(parts[1])
                        print("Angle mode set to", ANGLE_MODE)

                    except Exception as e:
                        print("Error:", e)

            else:
                print("Unknown command")

            continue

        # Math expressions
        try:

            result = calculate(user_input)

            HISTORY.append(f"{user_input} = {result}")

            print(result)

        except Exception as e:
            print("Error:", e)


# Starts program
if __name__ == "__main__":
    repl()