# shidiscript docs.
shidiscript is a small scripting langauge i made for fun. This will probably never get any practical use outside of my small programming circle

pros
* idk its cool?

cons
* sucks ass
* no practical use
* nobody uses it
* hard to write

## comments
comments are defined with <b>double slashes</b> `//`<br>
double slashes work like a command that never gets run.

`// this is a comment`

### INCORRECT COMMENTS:
```
printexa Hello, World! // prints "Hello, World!"
```
### CORRECT COMMENTS
```
printexa Hello, World!
// prints "Hello, World!"
```

## label and goto
takes one argument<br>
saves argument <b>one</b> to a list along with its position<br>
quickly move to that label with `goto`.

examples:
```
goto this
// moves pointer to line 4
// no code here gets ran.
label this
```

## stop
takes no arguments
stops program immedietely

## clear
clears terminal

## variable
takes in three arguments.

argument <b>one</b> can be of <b>`integer`</b> or <b>`string`</b><br>
argument <b>two</b> is the variable <b>name</b><br>
argument <b>three</b> is the <b>value</b> of the variable.<br>

examples:
```
variable integer gold 0
variable integer thisInt 25

// you can replace the value of variables too!
variable integer gold 25

variable string hi Hello!
variable string hworld Hello, World!
variable string note This string can be of any length.

variable string hworld Goodbye, World.
```
## printexa
prints all characters immedietaly after it<br>
examples:
```
printexa Hello, World!
printexa Goodbye, World.
printexa This can be of any length.
```

## print
takes one argument
argument <b>one</b> is to be a variable name.<br>
prints that variable's name

examples:
```
variable string toprint Hello, World!
print toprint
// will print "Hello, World!"

variable integer gold 25
print gold
// will print "25"
```

## math
takes in <b>five</b> arguments

argument <b>one</b> can be of <b>"add"</b>, <b>"neg"</b>, or <b>"mult"</b><br>
argument <b>two</b> can be of <b>`vv`</b>, <b>`vi`</b>, or <b>`ii`</b><br>
vv is variable to variable, vi is variable to integer, ii is integer to integer.

in case of `vv`:<br>
argument <b>three</b> and <b>four</b> are <b>pre-existing variables</b>.

in case of `vi`:<br>
argument <b>three</b> is a <b>pre-existing</b> variable.<br>
argument <b>four</b> is an integer value.

in case of `ii`:<br>
argument <b>three</b> and <b>four</b> are both integer values.

for all cases:<br>
argument <b>five</b> is a <b>pre-existing variable</b> that will be overwritten with the integer result.

examples:
```
variable string result unset

variable integer int1 25
variable integer int2 10

math add vv int1 int2 result
// result = 30

math neg vi int1 5 result
// result = 20

math mult ii 20 2 result
// result = 40
```

## append
takes in <b>three</b> arguments<br>
argument one can be of `variable` or `string`

if case of argument <b>one</b> being `variable`:<br>
argument <b>three</b> will be appended to argument <b>two</b>

if case of argument <b>one</b> being `string`:<br>
all characters including spaces after argument <b>two</b> will be appended to argument two

examples:
```
variable string part1 Hello, 
variable string part2 World!
append variable part1 part2

print part1
// prints "Hello, World!"
```
```
variable string part1 Gold: 
variable integer gold 25
append variable part1 gold

print part1
// prints "Gold: 25"
```
```
variable string part1 Hello, 
append string part1 World!

print part1
// prints "Hello, World!"
```

## if
takes in <b>three</b> arguments

argument <b>two</b> can be of `==`, `!=`, `matches`, or `matchnt`

in case of argument two being `==` or `!=`:<br>
argument <b>one</b> and <b>three</b> are variable names to check.

`==` is for if the two are equal to each other<br>
`!=` is for if the two are <b>NOT</b> equal to each other

in case of argument two being `matches` or `matchnt`:<br>
argument <b>one</b> will be a variable.
argument <b>three</b> will be an integer.

`matches` is for if the two are equal to each other<br>
`matchnt` is for if the two are <b>NOT</b> equal to each other

if equal. nothing happens
if NOT equal. skip a line.

examples:
```
variable integer int1 25
variable integer int2 25
variable integer int3 10

if int1 == int2
printexa yup that works

if int1 == int3
printexa will not get run

if int1 != int2
printexa will not get run

if int1 != int3
printexa yup that works

if int1 matches 25
printexa yup that works

if int1 matchnt 26
printexa yup that works
```
```
variable string str1 Hello, World!
variable string str2 Hello, World!
variable string str3 Goodbye, World.

if str1 == str2
printexa yup that works

if str1 != str2
printexa will not get run

if str1 == str3
printexa will not get run

if str1 != str3
printexa yup that works

```

## prompt
takes one argument<br>
puts <b>user input</b> (string) into a <b>pre-existing variable</b>

examples:
```
variable string userInput none
prompt userInput

print userInput
// will print whatever the user put in for prompt.
```

## random
takes four arguments<br>

argument <b>one</b> can be of `vv`, `vi`, or `ii`

in case of argument <b>one</b> being `vv`:<br>
argument <b>two</b> and <b>three</b> are to be <b>pre-existing</b> variables.

in case of argument <b>one</b> being `vi`:<br>
argument <b>two</b> is to be a <b>pre-existing</b> variable.<br>
arugment <b>three</b> is to be an <b>integer</b>

in case of argument <b>one</b> being `ii`:<br>
argument <b>two</b> and <b>three</b> are to be integers.

in all cases:
argument <b>five</b> is to be a <b>pre-existing</b> variable that will be overwritten.

examples:
```
variable string result unset
random ii 1 100 result
// generate a random number 1-100 and place it in 'result'

variable string result unset
variable integer start 50
random vi start 60 result
// generate a random number 50-60 and place it in 'result'

variable string result unset
variable integer start 30
variable integer end 50
random vv start end result
// generate a random number 30-50 and place it in 'result'
```

## lowerstring & upperstring

command takes one arugment<br>
argument must be an existing variable of type `string`<br>
upperstring will uppercase all characters on variable's value<br>
lowerstring will lowercase all characters on variable's value