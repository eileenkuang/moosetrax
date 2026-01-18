import json
import os
from dotenv import load_dotenv
from src.meta_engine import generate_weekly_report
from src.db_connector import fetch_user_history, get_session_details 

load_dotenv()

def main():
    # 1. Define the User
    TARGET_USER_ID = "76f963f6-4a5b-4248-bbe2-69122852a87b" 

    print(f"--- ANALYZING USER: {TARGET_USER_ID} ---")

    # 2. Fetch History
    history_data = fetch_user_history(TARGET_USER_ID)
    if not history_data:
        print("Stopping analysis due to missing data.")
        return

    # 3. Run Meta-Analysis
    report = generate_weekly_report(history_data)

    print("\n" + "="*60)
    print(f"📊 WEEKLY DASHBOARD REPORT")
    print("="*60)
    print(f"🔥 Streak: {report.current_streak_days} Days")
    print(f"🏆 Best Workout ID: {report.best_workout_id}")

    # 4. DEEP DIVE: FETCH BEST SESSION & VIDEO
    if report.best_workout_id and report.best_workout_id != "N/A":
        print(f"\n🔎 Fetching details for Best Workout...")
        
        best_session_data = get_session_details(report.best_workout_id)
        
        if best_session_data:
            analysis = best_session_data.get('analysis', {})
            
            # Extract Video Filename
            video_name = analysis.get('annotated_video_filename', 'default.mp4')
            
            # Create Highlight Card
            highlight_card = {
                "title": "🏆 Best Session of the Week",
                "score": best_session_data.get('form_score'),
                "date": best_session_data['created_at'][:10],
                "summary": analysis.get('personalized_summary'),
                "strengths": analysis.get('strengths', []),
                
                # Frontend Path
                "video_src": f"/videos/{video_name}" 
            }
            
            print(f"🎥 VIDEO LINK: {highlight_card['video_src']}")

            # Save Highlight JSON
            with open("data/best_session_highlight.json", "w") as f:
                json.dump(highlight_card, f, indent=2)
            print("✅ Saved best session data to data/best_session_highlight.json")

    # 5. Save Main Dashboard JSON
    with open("data/weekly_dashboard.json", "w") as f:
        f.write(report.model_dump_json(indent=2))
    print("✅ Dashboard JSON updated at: data/weekly_dashboard.json")

if __name__ == "__main__":
    main()