from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin
import time

def getPage(pageNum):
    page = "https://gamesdonequick.com/tracker/donations/agdq2018?page=%d" % pageNum
    req =  requests.get(page).text
    time.sleep(1)
    return BeautifulSoup(req, "html.parser")

def parseAndWriteComments(): # Parse comments the donor's donation page
    with open("donorlinks.txt") as f:
        donationLinks = f.readlines()

    for link in donationLinks:
        commentPage = requests.get(urljoin('https://gamesdonequick.com', link)).text
        commentSoup = BeautifulSoup(commentPage, "html.parser")
        try:
            file = open("corpus.txt", "a")
            print("Reading link")
            comment = commentSoup.find('td', {'class': "Invalid Variable: commentstate"}).text.strip('\t\r\n')
            if comment != " (Comment pending approval)":
                file.write(comment + " ")
            file.close()
            time.sleep(1)
        except:
            continue
    f.close()

def parseTable(donorFile, donationsTable): # Parse the donation table for the donor links
    for row in donationsTable.findAll('tr'):
        if(row.findAll(text=re.compile('Yes'))):
            link = row.findAll("td")[2].find('a').get('href')
            donorFile.write(link + '\n')
    return donationLinks

def scrape():
    donorFile = open("donorlinks.txt", "w")
    soup = getPage(1)
    totalPages = soup.find('label',{'for':'sort'}).text.split()[1]

    for pageNum in range(1, int(totalPages)+1):
        print("Scraping page: " + str(pageNum))
        soup = getPage(pageNum)
        dt = soup.table.tbody
        donationLinks = parseTable(donorFile, soup.table)
    donorFile.close()

if __name__ == '__main__':
    scrape()
    parseAndWriteComments()
    print("Finished")

