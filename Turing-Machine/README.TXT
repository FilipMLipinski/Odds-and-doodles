Type in rules to a file in the following format.
The first line is the set of states.
The first, second, and third states are the start, accept, 
and reject states respectively.
If machine won't know what to do it will reject.
Assume the tape has a start symbol S. The input will be written 
directly after S.
Blanks are denoted with '_'.
The alphabet on the tape is the set of all ascii characters, but 
of course you don't have to use all of them.
Name your states concisely (1-2 chars best).
You will be asked for the input string.

START OF FILE
Q1,AC,RE,...Qn
Q1,S:Q1,S,R
Q1,A:Q2,B,R
...
END OF FILE