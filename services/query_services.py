from app.agents.rag_agent import answer_question


def process_query(request: dict):

    
    question = request["question"]
    customer_profile = request["customer_profile"]
    response = answer_question(question,customer_profile)
    return {
        "question": question,
        "message": "Query received successfully.",
        "response": response,
    }
