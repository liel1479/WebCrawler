
# Web Crawler - GitLab
## Description
### What is a web crawler?
A web crawler, spider, or search engine bot downloads and indexes content from all over the Internet. The goal of such a bot is to learn what (almost) every webpage on the web is about, so that the information can be retrieved when it's needed. They're called "web crawlers" because crawling is the technical term for automatically accessing a website and obtaining data via a software program.

## Crawl the Gitlab
This web crawler crawl the GitLab website and store the most recent commits for a configurable repository and branch.

You will need to give it the url of the repo you want to crawl and the specific name of the branch.

First, this web crawler will scroll down the page and get all the commits of the repo.
All the commits will be saved in an excel table and wait 2 minutes.
The next time it will crawl the commits of the branch it will check if the last commit id is exist, if he has it then he will wait 2 minutes and check it again.

## Installing
### step-by-step tutorial:

For running the script, there needs to be pip, pandas and selenium.

In addition, you have to download chrome driver (the supported version for the chrome which is installed on the computer).

**Install commands:**

-pip install selenium

-pip install pandas

