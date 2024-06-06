# 2020 U.S. Presidential Election Top Stories
This dataset contains Top stories spanning one year (Dec. 15, 2018 - Dec. 30, 2019) for the 2020 U.S. presidential election candidates. The dataset includes 79,903 unique stories published by 2,168 sources for 30 candidates. More information on data collection method can be found in "The Media Coverage of the 2020 US Presidential Election Candidates through the Lens of Google's Top Stories" to appear in 2020 ICWSM. 

## Top Stories for Candidate
There are 28 Democratic candidates and 2 Republican candidates, listed in *candidatesList.tab*. Each candidate's stories are in *`<candidateName>`.json*. For the most part, story collection begins on Dec. 15, 2018. 

Each json file contains a list of Top story dictionaries. A dictionary contains the following key elements: 
* `title`: title of the article
* `url`: full url of article
* `source`: name of article, e.g. `The New York Times`
* `time`: amount of time that has passed since the article was published, at the time of data collection. Format in `X <timeFrame> ago`, where X is an integer and `timeFrame` is in seconds, minute(s), hour(s), day(s), week(s), or month(s). 
* `date`: day and time for which data was collected in `yyyy-mm-dd hh:mm:ss` format. 
* `query`: candidate name in `firstName lastName` format.
* `story_position`: an integer [1, 10] representing article's position within Top stories panel. 
* `panel_position`: an integer representing position of Top stories panel from top of search result page. 
* `domain`: domain of article, e.g. `www.nytimes.com`

If the data was not collected, a dictionary instead contains the following key elements:
* `reason`: If we did not attempt to collect data for the candidate or experienced hardware/software failure that prevented us from collecting data, `Not collected`. If the search page did not contain an element with the stories, `No Top stories`.
* `date`: day and time for which data is missing in `yyyy-mm-dd hh:mm:ss` format. 


## Metadata on Cumulative Top Stories
***licensedArticles.json***

There are 1,509 collected Top stories that have matching titles with other stories but are published by different sources. This json contains a dictionary of these Top stories. Each dictionary has keys of unique titles and values of a list of Top story dictionaries, for those stories from unique sources with the key title. 

> Note: This is the result of news licensing, which makes it possible for less-resourced news outlets to publish articles distributed by news agencies like AP news, Reuters, etc. For our analysis, we consider licensed articles to be distinct as long as they are published by different sources. However, in the dataset, the number of unique articles counted by having a unique title would differ from the number of unique articles counted by having a unique URL. 


***candidatesList.tab***
* All candidates for which Top stories data is available, in no particular order. 

***candidateStoryStats.tab***

All candidates in descending order based on the number of unique stories collected. A star (`*`) next to a candidate's name indicates that the candidate is no longer a pressidential candidate as of January 9, 2020. 

Each row contains the following elements:
1. `Candidate`: Candidate's name. 
2. `UniqueArticles`: Nummber of unique Top stories collected. 
3. `TotalMoments`: Number of Top stories collected. 
4. `NotCollected`: Number of measurements for which data was not collected because we did not begin collecting or there were hardware and software failures. 
5. `NoTopStories`: Number of measurements for which the search page did not contain an element with the stories. 
6. `PercMissedCollections`: 
```
                (# NotCollected)
-------------------------------------------------- * 100 
(# NotCollected + # TotalMoments + # NoTopStories)
```


***countsOfArticlesBySources.tab***

All news source domains are ranked in descending order, based on the source's unique stories count in dataset. Each row contains:
1. `Domain`
2. `Unique Articles`: Number of unique stories domain published in dataset. 
3. `Total Occurrences`: Number of stories domain published in dataset. 


## News Source Tiers
The sources were ranked by the number of unique stories in the dataset they published, then separated into three tiers: Upper tier, Middle tier, Lower tier. Sources from each tier cumulatively published approximately 1/3 of all the unique stories. 

***upperTierSources.tab***
* 8 ranked sources and their unique story counts. 

***UpperTier_InfoChart.tab***

Metadata on the upper tier sources. Each row includes the following information: 
1. `Rank`: rank within all sources
2. `News Source`
3. `Year Founded`
4. `Main Medium`: online, television, newspaper, magazine. 
5. `Local v National`
6. `Owner`
7. `Alexa Ranking (US)`: An integer indicating source's rank across all domains on the web, based on daily number of page views and unique visitors over 3 months. See alexa.com/siteinfo for more information.
8. `Political Bias Score`: A decimal between [-1, 1] where -1 indicates left-leaning and 1 indicates right-leaning. See https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/QAN5VX for more information.

***middleTierSources.tab***
* 48 ranked sources and their unique story counts. 

***MiddleTier_InfoChart.tab***
* Same metadata as those included in *UpperTier_InfoChart.tab*. 

***lowerTierSources.tab***
* 2,113 ranked sources and their unique story counts.
