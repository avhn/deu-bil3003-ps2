## Introduction to Data Mining - Problem set 2

[![pipeline status](https://gitlab.com/Anaxilaus/bil3003-ps2/badges/master/pipeline.svg)](https://gitlab.com/Anaxilaus/bil3003-ps2/commits/master)

Goal is to generate and prune **binary split classification trees** with an implementation of *CART algorithm*. See [problem set description.](./DESCRIPTION.pdf)

*Technologies used in this project:*

- Python 3.8 (Runs with 3.7)
- GitLab CI
- Git

## Running

To run, use the main.py file, there's no dependencies:
```
$ python3.8 main.py
```
<details><summary>Output</summary>
<pre>
# Decision Tree #
(credit_history in {delayed previously, existing paid, critical/other existing credit})
├(T)─ (credit_amount <= 7882.0)
│     ├(T)─ (credit_history in {delayed previously, existing paid})
│     │     ├(T)─ (property_magnitude in {real estate})
│     │     │     ├(T)─ (credit_amount <= 1768.0)
│     │     │     │     ├(T)─ good
│     │     │     │     └(F)─ (age <= 21.0)
│     │     │     │           ├(T)─ bad
│     │     │     │           └(F)─ good
│     │     │     └(F)─ good
│     │     └(F)─ (age <= 34.0)
│     │           ├(T)─ (employment in {1<=X<4, 4<=X<7})
│     │           │     ├(T)─ good
│     │           │     └(F)─ (credit_amount <= 2578.0)
│     │           │           ├(T)─ (age <= 28.0)
│     │           │           │     ├(T)─ good
│     │           │           │     └(F)─ bad
│     │           │           └(F)─ (employment in {<1, unemployed})
│     │           │                 ├(T)─ (property_magnitude in {real estate, no known property})
│     │           │                 │     ├(T)─ good
│     │           │                 │     └(F)─ bad
│     │           │                 └(F)─ good
│     │           └(F)─ good
│     └(F)─ bad
└(F)─ bad
<br>
# Test Result #
Accuracy: 0.72
TP rate: 0.7345132743362832
TN rate: 0.5833333333333334
TP count: 166
TN count: 14
</pre>
</details>

## Notes

- It is assumed that the .csv file indicates class tag as the last value.
