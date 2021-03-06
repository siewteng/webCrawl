from flask import Flask, request, render_template
import praw
import datetime
from datetime import timezone
from dateutil import tz

import os
import psycopg2

# connecting to database
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

cursor = conn.cursor()

# datetime stuff
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

reddit = praw.Reddit(client_id='bZnvlnGcW_cD_g',
                     client_secret='AmvzgAQojypX7OSILSDhfnIjGMIFlQ', user_agent='hootsnoow')

app = Flask(__name__)


@app.route("/")
def index():

    # # Load current count
    # f = open("count.txt", "r")
    # count = int(f.read())
    # f.close()

    # # Increment the count
    # count += 1

    # # Overwrite the count
    # f = open("count.txt", "w")
    # f.write(str(count))
    # f.close()

    # # Render HTML with count variable
    # return render_template("index.html", count=count)

    # ----------------------------------------------------

    # this only searches the top level comments
    # submission.comments.replace_more(limit=0)
    # for top_level_comment in submission.comments:
    #     print(top_level_comment.body)

    # this prints the reddit post's title, text, etc?
    # print("Title: " + submission.title)
    # print("Text: " + submission.selftext)
    # print("score: " + str(submission.score))
    # print("ID: " + submission.id)

    # still not sure how to put it in SG time
    # dateTime = datetime.datetime.fromtimestamp(submission.created_utc)
    # SGdateTime = dateTime.astimezone[datetime.tzname]
    # print("timezone: " + str(datetime.datetime.tzname(self)))
    # print("Time: " + str(datetime.datetime.fromtimestamp(submission.created_utc)))

    # # this searches infinitely the comments of comments and so on until there are none left
    # submission.comments.replace_more(limit=0)
    # for comment in submission.comments.list():
    #     print(comment.body)
    return render_template("index.html")


@app.route('/', methods=['POST'])
def my_form_post():
    theURL = request.form['theURL']
    # this is the specific url we want to crawl
    submission = reddit.submission(
        url=theURL)
    submission.comments.replace_more(limit=0)

    submissionDateTime = datetime.datetime.fromtimestamp(
        submission.created_utc)
    submissionDateTimeSG = submissionDateTime.replace(
        tzinfo=timezone.utc).astimezone(tz=None)

    mainPost = [submission.author, submission.title,
                submission.selftext, str(submission.score), str(submissionDateTimeSG)]

    # insert into the postgress part as well
    insertDatabase = "INSERT INTO urls (url, id, title, author, body, time, upvotes) \
        VALUES ( % s, % s, % s, % s, % s, % s, % s)"
    actualValues = (theURL, submission, submission.title, submission.author,
                    submission.selftext, submissionDateTimeSG, submission.score)
    #cursor.execute(insertDatabase, actualValues)

    commentId = []
    commentParent = []
    commentAuthor = []
    commentBody = []
    commentTime = []
    commentScore = []
    for comment in submission.comments.list():
        commentId.append(comment)
        commentParent.append(comment.parent_id)
        commentAuthor.append(comment.author)
        commentBody.append(comment.body)
        commentScore.append(comment.score)

        # configuring the datetime formatting
        dateTime = datetime.datetime.fromtimestamp(comment.created_utc)
        SGdateTime = dateTime.replace(tzinfo=timezone.utc).astimezone(tz=None)
        # utc = dateTime.replace(tzinfo=from_zone)
        # SGdateTime = utc.replace(int(to_zone))
        commentTime.append(SGdateTime)

    return render_template("index.html", mainPost=mainPost, commentId=commentId,
                           commentParent=commentParent, commentAuthor=commentAuthor, commentBody=commentBody, commentScore=commentScore, commentTime=commentTime)
    # return render_template("index.html", mainPost=mainPost, commentBody=commentBody)


if __name__ == "__main__":
    app.run()
