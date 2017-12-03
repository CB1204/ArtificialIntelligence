Name: Christian Baumann
Matrikelnummer: 03691706

I used Python 3.6.0 to implement my solution. 

Solution description:
The implemented solution uses A*-search, with a heuristic function that compares the number of
occurrences of each letter between current node and goal node. As the algorithm works quite 
efficiently, it is not necessary to compute the heuristic ahead of solving the actual problem,
but rather use an on-the-fly approach that calculates the heuristic function the first time the 
word is found. 
This is made possible by a "filtering-approach" when reading the data. The data is split into 
bins of word lengths. In a single step, a word length can only change by one, thus eliminating 
all words of other lengths than len(current_word)+1 or len(current_word)-1. With the implemented
structure, this eliminates most of the words from consideration even before computing the heuristic
function.
For backtracking, nodes are classes with a property 'parentID', which links back to their respective
parent. Also, f,g,h, and the word itself are saved in this node class.

Externals:
The os package is used in order to find the current location and thus open files.
the sys package is used to capture inputs from the shell.


