# Reddit Deal Scraper

## Using the git files

* clone repo
* build and run Dockerfile
~~~
docker build -t=reddit-deals .
docker run -v=/home/jhweaver/reddit-deals/scripts:/scripts --name reddit-deal-scraper reddit-deals
~~~

## After deployment

* set cronjob to run scraper on regular basis
* after changes to script, push from local machine and then pull from git to server
  * any changes in the scripts folder on the local machine are passed directly through, so verify they work first
