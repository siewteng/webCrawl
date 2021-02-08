from flask import Flask, render_template
import praw
import datetime

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

    # this is the specific url we want to crawl
    submission = reddit.submission(
        url="https://www.reddit.com/r/Genshin_Impact/comments/l9c3et/just_venti/")

    # this only searches the top level comments
    # submission.comments.replace_more(limit=0)
    # for top_level_comment in submission.comments:
    #     print(top_level_comment.body)

    # this prints the reddit post's title, text, etc?
    print("Title: " + submission.title)
    print("Text: " + submission.selftext)
    print("score: " + str(submission.score))
    print("ID: " + submission.id)

    # still not sure how to put it in SG time
    #dateTime = datetime.datetime.fromtimestamp(submission.created_utc)
    #SGdateTime = dateTime.astimezone[datetime.tzname]
    #print("timezone: " + str(datetime.datetime.tzname(self)))
    print("Time: " + str(datetime.datetime.fromtimestamp(submission.created_utc)))

    testText = [submission.title, submission.selftext, str(submission.score)]

    # # this searches infinitely the comments of comments and so on until there are none left
    # submission.comments.replace_more(limit=0)
    # for comment in submission.comments.list():
    #     print(comment.body)
    return render_template("index.html", testText=testText)


if __name__ == "__main__":
    app.run()
