from typing import Tuple
import logging
from time import sleep
from datetime import datetime, date, timedelta
import pandas as pd
from entsoe import EntsoePandasClient

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)


class Scraper:
    """Scraper Class which allow to scrape the data from enstoe,
    for a two specifics countries betwen now and a year ago.
    
    """

    def __init__(
        self,
        limitation: float,
        entsoe_api_key: str,
        country: str,
        surrounding_country: str
    ) -> None:
        """Init the class to be able to use the executor_scraping.

        Args:
            limitation (float): the time sleep between each requests
            entso_api_key (str): the key provide to entsoe to use their
            library
            country (str): the main country where the informations is needed
            surrounding_country (str): the country surrounding of the main
            country
        """

        self.limitation = limitation
        self.entsoe_api_key = entsoe_api_key
        self.country = country
        self.surrounding_country = surrounding_country
        self.start_date, self.end_date = self._get_interval()

    def execute_scraper(self) -> None:
        """Run the Scraping process after the Scraper has been initiliaze
        It's scraping for a two countries, the in and out from both side
        in term of energy

        It's using the different internal method from the classes. Only this
        function is able to be used outside of the class.
        """

        logging.info(
            f'Start Running the Scraper for the country {self.country}'
        )
        # Init a empty list where we append DataFrame
        list_pd_crossborder_flows = []

        # Get the all the combination to scrape for the country
        combinations = [
            (self.country, self.surrounding_country),
            (self.surrounding_country, self.country)
        ]

        # Scrape the differents combinations
        for combination in combinations:
            logging.info(f'Scraper runing for {combination}')
            country_code_to = combination[0]
            country_code_from = combination[1]

            # Get raw Data
            crossborder_flows = self._get_ensto_data_query_crossborder_flows(
                country_code_to,
                country_code_from
            )

            # Format the data into pandas
            pd_crossborder_flows_tmp = self._get_pandas_format(
                crossborder_flows=crossborder_flows,
                country_code_to=country_code_to,
                country_code_from=country_code_from
            )
            list_pd_crossborder_flows.append(pd_crossborder_flows_tmp)
            sleep(self.limitation)

        # Concat the two iteraction from the two countries
        pd_crossborder_flows = pd.concat(list_pd_crossborder_flows)

        return pd_crossborder_flows

    def _get_interval(self) -> Tuple[date, date]:
        """Get the start_date and end_date to get the interval from
        today and a year ago.

        Returns:
            start_date (date): the date a year ago
            end_day (date): the date of today
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        return (start_date, end_date)

    def _get_ensto_data_query_crossborder_flows(
        self, country_code_to: str, country_code_from: str
    ) -> pd.Series:
        """Get the raw data using the library
            https://github.com/EnergieID/entsoe-py
        for the `query_crossborder_flows` function.

        Args:
            country_code_from (str): the country where the flows
                is coming from folowing the convention ISO 3166-1 alpha-2.
            country_code_to (str): the country where the flow is going to
                following the convention ISO 3166-1 alpha-2.

        Returns:
            pd.Series: Series with the timestamp and the value in
                megawatts of the flow.
        """

        # Create the client connection
        client = EntsoePandasClient(api_key=self.entsoe_api_key)

        # Use the format of the library
        start = pd.Timestamp(
            self.start_date.strftime('%Y%m%d'), tz='Europe/Amsterdam'
        )
        end = pd.Timestamp(
            self.end_date.strftime('%Y%m%d'), tz='Europe/Amsterdam'
        )

        # Query Entsoe Api using  our parameters
        crossborder_flows = client.query_crossborder_flows(
            country_code_from=country_code_from,
            country_code_to=country_code_to,
            start=start,
            end=end
        )

        return crossborder_flows

    def _get_pandas_format(
        self,
        crossborder_flows: pd.Series,
        country_code_to: str,
        country_code_from: str,
    ) -> pd.DataFrame:
        """Format the data to the good format, following the schema of
        the database.

        Args:
            crossborder_flows (pd.Series): Raw Data from Entsoe
            country_code_to (str): the data which is receiving the energy
            country_code_from (str): the data which is sending the energy

        Returns:
            pd.DataFrame: The formatted DataFrame ready to be send to the
            database
        """
        pd_crossborder_flows = pd.DataFrame(
            crossborder_flows,
            columns=['capacity_mw']
        )
        pd_crossborder_flows['country_code_to'] = country_code_to
        pd_crossborder_flows['country_code_from'] = country_code_from
        pd_crossborder_flows['flow_timestamp'] = pd_crossborder_flows.index
        pd_crossborder_flows.reset_index(drop=True, inplace=True)

        return pd_crossborder_flows
