

def format_feedback(feedback):
    valid_body = {"text" : "class 'str'", "rating": "class 'str'"}
    out_feedback = {}
    out_feedback["text"] = feedback["text"]
    out_feedback["rating"] = feedback['rating']
    try:
        for value in out_feedback.values():
            if not type(value) is str:
                raise TypeError
        out_feedback["text"] = out_feedback["text"].capitalize()
        out_feedback["rating"] = float(out_feedback["rating"])
        if out_feedback["rating"] < 1:
            out_feedback["rating"] = 0.0
        if out_feedback["rating"] > 5:
            out_feedback["rating"] = 5.0

        return out_feedback
    except KeyError :
        return {
            "expecte_keys": [key for key in valid_body.keys()] ,
            "received": [key for key in feedback.keys()]
        }
    except TypeError:
        return {
            "expecte_types": [value for value in valid_body.values()],
            "received": [type(value) for value in feedback.values()]
        }
