import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User, Group

class DBManager:

    def __init__(self, db_url):
        """Initialize database connection and session."""
        self.engine = create_engine(db_url, pool_size=10, max_overflow=20, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)  # Creates all tables defined in Base

    def get_session(self):
        """Get a session for database interaction."""
        return self.Session()

    def fetch_all(self, table_class):
        """Fetch all rows from the specified table."""
        with self.get_session() as session:
            try:
                result = session.query(table_class).all()
                return result
            except Exception as e:
                print(f"Error fetching data: {e}")
                return []


    def save_user_to_table(self, user):
        """Insert or update a user in the database."""
        with self.get_session() as session:
            try:
                session.add(user)
                session.commit()
                print(f"User {user.user_id} saved to table 'user_info'")
            except Exception as e:
                session.rollback()
                print(f"Error saving user: {e}")

    def get_all_users(self):
        """Return all users with their IDs and nicknames."""
        users = self.fetch_all(User)
        return [{'user_id': user.user_id, 'nickname': user.nickname} for user in users]


    def save_group_to_table(self, group_name, thread_id):
        """Insert or update a group in the database."""
        with self.get_session() as session:
            try:
                group = Group(group_name=group_name, thread_id=thread_id)
                session.add(group)
                session.commit()
                print(f"Group {group_name} saved to table 'groups'")
                return True
            except Exception as e:
                session.rollback()
                print(f"Error saving group: {e}")
                return False

    def get_all_groups(self):
        """Return all groups with an indexed list of group names."""
        groups = self.fetch_all(Group)
        indexed_groups = [(index + 1, group.group_name) for index, group in enumerate(groups)]
        return indexed_groups

    def rename_group(self, index, new_group_name):
        """Renames a group."""
        with self.get_session() as session:
            try:
                group = session.query(Group).order_by(Group.group_id).offset(int(index)-1).first()
                if group:
                    group.group_name = new_group_name
                    session.commit()
                    print(f"Group has been renamed to '{new_group_name}'")
                    return True
                else:
                    print(f"Group couldn't be found!")
                    return False
            except Exception as e:
                session.rollback()
                print(f"Error renaming group: {e}")
                return False

    def delete_group_from_table(self, index):
        """Delete a group from the table."""
        with self.get_session() as session:
            try:
                group = session.query(Group).order_by(Group.group_id).offset(int(index)-1).first()
                if group:
                    session.delete(group)
                    session.commit()
                    print(f"Group has been deleted from table 'groups'")
                    return True
                else:
                    print(f"Group couldn't be found")
                    return False
            except Exception as e:
                session.rollback()
                print(f"Error deleting group: {e}")
                return False

    def get_thread_id_by_index(self, index):
        """Return the thread_id of the group at the specified index."""
        with self.get_session() as session:
            try:
                # Querying the group by its index (assuming 'group_id' is the index)
                group = session.query(Group).order_by(Group.group_id).offset(int(index)-1).first()
                # Return the thread_id if found, else return None
                return group.thread_id if group else None
            except Exception as e:
                print(f"Error fetching thread_id for group with index {index}: {e}")
                return None


DATABASE_URL = os.getenv("DATABASE_URL")
db_manager = DBManager(DATABASE_URL)