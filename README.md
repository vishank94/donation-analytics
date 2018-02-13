# Table of Contents
1. [Introduction](README.md#introduction)
2. [Approach](README.md#approach)
3. [Dependencies](README.md#dependencies)
4. [Running the Code](README.md#running-the-code)
5. [Assumptions](README.md#assumptions)
6. [Directory Structure](README.md#directory-structure)


# Introduction

This repository contains solution to coding challenge donation-analytics.


# Approach

1. For the purpose of data streaming, the input data is read line-by-line.
2. Each input data line is checked for missing or improper entries.
3. Each input data entry is validated for TRANSACTION_DT, ZIP_CODE, OTHER_ID.
4. Each donor has a unique UID- concatenation of NAME and corresponding ZIP_CODE.
5. Two dictionaries are maintained to keep a record for all possibilities of donors.
6. These dictionaries contain donor UID as key and their first year of donation as value.
7. Repeated dictionary contains donors who have donated in atleast two different years (with input data in successive order of years).
8. Non-repeated dictionary contains donors who have only donated once/multiple times in same year/in different years but with non-chronological input data.
9. We are only interested in analysing donations that are coming from repeated donors having chronologically documented donation input data.
10. The running percentile calculation is done using the concept of heaps- using minimum and maximum heaps.
11. The maximum heap is implemented by using the concept of minimum heaps but with negation.
12. The (number of) donation amounts are divided into these heaps in the ratio of the desired percentile.
13. So that, the 0th index of the maximum heap always stores the negative of the percentile donation value.
14. The heaps are rebalanced so that at any given point, the length of the maximum heap is equal to the ordinal rank of the set of donations.
15. The above percentile calculation is based on the nearest-rank method.
16. Two dictionaries are maintained to keep a record for all repeat donations and their count.
17. These dictionaries contain combination of CMTE_ID, ZIP_CODE and TRANSACTION_YR as keys.
16. Output dictionary maintains the cumulative TRANSACTION_AMT as its value.
17. Nums dictionary contains the count for repeat donations as its value.
18. Finally, all this is orchestrated under donation_analysis() that takes care of streaming as well.


# Dependencies
Python libraries:
math,
pandas,
heapq,
datetime


# Running the Code
1. Python file donation-analytics.py needs to be run.
2. The input and output files' path is defined in donation_analysis() and main() methods.
3. The repository directory structure given below must be maintained for the code to run successfully.


# Assumptions
1. Multiple donations in the same year aren't taken as repeated for the first occurrence of the same unique ID of the donor.
2. Multiple donations other than the first year of donations are considered as repeat if they occur in the years following respective first year.
3. The 'NAME' field is valid even if it contains only one character since there are no restrictions on its structure as per FEC INDIV data dictionary.


# Directory structure
The directory structure for my repo is as follows:

    ├── README.md 
    ├── run.sh
    ├── src
    │   └── donation-analytics.py
    ├── input
    │   └── percentile.txt
    │   └── itcont.txt
    ├── output
    |   └── repeat_donors.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_1
            |   ├── input
            |   │   └── percentile.txt
            |   │   └── itcont.txt
            |   |__ output
            |   │   └── repeat_donors.txt
            ├── test_DateAndZipCode
            |    ├── input
            |    │   └── itcont.txt
            |    |── output
            |        └── repeat_donors.txt
	    |── test_DifferentPercentileValue
            |    ├── input
            |    │   └── itcont.txt
            |    |── output
            |        └── repeat_donors.txt
	    ├── test_DonationCounterAndDecimalAndMore
            |    ├── input
            |    │   └── itcont.txt
            |    |── output
            |        └── repeat_donors.txt
	    ├── test_MissingFields
            |    ├── input
            |    │   └── itcont.txt
            |    |── output
            |        └── repeat_donors.txt
	    ├── test_SameOrPreviousYear
                 ├── input
                 │   └── itcont.txt
                 |── output
                    └── repeat_donors.txt
