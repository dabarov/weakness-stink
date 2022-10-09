STICKER_ID_FIELD = "sticker_id"
MESSAGE_SEND_ALIAS = """
Send an alias for the sticker.
Not longer than 20 characters and do not include * sign.
"""
MESSAGE_SEND_STICKER = """
Send a sticker you want to name
"""
MESSAGE_ALIAS_HAS_ASTERISK = """
Your alias includes '*', please enter another alias instead
"""
MESSAGE_ALIAS_TOO_LONG = """
Your alias is too long, maximum length is 20 characters
"""
MESSAGE_SUCCESS = """
The sticker was named successfully.
You can now use it with the following command:
"""
ALIAS_REGEX = r"[*][\w\s]+[*]"
