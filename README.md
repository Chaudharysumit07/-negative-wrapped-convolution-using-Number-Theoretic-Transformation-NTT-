
# Project Title

Write a software code for performing negative wrapped convolution using Number Theoretic Transformation (NTT) for the parameters n = 512, q = 12289, γ = 10968 for Rq = Zq[X]/X^n + 1. Your code must have three distinct functions:
- A function that will take the input in Rq and will convert the input into its corresponding NTT transformation using radix-2 Cooley-Tukey method.
- A function that will take the two inputs which are already transformed by NTT and will produce their point wise multiplication
- A function that will take the inputs in NTT transformed domain and will perform inverse NTT using the radix-2 Gentleman-Sande method


# How to run this code

## Install the dependency

```sh
pip install sympy

```
## Run the file

```sh
python assignment1_solution.py
```

Now it asks for input of 2 polynomial coffecients . 
```sh
Enter coefficients of the first polynomial separated by spaces: 

Enter coefficients of the second polynomial separated by spaces: 

```

enter 2 list of 512 space integer values which are coefficients of 2 polynomials

## Output

- 1st output is NTT transformation of polynomial 1 coefficients

- 2nd output is NTT transformation of polynomial 2 coefficients

- 3rd output is point-wise multiplication of NTT transformed polynomial's coefficients

- 4th output is inverse NTT performed on pointwise multiplication output list 


# Explanation 

n = 512 , q = 12289, r = 10968 

is initialized at the starting of the code.

There  are 3 functions :

- ntt : function that will take the input in Rq and will convert the input into its corresponding NTT transformation using radix-2 Cooley-Tukey method.

- pointwise_multiplication : A function that will take the two inputs which are already transformed by NTT and will produce their point wise multiplication

- intt : function that will take the inputs in NTT transformed domain and will perform inverse NTT using the radix-2 Gentleman-Sande method

There are 4  other helper functions :
- modExponent
- modInv
- bitReverse
- orderReverse
