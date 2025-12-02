from chatbot.dialogue_system import DialogueSystem

def main():
    """Main chatbot interface."""
    print("=" * 50)
    print("E-Commerce Customer Support Chatbot")
    print("=" * 50)
    print("Type 'quit' to exit\n")
    
    dialogue_system = DialogueSystem()
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Bot: Thank you for using our support chatbot. Goodbye!")
            break
        
        if not user_input:
            continue
        
        response = dialogue_system.process_input(user_input)
        print(f"Bot: {response}\n")

if __name__ == "__main__":
    main()
