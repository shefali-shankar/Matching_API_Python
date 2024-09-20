from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Dict
import json
from fuzzywuzzy import fuzz

app = FastAPI()

# Load predefined items from items.json file
with open('items.json') as file:
    items = json.load(file)

# Data Model for input validation
class TradeItem(BaseModel):
    trade: str
    unit_of_measure: str

# Matching algorithm to calculate similarity score
def calculate_similarity(input_data: Dict[str, str], item_data: Dict[str, str]) -> float:
    
    # Similarity score is 1.0 on exact matches  
    if input_data['trade'] == item_data['trade']:
        trade_score = 1.0 
    # If not an exact match, similarity score is a max of 0.99 
    else:  
        # Use Fuzzy Ratios (Levenshtein Distance) to calculate the similarity
        trade_score = 0.99 * fuzz.token_set_ratio(input_data['trade'],item_data['trade'])/100
   
    if input_data['unit_of_measure'] == item_data['unit_of_measure']:
        unit_score = 1.0  
    else:
        unit_score = 0.99 * fuzz.token_set_ratio(input_data['unit_of_measure'],item_data['unit_of_measure'])/100
    
    # No similarity if the score is less than threshold of 0.5 
    if trade_score < 0.5:
        trade_score = 0.0
        
    if unit_score < 0.5:
        unit_score = 0.0
    
    # Provide a weight of 70% to trade and 30% to unit of measure
    return (0.7 * trade_score) + (0.3 * unit_score)

# Post method to match items
@app.post("/match")
async def match_Item(input_data: TradeItem):

    # Error handling for spaces and empty strings
    if input_data.trade.isspace() or input_data.trade == "" or input_data.unit_of_measure.isspace() or input_data.unit_of_measure == "":
        raise HTTPException(status_code=404, detail="One or more Input Strings are empty.")
    
    best_match = None
    best_score = 0.0
    
    # Iterate over items in file and find the best match
    for item in items:
        score = calculate_similarity(input_data.dict(), item)
        if score > best_score:
            best_score = score
            best_match = item

    # Return results if best match is found
    if best_match and best_score > 0.5: #Set match threashold of 0.5
        return {"best_match": best_match, "similarity_score": round(best_score, 2)}
    else:
        raise HTTPException(status_code=404, detail="No matching trade item found")

    
# Error hanling for Invalid Data
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("Invalid Data")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": f"Invalid Data format. {exc.body}"}),
    )

