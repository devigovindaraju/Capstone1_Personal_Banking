from app.agents.rag_agent import answer_question


def process_query(request: dict):

    # Implement--> invoke rag_agent below
    print("FASTAPI RECEIVED REQUEST:", request)
    question = request["question"]

    customer_profile = request.get(
        "customer_profile"
    )


    print("PASSING TO AGENT:")
    print("Question:", question)
    print("Customer Profile:", customer_profile)
    response = answer_question(
        question,
        customer_profile
    )

    print("RESPONSE FROM AGENT:", response)
    return {
        " question": question,
        "message": "Query received successfully.",
        "response": response,
    }


# Also remember to return the response here so that we can send it back

# async def process_query(request: dict):

#  return {
#     "customer_id": request["customer_profile"]["customer_id"],
#     "question": request["question"],
#     "recommendation": "Rag response
#     "risk_warning": " risk_warning.",
#     "citations": []
# }
