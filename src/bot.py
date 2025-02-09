import asyncio
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

from fbchat_muqit import Client, Message, ThreadType
from db_manager import db_manager
from message_fetcher import fetch_messages
from summary_generator import summarize_conversation
from time_parser import parse_time_range


now = datetime.now()

# TODO
# Save, delete, update user in database
class FbChatSummarizer(Client):
    """A Messenger chatbot that summarizes group conversations."""

    async def onMessage(self, mid, author_id: str, message_object: Message, thread_id, thread_type=ThreadType.USER, **kwargs):
        """Handles incoming messages and executes commands."""

        # ignore own response
        if author_id == self.uid:
            return

        message_text = message_object.text.strip() # removes leading trailing whitespaces
        parts = message_text.split(maxsplit=1)  # Split into command and arguments
        command = parts[0].lower()  # Extract the command (e.g., "/addgroup")
        args = parts[1] if len(parts) > 1 else ""  # Everything after the command

        if command == "/help" or command == "/h":
            help_message = """
Here are the currently available commands:

/listGroups  - Lists all the available groups.
/addGroup    - Adds a new group. Usage: /addGroup <group_name> [<group_id>]
/deleteGroup - Deletes a group. Usage: /deleteGroup <group_name>
/renameGroup - Renames a group. Usage: /renameGroup [<group_id>] <new_group_name>
/recap       - Summarizes messages from a group. Usage: /recap <group_index> <time_range> (e.g., HH:MM, HH:MM-HH:MM, MM-DD, YYYY-MM-DD)
/ping        - Checks if the bot is online.
/help (/h)   - Displays this help message.
        """
            await self.sendMessage(help_message, thread_id, thread_type)
            return

        # /ping – Checks if the bot is online.
        if command == "/ping":
            await self.sendMessage("Pong!", thread_id, thread_type)
            return

        if command == "/recap":
            await self.handle_recap(args, thread_id, thread_type)
            return

        if command == "/listgroups":
            await self.list_groups(thread_id, thread_type)
            return

        if command == "/addgroup":
            await self.add_group(args, thread_id, thread_type)
            return

        # /rename [GroupID] [NewName] – Renames a group.
        if command == "/renamegroup":
            await self.rename_group(args, thread_id, thread_type)
            return

        if command == "/deletegroup":
            await self.delete_group(args, thread_id, thread_type)
            return


    async def onReply(self, mid, author_id, message_object, thread_id, thread_type=ThreadType.USER, **kwargs):

        # ignore own response
        if author_id == self.uid:
            return

        #Recaps the conversation from the message being replied to up until now.
        if message_object.text.lower() == "/recap":
            print(f"Recap started with message timestamp: {message_object.replied_to.timestamp}")

            messages = await fetch_messages(self, thread_id, message_object.replied_to.timestamp)
            summary = await summarize_conversation(messages)
            await self.sendMessage(f"Recap:\n{summary}", thread_id, thread_type)

    async def handle_recap(self, args, thread_id, thread_type):
        """Handles the /recap command."""
        parts = args.split(maxsplit=2)
        print(parts)

        if len(parts) < 2:
            await self.sendMessage("Invalid command! Use /recap [Group] [Time].", thread_id, thread_type)
        else:
            group_index = parts[0]  # user provided index
            print(group_index)
            group_id = db_manager.get_thread_id_by_index(group_index)  # actual group id
            print(group_id)
            if not group_id:
                await self.sendMessage(
                    f"Invalid group index {group_index}. Use /listgroups to see available groups.", thread_id,
                    thread_type)
            else:
                time_range = parse_time_range(parts[1]) if len(parts) > 1 else parse_time_range(
                    now.strftime("%H:%M"))

                print(time_range)

                if time_range:
                    start_time, end_time = time_range  # Now in milliseconds (Unix timestamp)
                    messages = await fetch_messages(self, group_id, start_time, end_time)
                    summary = await summarize_conversation(messages)
                    #await self.sendMessage(f"Summary for {group_index} ({start_time} - {end_time}):\n{summary}", thread_id, thread_type)
                    await self.sendMessage(f"Generated summary:\n{summary}", thread_id, thread_type)
                else:
                    await self.sendMessage("Invalid time format! Use HH:MM, MM-DD, or YYYY-MM-DD.", thread_id, thread_type)

    async def list_groups(self, thread_id, thread_type):
        """Lists all saved groups."""
        groups = db_manager.get_all_groups()

        if groups:
            # Group names with their indices
            group_list_message = "\n".join([f"{index} -- {group_name}" for index, group_name in groups])
            print(group_list_message)
            await self.sendMessage(f"Here are the available groups:\n{group_list_message}", thread_id, thread_type)
        else:
            # No groups exist
            await self.sendMessage("No groups found.", thread_id, thread_type)

    async def add_group(self, args, thread_id, thread_type):
        """Adds a new group."""
        message_content = args.strip().split()

        group_name = message_content[0] if len(message_content) > 0 else None
        group_id = int(message_content[1]) if len(message_content) > 1 else thread_id

        # group name is mandatory
        if group_name is None:
            #await self.sendMessage("A group name is required!", thread_id, thread_type)
            await self.sendMessage(
                "Usage: /addGroup <group_name> [<group_id>]\n- <group_name> is required.\n- <group_id> is optional (defaults to the current group).",
                thread_id, thread_type)
            return

        result = db_manager.save_group_to_table(group_name, group_id)

        if result:
            await self.sendMessage(f"Group '{group_name}' has been saved!", thread_id, thread_type)
        else:
            await self.sendMessage(f"Failed to save group '{group_name}'.", thread_id, thread_type)

    async def rename_group(self, args, thread_id, thread_type):
        """Renames a group."""
        message_content = args.strip().split()

        group_index = message_content[0] if len(message_content) > 0 else None
        new_group_name = message_content[1] if len(message_content) > 1 else None

        if group_index is None or new_group_name is None:
            await self.sendMessage("Usage: /renameGroup <group_index> <new_group_name>", thread_id, thread_type)
            return

        result = db_manager.rename_group(group_index, new_group_name)

        if result:
            await self.sendMessage(f"Group '{group_index}' has been renamed!", thread_id, thread_type)
        else:
            await self.sendMessage(f"Failed to rename group '{group_index}'.", thread_id, thread_type)

    async def delete_group(self, args, thread_id, thread_type):
        """Deletes a group."""
        message_content = args.strip().split()

        group_index = message_content[0] if len(message_content) > 0 else None

        # group index is mandatory
        if group_index is None:
            await self.sendMessage("Usage: /deleteGroup <group_index>", thread_id, thread_type)
            return

        result = db_manager.delete_group_from_table(group_index)

        if result:
            await self.sendMessage(f"Group '{group_index}' has been deleted!", thread_id, thread_type)
        else:
            await self.sendMessage(f"Failed to delete group '{group_index}'.", thread_id, thread_type)

async def main():
    cookies_path = "../cookies.json"  # Replace with the path to your saved cookies
    bot = await FbChatSummarizer.startSession(cookies_path)

    try:
        await bot.sendMessage("Bot is ready!", "100058264647160", ThreadType.USER)
        await bot.listen()  # Start listening for messages
    except Exception as e:
        print(e)


asyncio.run(main())