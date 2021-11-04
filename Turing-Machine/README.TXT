Type in rules to the RuleFile.txt file in the following format.
The first line is the set of states,
where the first, second, and third states are the start, accept, 
and reject states respectively.
For the next lines, write Q,A:R,B,L for "when reading A in state Q go to state R, write a B and move Left".
Each such rule write on a different line. One rule - one line.
If machine won't know what to do next it will reject.
Assume the tape has a start symbol S. The input will be written 
directly after S.
Blanks are denoted with '_', they will be added as the machine reaches the end of tape.
The alphabet on the tape is the set of all ascii characters, but 
of course you don't have to use all of them.
Name your states concisely (1-2 chars best).
You will be asked for the input string, repeatedly,
so you can experiment with different strings in the same run
of the program. However, rules from the RuleFile are loaded once,
at the beginning of the run.

properly formatted RuleFile:
START OF FILE
Q1,AC,RE,...Qn
Q1,S:Q1,S,R
Q1,A:Q2,B,R
...
END OF FILE
