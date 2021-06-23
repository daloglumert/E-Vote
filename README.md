# E-Vote

A voting platform with Blockchain.

## Demo

https://www.youtube.com/watch?v=y4Ouwu4PC94

## Members

Mert Daloğlu 20160808046
Ahmetcan Gürbüz 20160807014

## Installation

```
pip install flask
pip install flask-mysqldb
pip install passlib
pip install wtform
```

## Run

```
python app.py
```

## Methodology

In summary, this project is actually a cryptocurrency. We took a crptocurrency project as main concept and make changes on it. When someone register, system(TBMM in this project) will give you 1 coin. 
There is no way to add manual coin to yourself.
When you vote for someone, you will send your 1 coin to people you select. This transaction will add to blockchain. 
To count vote, system count every transaction in blockchain. Richest person in the candidate will win the vote.

## Findings

Election frauds is always important when election time. To avoid that, this project can be very useful. Because a vote platform with blockchain can't be manipulated. 
Number of voters and total vote can be seen easily. And there can't be a fraud when counting votes. When a voter votes, system will be already count votes. 
After the voting period, results can announce with one click. One of our project weakness is privacy. In database, you can see who voted for who. 
To avoid that, We can encrypt usernames when we're insert data to sql. 