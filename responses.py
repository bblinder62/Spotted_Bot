from random import choice, randint

def get_response(user_input: str, user:str) -> str:
    lowered: str = user_input.lower()
    if lowered == '':
        return "No need to be shy"
    elif "hello" in lowered:
        return "hello there!"
    # else:
    #     return "\"You get no response...\""
    