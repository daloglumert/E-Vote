# E-Vote

A voting platform with Blockchain.

## Demo

https://www.youtube.com/watch?v=y4Ouwu4PC94

## Members

Mert Daloğlu 20160808046
Ahmetcan Gürbüz 20160807014

## Requirements

pip install flask
pip install flask-mysqldb
pip install passlib
pip install wtform


## Run

python app.py


## Methodology

In summary, this project is actually a cryptocurrency. We took on a cryptocurrency project as the main concept and made changes on it. When someone registers, the system(TBMM in this project) will give you 1 coin. 
There is no way to add coins to yourself.
When you vote for someone, you will send your 1 coin to people you select. This transaction will add to the blockchain. 
To count votes, the system counts every transaction in the blockchain. Richest person in the candidate will win the vote.

## Findings

Election fraud is always important at election time. To avoid that, this project can be very useful. Because a vote platform with blockchain can't be manipulated. 
Number of voters and total vote can be seen easily. And there can't be fraud when counting votes. When a voter votes, the system will already count votes. 
After the voting period, results can be announced with one click. One of our project weaknesses is privacy. In the database, you can see who voted for who. 
To avoid that, We can encrypt usernames when we're inserting data to SQL.