import praw
import requests
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import os
import subprocess

url = 'https://www.reddit.com'
email_username = os.environ['email']
email_password = os.environ['pass']

reddit = praw.Reddit(client_id='redacted',
                     client_secret='redacted',
                     password='redacted',
                     user_agent='deal_scraper by /u/redacted',
                     username='redacted')

def buildapcsales():
    '''
    returns [deal{id,title,url}, deal{id,title,url}, etc.]
    '''
    deals = []
    response = reddit.subreddit('buildapcsales').new()
    for submission in response:
        title = submission.title.lower()
        if "monitor" in title and ('ultrawide' in title or '32"' in title):
            deals.append({'id':submission.id, 'title':submission.title.lower(),'url':url + submission.permalink})

    return deals

def blacklist(deals):
    '''
    Checks for existence of deal id. 
    If it is there, remove from deals to send email about.
    If it is not there, add to blacklist.
    Returns dictionary with deals not yet emailed about.
    '''
    append_blacklist =[]
    updated_deals = []

    if not os.path.isfile('blacklist.txt'):
        subprocess.call('touch blacklist.txt', shell=True)
    else:
        pass
    
    with open('blacklist.txt','r') as f:
        data = f.read()
        for deal in deals:
            if deal['id'] not in data:
                append_blacklist.append(deal['id'])
                updated_deals.append(deal)

    with open('blacklist.txt','a') as f:
        for item in append_blacklist:
            f.write('%s\n' % item)

    return updated_deals
    

def email_deals(deals):
    message = ''
    for deal in deals:
        message = message + deal['title'] + "\n" + deal['url'] + "\n\n"
    
    s = smtplib.SMTP(host='smtp.gmail.com', port=587, timeout=120)
    s.starttls()
    while True:
        try:
            s.login(email_username,email_password)
            break
        except:
            print("\nAuthentication failed. Exiting...\n")
            raise SystemExit(0) # Check this to be the cause of problems down the road.
    
    msg = MIMEMultipart()        
    msg['From']=email_username
    msg['To']=email_username
    msg['Subject']="Reddit Deals Spotted"
    msg.attach(MIMEText(message, 'plain'))
    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg
    
    # Terminate the SMTP session and close the connection
    s.quit()


results = buildapcsales()
updated_results = blacklist(results)
if updated_results:
    email_deals(updated_results)
