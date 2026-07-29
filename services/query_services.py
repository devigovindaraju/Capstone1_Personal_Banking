from app.agents.rag_agent import answer_question


def process_query(request: dict):

    question = request["question"]

    customer_profile = request.get("customer_profile")


    response = answer_question(question)
    print("******************REsponse returned by agent*************************",response)
   
    return {
        "question": question,
        "message": "Query received successfully.",
        "response": response
        #"citation":response["citations"]
    }
