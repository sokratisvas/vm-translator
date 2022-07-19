segments = {
    'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT',
    'static': '16', 'temp': '5', 'pointer': ['THIS', 'THAT']
}

def push_constant(constant):
    return ['@' + str(constant), 'D=A', '@SP',
                    'A=M', 'M=D', '@SP', 'M=M+1']

def arithmetic_command(token, cnt):
    if token == 'add':
        return ['@SP', 'M=M-1', 'A=M', 
                'D=M', 'A=A-1', 'M=M+D']
    elif token == 'sub':
        return ['@SP', 'M=M-1', 'A=M', 
                'D=M', 'A=A-1', 'M=M-D']
    elif token == 'neg':
        return ['@SP', 'A=M-1', 'M=-M']
    elif token == 'eq':
        return ['@SP', 'M=M-1', 'A=M', 'D=M', 
                'A=A-1', 'D=M-D', '@ISEQUAL' + str(cnt), 'D;JEQ',
                '@NOTEQUAL' + str(cnt), 'D;JNE', '(ISEQUAL' + str(cnt) + ')',
                '@SP', 'A=M-1', 'M=-1', '@EQEND' + str(cnt), '0;JMP',
                '(NOTEQUAL' + str(cnt) + ')', '@SP', 'A=M-1', 'M=0', 
                '@EQEND' + str(cnt), '0;JMP', '(EQEND' + str(cnt) + ')']
    elif token == 'not':
        return ['@SP', 'A=M-1', 'M=!M']
    elif token == 'and':
        return ['@SP', 'M=M-1', 'A=M', 'D=M', 
                'A=A-1', 'M=M&D']
    elif token == 'or':
        return ['@SP', 'M=M-1', 'A=M', 'D=M', 
                'A=A-1', 'M=M|D']
    elif token == 'gt':
        return ['@SP', 'M=M-1', 'A=M', 'D=M', 
                 'A=A-1', 'D=M-D', '@ISGREATER_GT' + str(cnt), 'D;JGT',
                 '@ISLESS_GT' + str(cnt), 'D;JLE', '(ISGREATER_GT' + str(cnt) + ')', 
                 '@SP', 'A=M-1', 'M=-1', '@GTEND' + str(cnt), '0;JMP',
                 '(ISLESS_GT' + str(cnt) + ')', '@SP', 'A=M-1', 'M=0', 
                 '@GTEND' + str(cnt), '0;JMP', '(GTEND' + str(cnt) + ')']
    else:
        return  ['@SP', 'M=M-1', 'A=M', 'D=M', 
                 'A=A-1', 'D=M-D', '@ISGREATER_LT' + str(cnt), 'D;JGE',
                 '@ISLESS_LT' + str(cnt), 'D;JLT', '(ISGREATER_LT' + str(cnt) + ')',
                 '@SP', 'A=M-1', 'M=0', '@LTEND' + str(cnt), '0;JMP', 
                 '(ISLESS_LT' + str(cnt) + ')', '@SP', 'A=M-1', 'M=-1', 
                 '@LTEND' + str(cnt), '0;JMP', '(LTEND' + str(cnt) + ')']

def tokenize(filename):
    boolean_counter = {'eq': 0, 'gt': 0, 'lt': 0}
    filepath = '../examples/' + filename
    with open(filepath, mode = 'r', encoding = 'utf-8') as f:
        instructions = [line.strip() for line in f 
                        if line.strip()[:2] != '//' and line.strip()]

    tokens = [instruction.split() for instruction in instructions]

    filepath = '../examples/' + filename[:-3] + '.asm'
    with open(filepath, mode = 'w', encoding = "utf-8") as f:
        for token in tokens:
            if len(token) == 3:
                assembly = push_constant(token[2])
            elif len(token) == 1:
                if token[0] in boolean_counter:
                    boolean_counter[token[0]] += 1
                    assembly = arithmetic_command(token[0], boolean_counter[token[0]])
                else:
                    assembly = arithmetic_command(token[0], 0) 
            for line in assembly:
                f.write(line + '\n')


#def write_assembly(tokens):
#    for token in tokens:
#        assert (len(token) == 1 or len(token) == 3)

tokenize('SimpleAdd.vm')
