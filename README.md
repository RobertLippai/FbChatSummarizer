# FbChatSummarizer

A chatbot that summarizes Messenger group conversations using AI and stores relevant data in a PostgreSQL database.

## Features
- Fetches messages from Facebook Messenger groups using `fbchat_muqit`
- Summarizes conversations with OpenAI's API (also supports DeepSeek and Gemini)
- Stores user data in a PostgreSQL database (messages will be stored in the future)
- Currently only supports text messages (image support planned)

## Requirements
- SQLAlchemy
- [`openai`](https://github.com/openai/openai-python)
- [`fbchat_muqit`](https://github.com/togashigreat/fbchat-muqit)
- Python 3.x


## Example usage  
Start the bot by run the following command:  

    python bot.py 
It will begin listening for incoming messages.  
  
### 1. Add a group  
You can add a group using the `/addGroup` command, in two ways:  
  
**Add a different group**  
If you want to add a group that is different from where you are  sending the command, you need to provide it's `thread_id`. It can be found by looking at the URL in your browser when you're in a Messenger chat:  
    https://www.messenger.com/t/6161463540609695  

In this case, `6161463540609695` is the `thread_id` for the group.  
  
The command would be:
  
    /addGroup "Group Name" 6161463540609695 

  
  
**Add the current group**  
If you want to add the group where the command is being sent,    you only need to provide the group name. The bot will use the current groups's thread_id.  
  
    /addGroup "Friends Chat"  

  
### 2. Summarizing a conversation  
To summarize the "Friends Chat" group from 12:00 to 14:00:  
- First, use the `/listGroups` command to get the group index.  
- Then, use the `/recap` command with the group index and time range:  
  
    /recap 1 12:00-14:00


## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/robertlippai/FbChatSummarizer.git
   cd FbChatSummarizer
   ```
   
2. **Install dependencies:**
   ```sh
    pip install -r requirements.txt
   ```
   
2. **Set up the database:**
- Ensure a PostgreSQL based database is installed and running properly.

4. **Set up the environment variables:**
   - Create a .env file in the root directory of the project.
   - Add the following variables to the .env file:
   ```dotenv
   OPENAI_API_KEY=your_openai_api_key
   DATABASE_URL=your_database_connection_url
   AI_ENDPOINT_URL="https://generativelanguage.googleapis.com/v1beta/"  # Default endpoint for Gemini
   AI_MODEL_NAME="models/gemini-2.0-flash-exp" 
   ```
   **Some example endpoints:**
   - OpenAI: "https://api.openai.com/v1"
   - For Gemini (Google DeepMind): "https://generativelanguage.googleapis.com/v1beta/"
   - For DeepSeek AI: "https://api.deepseek.com/v1"


5. **Authenticate with Facebook:**
   - Fill `cookies.json` with your extracted Facebook cookies.
   - You can obtain them using the [`C3C FbState Utility`](https://github.com/c3cbot/c3c-ufc-utility).
   - The file shuld be placed in the root directory of the project.

### Future Plans
- Support for images with AI-generated descriptions
- Automatic Summarization: If a user misses a certain number of messages,
the bot will automatically generate and send a recap of the missed conversation
as soon as they open the group.