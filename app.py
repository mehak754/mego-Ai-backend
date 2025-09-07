from jarvis_logic import say, take_command, handle_query

say("Hello! I am Mego A.I. How can I help you today?")

while True:
    query = take_command()

    if query:
        response = handle_query(query)
        if response:
            say(response)

            # exit conditions
            if any(word in response.lower() for word in ["goodbye", "exit", "quit", "stop"]):
                break


