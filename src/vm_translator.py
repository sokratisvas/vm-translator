segment_mapping = {
    'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT',
    'temp': '5', 'pointer': ['THIS', 'THAT']
}

def handle_branching(arg1, arg2):
    if arg1 == 'label':
        return ['(' + str(arg2) + ')']
    elif arg1 == 'goto':
        return ['@' + str(arg2), '0;JMP']
    elif arg1 == 'if-goto':
        return ['@SP', 'M=M-1', 'A=M', 'D=M', 
                '@' + str(arg2), 'D;JNE']

def push_variable(segment, address):
    if segment in ['local', 'argument', 'this', 'that']:
        return ['@' + str(address), 'D=A', '@' + segment_mapping[segment],
                'D=D+M', '@addr', 'M=D', 'A=M', 'D=M', '@SP', 'A=M', 
                'M=D', '@SP', 'M=M+1']
    elif segment == 'temp':
        return ['@' + str(address), 'D=A', '@5', 'D=D+A', 
                'A=D', 'D=M', '@SP', 'A=M', 'M=D', '@SP',
                'M=M+1']
    elif segment == 'constant':
        return ['@' + str(address), 'D=A', '@SP',
                'A=M', 'M=D', '@SP', 'M=M+1']
    elif segment == 'static':
        return ['@STC.' + str(address), 'D=M', '@SP', 'A=M',
                'M=D', '@SP', 'M=M+1']
    elif segment == 'pointer':
        return ['@' + segment_mapping[segment][int(address)], 'D=M', 
                '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']

def pop_variable(segment, address):
    if segment in ['local', 'argument', 'this', 'that']:
        return ['@' + str(address), 'D=A', '@' + segment_mapping[segment],
                'D=D+M', '@addr', 'M=D', '@SP', 'M=M-1', 
                'A=M',  'D=M', '@addr', 'A=M', 'M=D']
    elif segment == 'temp':
        return ['@' + str(address), 'D=A', '@5', 'D=D+A', 
                '@addr', 'M=D', '@SP', 'M=M-1', 'A=M', 'D=M',
                '@addr', 'A=M', 'M=D']
    elif segment == 'static':
        return ['@SP', 'M=M-1', 'A=M', 'D=M', 
                '@STC.' + str(address), 'M=D']
    elif segment == 'pointer':
        return ['@SP', 'M=M-1', 'A=M', 'D=M', 
                '@' + segment_mapping[segment][int(address)], 'M=D']

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
    for i in range(len(tokens)):
        try:
            comment_index = tokens[i].index('//')
        except ValueError as e:
            comment_index = None
        tokens[i] = tokens[i][:comment_index]
        assert len(tokens[i]) <= 3

    filepath = '../examples/' + filename[:-3] + '.asm'
    with open(filepath, mode = 'w', encoding = "utf-8") as f:
        for token in tokens:
            print(token)
            if len(token) == 3:
                if token[0] == 'push':
                    assembly = push_variable(token[1], token[2])
                elif token[0] == 'pop':
                    assembly = pop_variable(token[1], token[2])
            elif len(token) == 1:
                if token[0] in boolean_counter:
                    boolean_counter[token[0]] += 1
                    assembly = arithmetic_command(token[0], boolean_counter[token[0]])
                else:
                    assembly = arithmetic_command(token[0], 0)
            elif len(token) == 2:
                assembly = handle_branching(token[0], token[1])
            for line in assembly:
                f.write(line + '\n')
        f.write('(END)\n@END\n0;JMP\n')


#def write_assembly(tokens):
#    for token in tokens:
#        assert (len(token) == 1 or len(token) == 3)

tokenize('FibonacciSeries.vm')
