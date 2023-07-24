# Spliddit

Spliddit is an algorithm housemates can use to split rent fairly.

Usage:

```
python spliddit.py [fast]
```

The `fast` option skips the typing animation.

## How to split rent

Spliddit is arguably the best way to decide rent and room allocation under most circumstances. Other strategies, like negotiation and going by floor area, have critical flaws. The problem with negotiating is that some people are more willing and/or able to negotiate than others. This might be seen as a good thing for those who are good negotiators, but unequal outcomes in room assignment are apt to create envy or resentment.

Going by floor area provides objectivity, but it can also lead to unfair outcomes. Obviously, residents might care about many aspects of a room other than its size, and size itself doesn't correlate perfectly with utility (it doesn't account for common spaces or sublinear utility). Also, going by square feet doesn't provide a solution for room assignment.

Spliddit takes a third approach: using an algorithm. Although an algorithmic approach might seem opaque, impersonal, or arbitrary, the Spliddit algorithm is specifically designed to be none of those things!

### Spliddit guarantees

Spliddit promotes harmony by guaranteeing the following properties:

#### Envy-freeness

Spliddit finds an outcome where no one wants someone else's room at the price they're paying for it.

#### Low "pettiness"

Spliddit finds an outcome where the difference between your satisfaction and someone else's is minimized.

#### Fairness

Even if someone has positive pettiness, the program is ex-ante fair. In other words, housemates can use Spliddit with the confidence that it won't be biased with respect to room or participant.

As a side-note, it might be non-obvious that "low pettiness" is the best objective. This may be easier to accept considering that the amount of money spent collectively is the same no matter what, so there's no free lunch—lowering one person's rent necessarily raises someone else's.

## Requirements

* Each participant is able to come up with values for each room such that:
	* The values add up to the total rent
	* The participant would be equally happy with any room at those prices
	* The participant can afford any room at those prices.
* Participants can be trusted to report their preferences honestly and based only on personal preferences.
* Participants agree to accept the result of the algorithm without negotiation.
* For N participants, the non-shared parts of the living space can be divided into N partitions that don't change based on who is assigned where.

## Further reading

Original lecture notes: http://s3.amazonaws.com/arena-attachments/1980072/5c6f0b23e0f307a7096dbfb446d1f93b.pdf?1522603643
