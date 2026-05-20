import os
import asyncio
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from concurrent.futures import ThreadPoolExecutor

# --- 1. CPU OPTIMIZATIONS FOR VPS ---
# Limit TensorFlow to 1 CPU thread to prevent system-wide lag
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TF_NUM_INTRA_OP_THREADS"] = "1"
os.environ["TF_NUM_INTER_OP_THREADS"] = "1"

tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace '*' with your specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
model = None
# This Semaphore(1) ensures only ONE model run happens at a time
model_semaphore = asyncio.Semaphore(1)
# Thread pool to run the heavy model work without freezing the API
executor = ThreadPoolExecutor(max_workers=1)

@app.on_event("startup")
def load_model():
    global model
    print("Loading model...")
    # Loading can be slow on VPS, do it once at startup
    model = tf.keras.models.load_model("model_aapl_trained.keras")
    print("Model ready!")

class InputData(BaseModel):
    data: List[List[float]]

def sync_predict(data_as_list):
    """The actual heavy math, wrapped in a standard function"""
    input_array = np.array([data_as_list])
    # Calling model.predict on CPU can be slow
    prediction = model.predict(input_array)
    return prediction.tolist()

@app.post("/predict")
async def predict(request: InputData):
    async with model_semaphore:
        # Convert the 2D list into a 3D array for the model 
        # (Batch_size=1, Time_steps=30, Features=N)
        input_array = np.array([request.data]) 
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(executor, model.predict, input_array)
        return {"prediction": result.tolist()}

@app.get("/health")
def health():
    # This will now remain responsive even while the model is running
    return {"status": "ok", "locked": model_semaphore.locked()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10002)