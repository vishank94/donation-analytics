# Table of Contents
1. [Introduction](README.md#introduction)
2. [Dependencies](README.md#dependencies)
3. [Running the Code](README.md#running-the-code)
4. [Assumptions](README.md#assumptions)
5. [Directory Structure](README.md#directory-structure)


# Introduction

This repository contains solution to Insight Data Engineering Coding Challenge.

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
1. Multiple donations in the same year is not taken to be repeated for the first occurrence of the same unique ID of the donor.
2. Multiple donations other than the first year of donations are considered as repeat.
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
			├── test_DifferentPercentileValue
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
