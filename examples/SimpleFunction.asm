// function declaration
(SimpleFunction.test)
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1

@0
D=A
@LCL
D=D+M
@addr
M=D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@LCL
D=D+M
@addr
M=D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D
@SP
A=M-1
M=!M
@0
D=A
@ARG
D=D+M
@addr
M=D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D
@1
D=A
@ARG
D=D+M
@addr
M=D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D
// endframe = LCL
@LCL
D=M
@endframe
M=D
// retaddr = *(endframe - 5)
@endframe
D=M
@5
D=D-A
A=D
D=M
@retaddr
M=D
// *ARG = pop()
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
// SP = ARG + 1
@ARG
D=M
D=D+1
@SP
M=D
// THAT = *(endframe - 1)
@endframe
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
// THIS = *(endframe - 2)
@endframe
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
// ARG = *(endframe - 3)
@endframe
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
// LCL = *(endframe - 4)
@endframe
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
// goto retaddr
@retaddr
A=M
0;JMP
(END)
@END
0;JMP