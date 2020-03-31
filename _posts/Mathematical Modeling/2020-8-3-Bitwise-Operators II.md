---
layout: post
title: "Introduction: Bitwise Operators II"
date: 2020-12-03 16:48:38 -0400
category: mathematical-modeling
author: teddy
short-description: A first glance at bitwise operators.
---

# Bitwise-Operators
Bitwise operators are extremely useful. Unfortunately, they often go overlooked - this repository is here to change that.

Bitwise operators are similar to logical operators but they work on a smaller scale. What is special about bitwise operators is that they compare corresponding bits of the number. Although bitwise operators work at the binary level they are used as operators between regular floating point numbers and integers. 

For example, we would call:
* ```5 <bitwise-operator> 2``` not ```0101 <bitwise-operator> 0010``` 

## Types of Bitwise Operators
There are six btiwise operators in python:
* Bitwise AND - ```&```
* Bitwise OR - ```|```
* Bitwise XOR - ```^```
* Bitwise NOT - ```~```
* Bitwsie right shift - ```>>```
* Bitwise left shift - ```<<```



#### Bitwise AND (```&```)
Bitwise AND returns 1 if both bits are 1 ```else``` 0.

| First Bit (A) | Second Bit (B) |  ```A & B```  |
|      :---:    |      :---:     |     :---:   |
|        1      |        1       |       1     |
|        1      |        0       |       0     |
|        0      |        1       |       0     |
|        0      |        0       |       0     |

For example, 

```A = 5``` (0101 in binary) 

```B = 6``` (0110 in binary)

then ```A & B = 0100``` which is equivalent to ```A & B = 4```



#### Bitwise OR (```|```)
Bitwise OR returns 1 if either bit is 1 ```else``` 0.

| First Bit (A) | Second Bit (B) |  ```A \| B```  |
|      :---:    |      :---:     |      :---:    |
|        1      |        1       |        1      |
|        1      |        0       |        1      |
|        0      |        1       |        1      |
|        0      |        0       |        0      |


For example, 

```A = 5``` (0101 in binary) 

```B = 6``` (0110 in binary)

then ```A | B = 0111``` which is equivalent to ```A & B = 7```



#### Bitwise XOR (```^```)
Bitwise XOR returns 1 if one of the bits is 1 and the other is 0 ```else``` 0.

| First Bit (A) | Second Bit (B) |  ```A ^ B```  |
|      :---:    |      :---:     |      :---:    |
|        1      |        1       |        0      |
|        1      |        0       |        1      |
|        0      |        1       |        1      |
|        0      |        0       |        0      |

For example, 

```A = 5``` (0101 in binary) 

```B = 6``` (0110 in binary)

then ```A & B = 0011``` which is equivalent to ```A & B = 3```

#### Bitwise NOT (```~```)
Bitwise NOT returns one's compliment. A quick trick to calculate ~A is to take -A and take one away from it. More formally add one to the binary number 

| First Bit (A) |    ```~A```   |
|      :---:    |      :---:    |
|        1      |        0      |
|        0      |        1      |

For example, 

```A = 5``` (0101 in binary) 

then ```~A = -(0101 + 0001) = -(0110)``` which is equivalent to ```~A = -6```

#### Bitwise Right Shift (```>>```)
Bitwise right shift will shift the numbers to the right by the defined integer. In essense ```A >> n ``` is equivalent to ``` A // 2^n ``` - that is the floor of ```A / 2^n```.

For example, 

```A = 5``` (0101 in binary) 

* then ```A >> 1 = 0010``` which is equivalent to ```A = 2```
* then ```A >> 2 = 0001``` which is equivalent to ```A = 1```

#### Bitwise Left Shift (```<<```)
Bitwise right shift will shift the numbers to the right by the defined integer. In essense ```A << n ``` is equivalent to ``` A * 2^n ```.

For example, 

```A = 5``` (0101 in binary) 

* then ```A << 1 = 1010``` which is equivalent to ```A = 10```
* then ```A << 2 = 10100``` which is equivalent to ```A = 20```

## Check out the page for common uses for bitwise operators!
