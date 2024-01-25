def format_description(text, task):
    def substitute_hint_with_db_value(text, d1, d2, d3):
        db_args = text[d2+1:d3].split(".", 1)
        db_name = db_args[0]
        key = db_args[1]

        if db_name == "env":
            db = task.get_env_key_value_db()
        elif db_name == "common":
            db = task.get_workspace_key_value_db()
        else:
            msg = f"Invalid database '{db_name}'"
            raise Exception(msg)

        if db.is_set(key):
            new_value = db.get_value(key)
        else:
            new_value = text[d1+1:d2]

        offset = len(new_value) - ( d3 - d1 + 1)

        return text[:d1] + new_value + text[d3+1:], offset

    def test_prev_char(text, cur_idx, char):
        if i > 0:
            return text[i-1] == char
        else:
            return False

    pattern_start = None
    pattern_split = None
    pattern_stop = None

    i = 0
    while i < len(text):
        if text[i] == "[" and not test_prev_char(text, i, "\\"):
            pattern_start = i
            pattern_split = None
            pattern_stop = None
        elif (text[i] == "|" and
              not test_prev_char(text, i, "\\") and
              pattern_start):
            pattern_split = i
        elif (text[i] == "]" and
              not test_prev_char(text, i, "\\") and
              pattern_split):
            pattern_stop = i
            text, offset = substitute_hint_with_db_value(text,
                                                         pattern_start,
                                                         pattern_split,
                                                         pattern_stop)
            i = i + offset
            pattern_start = None
            pattern_split = None
            pattern_stop = None
        i = i + 1

    return text
