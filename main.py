from selenium import webdriver
from time import sleep
import pandas as pd
from selenium.webdriver.common.by import By


class Commit:
    def __init__(self, date, title, commit_href, commit_id, committer_name, committer_username):
        self.date = date
        self.title = title
        self.commit_href = commit_href
        self.committer_name = committer_name
        self.committer_username = committer_username
        self.commit_id = commit_id

    def get_dict(self):
        return {
            'date': self.date,
            'title': self.title,
            'commit_href': self.commit_href,
            'committer_name': self.committer_name,
            'committer_username': self.committer_username,
            'commit_id': self.commit_id,
        }


class GitlabCrawler:
    def __init__(self, chromedriver_path, repo_url, branch_name):
        self.chromedriver_path = chromedriver_path
        self.url = repo_url + '/commits/' + branch_name
        self.driver = webdriver.Chrome(chromedriver_path)

    def scroll_down(self):
        """A method for scrolling the page."""

        # Make sure page is loaded and ready to be scrolled
        sleep(1)

        # Get scroll height.
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to the bottom.
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            sleep(3)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

    def crawl(self, check=False, first_commit_id_last_iter=None, to_save=True):
        self.driver.get(self.url)
        first_commit_id = self.driver.find_element(by=By.CLASS_NAME, value='commit').get_attribute('id').split('-')[1]
        print(first_commit_id, first_commit_id_last_iter)

        if check and first_commit_id_last_iter:
            if first_commit_id_last_iter == first_commit_id:
                print('nothing new, going to sleep for 2 minutes')
                return [], first_commit_id, False

        self.scroll_down()

        all_commits = []
        commits_rows = self.driver.find_elements(by=By.CLASS_NAME, value='commits-row')
        for commits_row in commits_rows:
            date = commits_row.get_attribute('data-day')
            commits = commits_row.find_elements(by=By.CLASS_NAME, value='commit')
            for commit in commits:
                commit_id = commit.get_attribute('id').split('-')[1]
                a = commit.find_element(by=By.CLASS_NAME, value='commit-row-message')
                href = a.get_attribute('href')
                title = a.text
                committer_webelement = commit.find_element(by=By.CLASS_NAME, value='commit-author-link')
                committer_name = committer_webelement.text
                committer_username = committer_webelement.get_attribute('href').split('/')[-1]
                all_commits.append(Commit(date, title, href, commit_id, committer_name, committer_username))

        return all_commits, first_commit_id, True


def main():
    chromedriver_path = r"chromedriver.exe"
    url = input('Please enter the repository url:')
    branch_name = input('Please enter branch name:')

    git_crawler = GitlabCrawler(chromedriver_path, url, branch_name)
    commits, first_commit_id, to_save = git_crawler.crawl()
    df = pd.DataFrame.from_records([commit.get_dict() for commit in commits])
    df.to_excel("output.xlsx")
    sleep(120)

    while True:
        commits, first_commit_id, to_save = git_crawler.crawl(check=True, first_commit_id_last_iter=first_commit_id)
        df = pd.DataFrame.from_records([commit.get_dict() for commit in commits])
        if to_save:
            df.to_excel("output.xlsx")
        sleep(120)


if __name__ == '__main__':
    main()
