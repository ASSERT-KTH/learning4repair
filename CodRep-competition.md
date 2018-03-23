# The CodRep Competition

This competition is about predicting source code changes.

As input, you are given a pair (Java file, Java line) and as output you give a line number corresponding to the line to be replaced by in the file.
 
Example of one-liner replacement

```
-		return true;
+		return false;
```

## Submission format

To play in the competition, you have to submit a program which takes as in put a folder name, and outputs on the console, the predicted line numbers. Several line numbers can be predicted if the tool is not 100% sure of the prediction. The loss function of the competition in takes this into account.

```
<FileName> <line numer>
<FileName1> <line numer> <line numer>
<FileName2> <line numer>
```

Eg;
```
1.txt 42
2.txt 78 526
...


## Folder structure and input format

The provided data is `Files/Replaced/*.txt`. The txt files are in a format that has been designed to be usuper easy to parse.
Each file contains:
```
{Code line to insert} \newline
{The program}
```

In the example below of data file `foo.txt`, `double b = 0.1` is the code line to be added somewhere in the file in place of another line.
```
double b = 0.1

public class test{
  int a = 1
  int b = 0.1
}
```

if your program output `foo.txt 3`, it means replace line 3 (`int b = 0.1`) with the new code line `double b = 0.1`.

For each data file , the correct answer is given in folder `Solutions/`,  e.g. the correct answer to `Files/Added/1.txt` is in `Solutions/Added/1.txt`

## Loss function

TODO

## Base line systems

We provide 4 stupid systems for illustrating our to parse the data, and having a baseline performance.

TODO: explain them and give performance


