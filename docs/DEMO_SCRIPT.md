# Demo Script

## 60-90 Second Presentation

“EduRPG is a learning platform MVP that turns study progress into an RPG-style quest flow. The goal is to make lessons feel more motivating by combining subjects, topics, rewards, and profile progression.”

## Click Flow

1. Start on the Home dashboard.
   - Say: “This is the main learner dashboard. It shows player stats, current lesson, daily quests, recent activity, and subject progress.”

2. Click `Learning Map`.
   - Say: “The learning map organizes content by subject and topic. In the MVP, Biology contains the Genetics topic and the lesson `What is DNA?`.”

3. Click `What is DNA?` or `Start route`.
   - Say: “The lesson page presents the content as a quest. The user can see the subject, topic, level, XP reward, and coin reward.”

4. Click `Complete lesson`.
   - Say: “Completing a lesson awards XP and coins. The backend prevents repeatedly farming the same lesson.”

5. Click `Profile`.
   - Say: “The profile shows the demo learner’s level, XP, coins, achievements, streak, and rank-style stats.”

6. Click `Duels` and `Shop`.
   - Say: “These are planned modules. Duels will support battle-based quiz learning, and Shop will let users spend coins on boosts or cosmetics.”

## If Backend Is Not Running

Say:

“For demo stability, the frontend includes polished fallback data. The visual flow still works, but live reward persistence and database-backed content require the Django backend to be running.”

Then continue showing:

- Home dashboard
- Learning Map
- Lesson page
- Profile fallback stats

## Planned Modules Talking Point

“Duels and Shop are intentionally shown as planned modules. They demonstrate the product direction beyond the MVP without pretending the full systems are already implemented.”
