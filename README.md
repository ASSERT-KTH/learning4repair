# One liner competition

All one liner changes from https://github.com/monperrus/real-bug-fixes-icse-2015/ .
Can be used as benchmark for predicting added/removed/replaced one-liner change.

## Example of one-liner change

### Added one-liner

```
+      return true;
```

### Removed one-liner

```
-import java.io.IOException;
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
The output should be a line number where the inserted code should be place AFTER. Line numbers starts from 1.

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

Then your program should output: 1
