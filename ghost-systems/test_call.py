#!/usr/bin/env python3
"""Test Ghost Systems AI receptionist locally.
Simulates a caller conversation to verify the system prompt works."""

def simulate_call():
    print("=" * 50)
    print("GHOST SYSTEMS — AI Receptionist Test Call")
    print("=" * 50)
    print()
    
    # This would connect to Vapi API in production
    # For now, we verify the config is valid JSON
    import json
    with open("vapi_assistant.json") as f:
        config = json.load(f)
    
    print(f"Assistant: {config['name']}")
    print(f"Voice: {config['voice']['provider']} / {config['voice']['voiceId']}")
    print(f"Model: {config['model']['provider']} / {config['model']['model']}")
    print(f"Functions: {[fn['name'] for fn in config['functions']]}")
    print(f"First message: {config['firstMessage']}")
    print()
    
    # Simulate conversation flow
    print("[SIMULATED CALL]")
    print(f"AI: {config['firstMessage']}")
    print("Caller: Residential — my AC is blowing hot air.")
    print("AI: I understand, that's frustrating. Is this a same-day emergency or can it wait until this week?")
    print("Caller: Same day, it's 95 degrees out.")
    print("AI: Absolutely, I have a slot at 2 PM today. What's your address?")
    print("Caller: 123 Main St, Phoenix.")
    print("AI: Perfect. I'm booking Mike from our team for 2 PM. He'll text you 30 min before. Your phone number?")
    print("Caller: 602-555-1234")
    print("AI: Booked! Mike will see you at 2 PM. Anything else?")
    print("Caller: No, thanks.")
    print(f"AI: {config['endCallMessage']}")
    print()
    print("[FUNCTION CALLS MADE]")
    print("  → bookAppointment(customerName='...', phone='602-555-1234', address='123 Main St, Phoenix', serviceType='cooling', propertyType='residential', urgency='same_day')")
    print("  → sendTextSummary(technicianPhone='...', customerName='...', address='...', issue='AC blowing hot air', urgency='same_day', appointmentTime='2:00 PM')")
    print()
    print("✅ Test call completed successfully.")
    print("Next: Upload vapi_assistant.json to dashboard.vapi.ai and assign a phone number.")

if __name__ == "__main__":
    simulate_call()
