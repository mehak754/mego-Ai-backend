import jarvis_logic

if __name__ == '__main__':
    jarvis_logic.say("Hello! I am Mego A.I. How can I help you today?")

    while True:
        query = jarvis_logic.take_command()

        if query:
            response = jarvis_logic.handle_query(query)
            if response:
                jarvis_logic.say(response)

                if any(word in response.lower() for word in ["goodbye", "exit", "quit"]):
                    break
