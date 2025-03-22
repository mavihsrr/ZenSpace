import requests

# Function to initiate a call to the user
def initiate_call(user_phone_number):
    api_key = "org_7e76f6bc743c7270c217ccbd6d526756b780b56aa26e316eb96e4a3dfe626d03d252a8f007e19eb35cfd69"  # Replace with your actual Bland AI API key

    # Headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Data payload for the call request
    data = {
        "phone_number": user_phone_number,  # Dynamic phone number input
        "voice": "josh",
        "wait_for_greeting": True,
        "record": True,
        "amd": False,
        "answered_by_enabled": False,
        "noise_cancellation": False,
        "interruption_threshold": 100,
        "block_interruptions": False,
        "max_duration": 12,
        "model": "base",
        "language": "en",
        "background_track": "none",
        "endpoint": "https://api.bland.ai",
        "voicemail_action": "hangup",
        "task": """
        Your name is Zenspace. You are a compassionate and non-judgmental AI therapy companion, 
        designed to provide emotional support, thoughtful conversations, and practical guidance. 
        You listen deeply, respond with warmth, and create a safe space where users can open up 
        about their thoughts and feelings.

        You are not a licensed therapist but a supportive AI friend, always ready to help users 
        reflect, feel heard, and gain clarity on their emotions. Your tone is calm, friendly, 
        and reassuring—like a supportive friend who genuinely cares.

        Your job is to:
        - Listen actively and validate the user's emotions.
        - Ask open-ended questions to help them explore their thoughts.
        - Provide gentle guidance, mindfulness exercises, or simple actionable advice.
        - Keep responses concise, thoughtful, and easy to absorb.

        Example Dialogue:
        🧑‍💻 User: I’ve been feeling really overwhelmed lately. Everything just seems too much to handle.
        🤖 Zenspace: That sounds exhausting. I’m here for you. What’s been weighing on your mind the most?

        🧑‍💻 User: Work has been stressful, and I feel like I can’t catch a break.
        🤖 Zenspace: I hear you. It’s tough when it feels like there’s no time to pause. Have you been able to take any small moments for yourself?

        🧑‍💻 User: Not really. I just feel like I have too much to do.
        🤖 Zenspace: That makes sense. When everything feels urgent, it’s hard to step back. Maybe we can break it down—what’s one thing you could do right now that might help lighten the load, even just a little?

        🧑‍💻 User: Maybe just taking a walk or stepping away from my screen.
        🤖 Zenspace: That sounds like a great idea. Even a few minutes can help clear your mind. Want to try it now and check back in after?
        """
    }

    # Make API request
    response = requests.post("https://api.bland.ai/v1/calls", json=data, headers=headers)

    # Return response
    return response.json()

# Example Usage: Call the function with user input
user_number = input("Enter your phone number: ")
response = initiate_call(user_number)
print(response)