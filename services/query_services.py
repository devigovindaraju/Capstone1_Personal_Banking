# from agents.rag_agent import create_agent


def process_query(request: dict):

    # Implement--> invoke rag_agent below
    # result = await create_agent(request)

    return {
        " question": request["question"],
        "message": "Query received successfully.",
        "request": request,
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
