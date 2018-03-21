# The CodIns Competition

All one liner changes from https://github.com/monperrus/real-bug-fixes-icse-2015/ .
Can be used as benchmark for predicting added/removed/replaced one-liner change.

## Example of one-liner change

### Added one-liner

```
+      return true;
```

### Replaced one-liner

```
-		return true;
+		return false;
```

## File structure in the competition

### Added one-liner

All data in Files/Added/. Each file contains:
```
{Code to be inserted}
\newline
{The program}
```
The output should be a line number where the inserted code should be place AFTER. Line numbers starts from 1, if you want to insert it before the first line, your program should output 0.

Example:
```
System.out.println("one liner competition")

public class test{
}
```

And the correct answer is:
```
public class test{
  System.out.println("one liner competition")
}
```

Then your program should output: 1. (Insert it after line 1)

### Replaced one-liner

All data in Files/Replaced/. Each file contains:
```
{Code to insert}
\newline
{The program}
```
The output should be a line number where the line should be replaced. Line numbers starts from 1.

Example:
```
double b = 0.1

public class test{
  int a = 1
  int b = 0.1
}
```

And the correct answer is:
```
public class test{
  int a = 1
  double b = 0.1
}
```

Then your program should output: 3. (Replace line 3 with the inserted code)

## Competition structure

All the competition data in Files/ and all solutions in Solutions/.

e.g. solution to Files/Added/1.txt is Solutions/Added/1.txt

## Performance of baseline algorithms

|       Type        | Algorithm | Performance |
| ----------------- | --------- | ----------- |
| Replaced one line | maximumError | Total files: 4454 \nCumulative line error: 4453.99989692 (the lower, the better) \n Top 1 accuracy: 0.0 (the higher, the better) |
