Senti

Senti is an AI-powered mental health wake-up platform that helps users start their day with compassion instead of a jarring alarm. Instead of ringing, Senti calls you with a supportive, empathetic AI voice designed to motivate you out of bed — especially on mornings when depression, anxiety, or burnout make it hardest to rise.

🚀 Features

📞 AI Wake-Up Calls – Replace alarms with personalized, empathetic conversations.

🧠 Mood-Aware Responses – Calls adapt to user mood and preferences over time.

🌐 Web Scheduling Interface – Simple interface for booking wake-up calls.

⚡ Low-Latency Infrastructure – Sub-2 second response time during live calls.

🎭 Customizable Personalities – Choose from motivational, gentle, or humorous tones.

🛠 Tech Stack

Backend: Python, FastAPI

Frontend: React

Telephony & AI: AWS Connect, AWS Lex, AWS Lambda

Data & Caching: AWS Elasticache (Valkey)

Cloud Infrastructure: AWS

📐 Architecture Overview

User Scheduling (Web UI): Users book wake-up calls via a React-based interface.

Scheduling Engine: FastAPI + Elasticache store call data and trigger logic.

AI Call Flow:

AWS Connect initiates the call.

AWS Lex handles conversation.

Lambda integrates AI responses in real-time.

Response Delivery: Users receive empathetic, natural voice conversations within seconds.

🎯 Target Audience

Primary: Gen Z & Millennials (18–34) struggling with mornings due to mental health challenges.

Secondary: Caregivers scheduling calls for loved ones, universities, and HR wellness programs.

💡 Why Senti?

Mornings can feel impossible for millions of people living with depression and anxiety. While wellness apps focus on therapy or meditation, Senti addresses the first step of the day: getting out of bed.

By combining empathy with technology, Senti helps users start their day feeling supported, not startled.

📈 Future Roadmap

Mobile app (iOS/Android).

Enhanced personalization with mood tracking & AI adaptation.

Caregiver portal for families to schedule calls remotely.

Corporate wellness integrations.

📝 License

MIT License.
