# Airline Close Ratio Analysis

## Summary

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