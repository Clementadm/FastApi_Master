from fastapi import FastAPI
from router import configuration_route
import uvicorn

app = FastAPI()

app = configuration_route(app)

# Run website
if __name__ == '__main__':
    uvicorn.run(app)