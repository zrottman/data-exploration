# Knoedler Stock Books
[Dataset](https://github.com/thegetty/provenance-index-csv/tree/master/knoedler)


## 01: Transactions by Volume

I'm just starting to get to know the dataset so my modest goal in this first journal is to get a rough estimate of the dealer's activity over the course of its one-hundred-year history. There are many ways to generate such estimates, of course. In this case, to keep things simple, I estimate activity by looking at the volume of transactions as artworks enter and exit the stockbooks. I am therefore concerned really with only two columns from the dataset: `entry_date_year`, which specifies the year the arwork entered the dealer's inventory or else the year it was entered into the stockbook (so, a little fuzziness here); and `sale_date_year`, which specifies the year the artwork was sold. My hypothesis is that examining the number of transactions per year might give us a general sense of how active the dealer was at any given time and how that changed over time.

## 02: Transactions by Currency

In this second journal, I am still concerned with measuring the dealer's activity over time. Now, however, I am curious about measuring that activity in terms of transaction value rather than transaction volume--in other words, not how many transactions were made in a given year but the total value of those transactions. As I discover, this becomes complicated for several reasons. First of all, the dealer transacted in multiple currencies--mainly US dollars, German marks, French franks, and British punds--so, each transaction value will need to be converted to the same currency (US dollars) in order to be comparable. Second, the dealer's transactions occur over the course of a century, which means I also have to think about adjusting those historical transaction values to present-day value. These particular challenges I save for the next journal; for now, I am focused on getting a sense of how distributed these currencies are, so that I know how best to proceed. Because the dealer seems to have bought and sold artworks both on its own and in partnership with other dealers, there are columns that will largely concern me here: `purch_currency` (specifying currency for the dealer's solo acquisitions), `knoedpurch_curr` (for the dealer's join acquisitions), `price_currency` (used for the dealer's solo sales), and `knoedshare_crr` (for the dealer's joint sales).

## 03: Currency Conversion and Price Adjustment

Continuing from the previous journal, here I tackle the challenges involved with measuring activity by transaction value. Having written a crude web scraper to gather all the currency conversion and inflation adjustment, I now have a second dataset to merge with the original dataset containing a multipler that roughly translates historical transactions to 2015 US dollar amounts. I run into some issues, however. There is some underlying messiness that needs to be cleaned up, for instance. More importantly, I discover that the dealer often bought and sold works in lots, and when this occurred the stockbooks (and thus the dataset) stipulate, for each artwork belonging to the lot, the transaction value of the lot--_not_ the value of the individual artwork, which of course never had a specific price to begin with. For obvious reasons, the largest transactions are often (but not always) multiple artworks, which mean that the largest transaction values tend to be repeated, somtimes dozens of times. For example, the most expensive solo acquisition (in 2015 USD) was valued at about $19M, but consisted of 30+ objects. So it looks like we have 30 transactions valued at ~$19M rather than 1. This I determine is best left to the next journal to sort out. My plan is to begin by looking at transactions of single objects first in order to see how good a picture we get.

## 04: Buyer and Seller Locations

I abandon the previous project, which, it is becoming clear, may not be possible with a dataset as inconsistent and messy as this one. Instead, I pivot to a different series of questions as to the geographical origins and destinations of the artworks in Knoedler's inventory. Where did it acquire its inventory? And where did that inventory get placed? In preparation for this inquiry, I cleaned up the dataset with OpenRefine to make my life a little easier. For the purposes of this notebook, I've limited my inquiry to countries. However, given the fact that the vast, vast majority of artworks mediated by Knoedler ended up in the US (unsurprising for a New York City-based gallery!), the question of artwork destinations may be more interesting when considered at a more granular level—i.e., what cities and states in the US absorbed artworks from Knoedler? I leave that for journal 05.

## 05: U.S. Destinations, Part I

In this notebook I begin looking at where in the United States artworks from Knoedler's inventory ended up. This is mostly preliminary work, since one of the tasks is to pull coordinates for each of these locations so that I'll be able to visualize the data geographically, which I do in the next journal.

## 06: U.S. Destinations, Part II

Here I visualize the buyer location data using the coordinates generated in the previous journal. No surprises here, although nevertheless interesting to see how dispersed Kneodler objects in fact were across the U.S.
