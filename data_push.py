import requests
import json
def push_data_to_api(url, json_data_arr):
    """
    Pushes data to an API with the specified request body.

    Args:
        url: The URL of the API endpoint.
        name: The name of the item.
        description: The description of the item.
        price: The price of the item.
        item_type: The type of the item.
    """
    item_id_arr = []
    for item in json_data_arr:

        data = item

        response = requests.post(url, json=data)

        if response.status_code == 200:
            print("Data pushed successfully!")
            id_val = json.loads(response.text)["id"]
            print(id_val)
            item_id_arr.append(id_val)
        else:
            print("Error pushing data:", response.text)
    return item_id_arr

def validate_data_to_api(url_1, json_data_arr, id_arr):
    validate = False
    for index, value in enumerate(json_data_arr):
        url = f"{url_1}{id_arr[index]}"
        response = requests.get(url)
        data_back = json.loads(response.text)
        value["id"] = id_arr[index]
        if(value == data_back):
            validate = True
        else:
            validate = False

        if validate == False:
            print("Data Failed Validation")
            return False
    print("All Data Validated Successfully")
    return True





# Example usage:
api_url = "http://ec2-54-254-162-245.ap-southeast-1.compute.amazonaws.com:9000/items/"

jdata = [
{"title": "For ‘frictionless credit’, RBI to tech platform 'Unified Lending Interface': Governor", "link": "https://indianexpress.com/article/business/ai-loan-sanctioning-rbi-governor-das-9534032/", "date_time": "27082024"},
{"title": "Gas demand uptick driven by power sector bumps up India’s LNG imports in April-July", "link": "https://indianexpress.com/article/business/commodities/gas-demand-uptick-driven-by-power-sector-bumps-up-indias-lng-imports-in-april-july-9534613/", "date_time": "27082024"},
{"title": "To catch the IPO boom, law firms race to scale up capital markets practices", "link": "https://indianexpress.com/article/business/economy/to-catch-the-ipo-boom-law-firms-race-to-scale-up-capital-markets-practices-9534631/", "date_time": "27082024"}
]

validate_url = "http://ec2-54-254-162-245.ap-southeast-1.compute.amazonaws.com:9000/items/"
#id_arr = push_data_to_api(api_url, jdata)
#validate_data_to_api(validate_url, jdata, id_arr)