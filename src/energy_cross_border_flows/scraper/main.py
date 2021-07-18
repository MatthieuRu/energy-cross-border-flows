from scraper import Scraper
import yaml
import sys
import requests


if __name__ == "__main__":
    """Main function to run the scraper for the countries in scope.
    """

    # Load the Config File
    configs = {}
    with open('./config.yml', "r") as f:
        configs.update(yaml.load(f, Loader=yaml.FullLoader))

    # Loop on the country & surrounding country to scraped
    # The Scope is a part of the config File
    for country, surrounding_countries in configs['scope'].items():

        # get for a specifics all the combinations between 
        # the country and its surrounding countries
        combinations = [
            [(country, surrounding_country)]
            for surrounding_country in surrounding_countries.split(',')
        ]
        combinations = [item for sublist in combinations for item in sublist]
        print(combinations)
        # For each combinatios run the Scraper
        for combination in combinations:
            # Setup the parameter
            country = combination[0]
            surrounding_country = combination[1]

            # Scraper Class for the specifics combination
            pd_crossborder_flows = Scraper(
                limitation=configs['limitation'],
                entsoe_api_key=sys.argv[1],
                country=country,
                surrounding_country=surrounding_country
            ).execute_scraper()

            # Send to the database by using the API
            requests.post(
                'http://localhost:8000/add-dataframe/',
                data=pd_crossborder_flows.to_json(
                    orient='records', date_format='iso'
                )
            ) 
