import time
from datetime import datetime

def convert_to_milliseconds(timestamp):
    """Convert a timestamp to milliseconds if it's in seconds."""
    if timestamp < 10000000000:  # Less than 10 digits suggests seconds
        return int(timestamp * 1000)
    return int(timestamp)

# until now by default
async def fetch_messages(bot, thread_id, from_timestamp, until_timestamp=None):
    """Fetches messages in a given time range from a given thread."""

    # Set default `until_timestamp` to current time if not provided
    if until_timestamp is None:
        until_timestamp = int(time.time())

    until_timestamp_converted = convert_to_milliseconds(until_timestamp)

    all_messages = []
    latest_timestamp = until_timestamp 

    print("Fetching messages...")

    while True:
        # Fetch a batch of messages
        try:
            messages = await bot.fetchThreadMessages(thread_id, limit=20, before=latest_timestamp)
            if not messages:
                break  # Stop if there are no more messages

            # Filter out messages that don't have valid content
            filtered_messages = [msg for msg in messages if from_timestamp <= int(msg.timestamp) < until_timestamp_converted]
            all_messages.extend(filtered_messages)

            # Update latest_timestamp to the oldest message in this batch (for next fetch)
            latest_timestamp = messages[-1].timestamp
            print(datetime.fromtimestamp(int(latest_timestamp)/1000))


            # Stop if the oldest message in the batch is already older than the until_timestamp_converted
            if int(latest_timestamp) <= from_timestamp:
                print("Stopping latest_timestamp is older than until_timestamp.")
                break

            print(str(all_messages))

        except Exception as e:
            print(f"Error fetching messages: {e} (timestamp: {latest_timestamp})")
            continue


    print("Finished fetching messages.")
    print(len(all_messages))

    #return all_messages[::-1]  # Reverse to get messages in chronological order
    return all_messages