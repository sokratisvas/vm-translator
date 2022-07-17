segments = {
    'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT',
    'static': '16', 'temp': '5', 'pointer': ['THIS', 'THAT']
}

def tokenize(filename):
    filepath = '../examples/' + filename
    with open(filepath, mode = 'r', encoding = 'utf-8') as f:
        instructions = [line.strip() for line in f if line.strip()[:2] != '//' and line.strip()]

    tokens = [instruction.split() for instruction in instructions]

    for token in tokens:
        print(token)

def write_assembly(tokens):
    stack = []



tokenize('PointerTest.vm')
