#Knoedler Stock Books
[Dataset](https://github.com/thegetty/provenance-index-csv/tree/master/knoedler)


##Knoedler_01

I'm just starting to get to know the dataset so my modest goal in this first journal is to get a rough estimate of the dealer's activity over the course of its one-hundred-year history. There are many ways to generate such estimates, of course. In this case, to keep things simple, I estimate activity by looking at the volume of transactions as artworks enter and exit the stockbooks. I am therefore concerned really with only two columns from the dataset: `entry_date_year`, which specifies the year the arwork entered the dealer's inventory or else the year it was entered into the stockbook (so, a little fuzziness here); and `sale_date_year`, which specifies the year the artwork was sold. My hypothesis is that examining the number of transactions per year might give us a general sense of how active the dealer was at any given time and how that changed over time.

##Knoedler_02

In this second journal, I am still concerned with measuring the dealer's activity over time. Now, however, I am curious about measuring that activity in terms of transaction value rather than transaction volume--in other words, not how many transactions were made in a given year but the total value of those transactions. As I discover, this becomes complicated for several reasons. First of all, the dealer transacted in multiple currencies--mainly US dollars, German marks, French franks, and British punds--so, each transaction value will need to be converted to the same currency (US dollars) in order to be comparable. Second, the dealer's transactions occur over the course of a century, which means I also have to think about adjusting those historical transaction values to present-day value. These particular challenges I save for the next journal; for now, I am focused on getting a sense of how distributed these currencies are, so that I know how best to proceed. Because the dealer seems to have bought and sold artworks both on its own and in partnership with other dealers, there are columns that will largely concern me here: `purch_currency` (specifying currency for the dealer's solo acquisitions), `knoedpurch_curr` (for the dealer's join acquisitions), `price_currency` (used for the dealer's solo sales), and `knoedshare_crr` (for the dealer's joint sales).

##Knoedler_03

Continuing from the previous journal, here I tackle the challenges involved with measuring activity by transaction value. Having written a crude web scraper to gather all the currency conversion and inflation adjustment, I now have a second dataset to merge with the original dataset containing a multipler that roughly translates historical transactions to 2015 US dollar amounts.
