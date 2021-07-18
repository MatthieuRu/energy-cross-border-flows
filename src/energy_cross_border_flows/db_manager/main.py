from fastapi import FastAPI
import uvicorn
from server import Server
from typing import List
from pydantic import BaseModel
import pandas as pd
import sys
import yaml


# Create the connection
app = FastAPI()

configs = {}
with open('./config.yml', "r") as f:
    configs.update(yaml.load(f, Loader=yaml.FullLoader))

server = Server(
    ip=sys.argv[1],
    user=configs['user'],
    passwd=configs['passwd'],
    database=configs['database']
)


# Class to be able to store the data
class Flow(BaseModel):
    capacity_mw: float
    country_code_to: str
    country_code_from: str
    flow_timestamp: str


@app.get("/date/{date}/country/{country_a}/country/{country_b}")
async def query_table(date: str, country_a: str, country_b: str):
    """ Extract from energy_cross_border_flows, all information from
        two countries.
    """
    query = """
        SELECT
            *
        FROM
            dexter.energy_cross_border_flows as ecbf
        WHERE
            DATE(flow_timestamp) = '{0}' and
            country_code_to in ('{1}', '{2}') and
            country_code_from in ('{2}', '{1}')
    """.format(
        date,
        country_a,
        country_b
    )
    pd_crossborder_flows = server._execute_extract(query)
    return pd_crossborder_flows.to_dict(orient='record')


@app.post("/add-dataframe", status_code=201)
async def add_dataframe(data: List[Flow]):
    """ Send tp energy_cross_border_flows a list of Flow,
        using the function from db_manager.table
    """
    pd_crossborder_flows = pd.DataFrame.from_records([s.__dict__ for s in data])

    # Compute regex matches
    server.db['dexter'].tb['energy_cross_border_flows'].append_dataframe(
        pd_crossborder_flows
    )

    return data


if __name__ == "__main__":
    """Run the API on the machin
    """
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug"
    )
