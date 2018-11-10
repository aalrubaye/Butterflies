# Butterflies

## Libraries Required:
- NetworkX
- matplotlib
- tqdm (a smart progress meter)

## Installations required:
### NetworkX:
```
  pip install networkx
```
For more information please visit https://networkx.github.io/documentation/stable/install.html

### matplotlib:
 ```
    python -m pip install -U pip
    python -m pip install -U matplotlib
``` 
For more information please visit https://matplotlib.org/users/installing.html
    
### tqdm
```
    pip install https://github.com/tqdm/tqdm/#installation
``` 
For more information please visit https://github.com/jeffalstott/powerlaw
    
## Running the code:
To run the code you can do either one:
- via terminal/shell by getting into the directory of the code then 
```
    python butterfly.py
```
watch it here (https://www.youtube.com/watch?v=PdDxDyJ1jAs)


The first 10 test cases and thier correct answer (via BruteForce algorithm) are stored at the file "Test_cases_and_correct_answers.txt"
The first 10 test cases correctness validation are stored at the file "Validating_test_cases_answers.txt" 

Initially the number of steps are limited to 400 so it takes less time to execute, you can change it by updating the variable "number_of_iterations" on line 248 of the file buterfly.py.

The execution time for 400 iterations will be ~1 min and 25 seconds on a machine with 2.3 intel core i7, memory 16 GB). The execution time for 1000 iterations will be ~25 mins.
