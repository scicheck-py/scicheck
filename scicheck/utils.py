import inspect

#####
# Error Messages
#####


def caller(k: int) -> str:
    "Gets the name of the calling function at the kth index in the stack"
    return inspect.stack()[k].function


def context(input: str, stack: int = 1) -> str:
    "Returns an informative name for an input that failed a debugging check"

    if function is None:
        function = caller(stack)
    return f"In the call to scicheck.{function}, the {input} input"


def strlist(strings: list[str]) -> str:
    "Returns a nicely formatted string list"

    if len(strings) == 1:
        return strings[0]
    elif len(strings) == 2:
        return f"{strings[0]} or {strings[1]}"
    else:
        head = ", ".join(strings[:-1])
        return ", or ".join([head, strings[-1]])
