# hack_ai
The following project is created during HackAI hackathon conducted at Univerity of Texas at Dallas.
The code solves Signapay challenge which is to identify fraud companies.

Methods used to identify a fraud company are-
1. Social media is a great source to find out about the company.
Have used twitter live data and Yelp data.
Twitter data- Sentiment analysis using TextBlob to check people's sentiment of the company. 
Sentiments are classified as positive and negative.
2.Yelp data- Most of the local businesses are present in yelp. 
Find the score of each company using the formula score = 0.5(p)(1 - exp(-q/Q))
where p- rating, q- number of rating, Q- any constant.
3.Whois API to check more details about the company given the domain name of the company.
4.iextrading API to check peratio(price/earning ratio), 52weekhigh, 52weeklow of the company. If the given 
company is public, check the financial status of the company.
5.Based on the above 4 factors access risk and detect fraud.

Challenges:
1. Yelp dataset is too small. Use yelp API to check for maximum businesses.
2. iextrading API is not accurate and provides less information.

How to run:
1. You should have python pandas, numpy, tweepy etc..packages to run the code.
2. Code is written in python 3.7.
