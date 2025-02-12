def result_message(result):
    if result:
        return {"status": 1, "message": result}
    return {"status": 0, "message": result}