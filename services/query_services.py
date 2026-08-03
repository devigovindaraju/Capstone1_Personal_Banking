from app.agents.rag_agent import answer_question
import json


def process_query(request: dict):

    question = request["question"]

    customer_profile = request.get("customer_profile")

    
    try:
        response = answer_question(question,customer_profile)
        response = json.loads(response) 
        print("******************REsponse returned by agent*************************",response)

        return {
            "status": "success",
            "question": question,
            "message": "Query received successfully.",
            "response": response

        }

    except Exception as e:
        #return "error Unable to process your request. Please try again later."
        return {
            "status": "error",
            "error": str(e)
        }