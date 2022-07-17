segments = {
    'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT',
    'static': '16', 'temp': '5', 'pointer': ['THIS', 'THAT']
}

def arithmetic_command(token):
    match token:
        case 'add':
            assembly = ['@SP', 'M=M-1', 'A=M', 
                        'D=M', 'A=A-1', 'M=M+D']
        case 'sub':
            assembly = ['@SP', 'M=M-1', 'A=M', 
                        'D=M', 'A=A-1', 'M=M-D']
        case 'neg':
            assembly = ['@SP', ]



#def memory_command(token)

def tokenize(filename):
    filepath = '../examples/' + filename
    with open(filepath, mode = 'r', encoding = 'utf-8') as f:
        instructions = [line.strip() for line in f 
                        if line.strip()[:2] != '//' and line.strip()]

    tokens = [instruction.split() for instruction in instructions]

    for token in tokens:
        print(token)

#def write_assembly(tokens):
#    for token in tokens:
#        assert (len(token) == 1 or len(token) == 3)
            



tokenize('PointerTest.vm')
