import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Initialize Client
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Supabase credentials missing in .env")

supabase: Client = create_client(url, key)

def fetch_user_history(user_id: str):
    """
    Connects to Supabase and fetches the workout history for the user.
    """
    try:
        response = supabase.table("workout_sessions") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .limit(20) \
            .execute()
        
        data = response.data
        if not data:
            print(f"⚠️ No history found for user {user_id}")
            return []
            
        print(f"✅ Successfully fetched {len(data)} sessions from Supabase.")
        return data

    except Exception as e:
        print(f"❌ Database Error: {e}")
        return []

def get_session_details(session_id: str):
    """
    Fetches the full details of a SINGLE session by its UUID.
    """
    try:
        response = supabase.table("workout_sessions") \
            .select("*") \
            .eq("session_id", session_id) \
            .single() \
            .execute()
        
        if not response.data:
            print(f"⚠️ Session {session_id} not found.")
            return None
            
        return response.data

    except Exception as e:
        print(f"❌ Error fetching session {session_id}: {e}")
        return None