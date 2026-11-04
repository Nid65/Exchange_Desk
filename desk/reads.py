from desk.config import llm
from desk.state import Claim, DeskState, Tone

llm_claim = llm.with_structured_output(Claim)
llm_tone = llm.with_structured_output(Tone)


def extract_claim(state: DeskState):
    prompt = f"Read this Hopscotch customer message and extract the claim: {state['message']}"
    claim = llm_claim.invoke(prompt)
    return {"claim": claim.model_dump()}


def read_tone(state: DeskState):
    prompt = f"How does this customer sound? Message: {state['message']}"
    result = llm_tone.invoke(prompt)
    return {"tone": result.tone}


if __name__ == "__main__":
    message = "Order HS2291. The 4-5Y kurta set is too small. Please pick it up from 122002."
    print(extract_claim({"message": message}))
    print(read_tone({"message": message}))