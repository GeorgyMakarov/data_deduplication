# Airline Close Ratio Analysis

## Problem statement

Datasets can contain duplicated data belonging to the same entity. Duplicated
rows can be skewing important business metrics or any ratios that rely on 
computations of fractions. This is important across industrial, government and
academic fields. Sometimes companies rely on manual deduplication of records. 
It can be a time consuming process prone to random human related errors. 

One of the ways to overcome the issues of manual data deduplication is to 
let this job to be done by computers. There are different approaches to this
problem, but one of the most simple is deterministic data deduplication that is
performed according to a set of rules. Deterministic methodology has its pros and
cons as any other method.

Pros:

&check; simple to implement  
&check; explainable  
&check; applicable for concept testing  

Cons:

&cross; hard to decide on criteria of deduplication if many dimensions in data  
&cross; prone to systematic skewing based on human judgement  

This repo shows how to approach deterministic data deduplication using `Python`
code.

## Entering data and assumptions

An airline tracks an important business metric **close ratio** to understand how
people interact with their website. Close ratio is a fraction of a number of sales
from a number of quotes made. A quote resulting in a purchase represents one
sale no matter the number of tickets purchased.

The data consists of **2152** rows and **298** sales, which results in **13.8**
percent close ratio. The airline thinks that the close ratio is too low and finds
out that many quotes are similar by user, dates, destinations and prices. Having
that in mind, they suggest that the data is duplicated.

The airline wants to deduplicate the records that represent the same entity and
are looking for a programmatic solution that can be easily implemented and that
can allow to test multiple concepts.

**The objective is to code an algorithm that allows the company to deduplicate data effectively and reduce the skeweness of the close ratio.**

## Coding strategy

The simplest way to reach the objective is to use a set of determined rules to
aggregate the rows by groups belonging to the same interaction. One set of
rules could be the aggregation by user and by flight date falling into some cut
off interval.

The pseudo code of this algorithm looks as following:

```
for cut-off date in [1, 2, 3, ..., n]:
  
  for user in unique(users):
    filter data to user
    sort records in ascending order by flight date
    assign groups of quotes that fall into same cut-off threshold
    find duplicates in the same group (their sales flag = 0)
    
    if there are sales in a group (sales flag = 0):
      leave quotes with closed sales for this group (sales falg = 0)
    else:
      leave quote with the last non-closed sale (latest interaction time)
    return quotes list
  
  filter input data to contain the quotes in the list
  compute new close ratio
```

The `Python` implementation of the algorithm is in [data_deduplication.py](https://github.com/GeorgyMakarov/data_deduplication/blob/main/data_deduplication.py) file.

## Summary

The result of this operation shows that the close ratio will grow as we iterate
over the growing cut off dates. This shows positive effect of deduplication of the
data. At the same time, the correct value of cut off depends on the domain
knowledge of a user as aggregating the data by larger intervals will finally
result in a 100 percent close ratio.


