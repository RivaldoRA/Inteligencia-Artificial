import tweepy
import csv

load_dotenv()

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

query = '"Carlos Manzo" -is:retweet lang:es'

response = client.search_recent_tweets(
    query=query,
    tweet_fields=["created_at", "lang", "public_metrics", "author_id"],
    max_results=50
)

output_file = "carlos_manzo_tweets.csv"

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["tweet_id", "author_id", "created_at", "text", "like_count", "retweet_count", "reply_count", "quote_count"])

    if response.data:
        for tweet in response.data:
            metrics = tweet.public_metrics
            writer.writerow([
                tweet.id,
                tweet.author_id,
                tweet.created_at,
                tweet.text.replace("\n", " "),
                metrics["like_count"],
                metrics["retweet_count"],
                metrics["reply_count"],
                metrics["quote_count"]
            ])
        print(f"✅ {len(response.data)} tweets saved to {output_file}")
    else:
        print("No tweets found for 'Carlos Manzo'.")
