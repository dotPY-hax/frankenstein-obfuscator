def is_block_start(line):
    return line.strip().startswith("<#")

def is_block_end(line):
    return line.strip().endswith("#>")

def is_single_line_comment(line):
    return line.strip().startswith("#")

def might_be_inline_comment(line):
    """This breaks if there is # inside a string too bad..."""
    return "#" in line

def cut_inline_comment(line):
    """This breaks if there is # inside a string too bad..."""
    return line.split("#", 1)[0]


def remove_comments(script):
    new_script = []
    in_block = False

    for line in script.split("\n"):
        if is_block_start(line):
            in_block = True
            continue
        elif is_block_end(line):
            in_block = False
            continue
        elif in_block:
            continue
        elif is_single_line_comment(line):
            continue
        elif might_be_inline_comment(line):
            line = cut_inline_comment(line)
        new_script.append(line)
    return "\n".join(new_script)
