from db_manager import db_manager
from models import User


class UserDataManager:
    def __init__(self):
        self.user_cache = {}

    def load_user_data(self):
        """Load user data from the database into cache."""
        try:
            users = db_manager.get_all_users()
            self.user_cache = {user['user_id']: user['nickname'] for user in users}
        except Exception as e:
            print(f"Error loading user data: {e}")
            self.user_cache = {}

    def get_user_name_cache(self, user_id):
        """Retrieve the username from the user cache."""

        print(f"Looking for user name for {user_id}")

        user_name = self.user_cache.get(user_id, "id_lookup_failed")
        print(user_name)
        return user_name

    async def get_user_name(self, bot, user_id):
        """Retrieve the username from the user cache or fetch it if not found."""
        if user_id not in self.user_cache:
            await self.get_user_info(bot, user_id)

        print(f"Looking for user name for {user_id}")

        user_name = self.user_cache.get(user_id, "id_lookup_failed")
        print(user_name)
        return user_name

    async def get_user_info(self, bot, user_id):
        """Fetch user info and update the database and cache."""
        try:
            user_info = await bot.fetchUserInfo(user_id)
            print(user_info)

            if user_id not in user_info:
                print(f"User info for {user_id} not found.")
                return

            user_info = user_info[user_id]
            user = User(user_id=user_id, nickname=user_info.name.split()[0], full_name=user_info.name)

            db_manager.save_user_to_table(user)
            self.user_cache[user_id] = user_info.name  # Update cache

            print(f"User cache updated: {user_id} -> {user.nickname}")

        except Exception as e:
            print(f"Error fetching user info for {user_id}: {e}")

user_data_manager = UserDataManager()
user_data_manager.load_user_data()
print(db_manager.get_all_users())
