import argparse
import csv
import requests

base_url = 'https://asm.cloud.tenable.com'
api_key = ''


def bad_response_handler(response):
    if response.status_code != 200:
        print('ERROR: ' + response.text)
        quit()

# Receive inventory id from user
arg_parser = argparse.ArgumentParser(
    description='This script creates a CSV report containing all assets in a specified inventory and appends Severity '
                'Breakdown data for each asset.'
)
arg_parser.add_argument(
    '-i',
    '--inventory-id',
    metavar='1234',
    required=True,
    help='Generate a report on this inventory ID',
    type=int,
    dest='inventory_id'
)
inventory_id = arg_parser.parse_args().inventory_id

# Generate API key for inventory
response = requests.get(
    base_url + '/api/1.0/inventories/list',
    headers={
        "accept": "application/json",
        "Authorization": api_key
    },
)
bad_response_handler(response)
inventories = response.json()['list']
inventory_api_key = ''
for inventory in inventories:
    if inventory['inventory_id'] == inventory_id:
        inventory_api_key = inventory['api_key']

# Export inventory as CSV
# Create a list of dictionaries
print('Exporting inventory data as a CSV...')
response = requests.post(
    base_url + '/api/1.0/assets/export/csv',
    headers={
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": inventory_api_key
    },
    json={
        "filters":
            [],
        "columns":
            [
                "id",
                "bd.severity_ranking",
                "bd.hostname",
                "bd.ip_address",
                "ports.ports",
                "ports.services",
                "screenshot.finalurl",
                "ssl.valid_to",
                "rbls.rbls",
                "ipgeo.asn",
                "ipgeo.asn_number",
                "wtech.Hosting",
                "domaininfo.administrativecontact_name",
                "domaininfo.administrativecontact_email"
            ]
    }
)
bad_response_handler(response)
export_token = response.json()['token']

csv_export_data = requests.post(
    base_url + '/api/1.0/export/download',
    headers={
        "Accept": "application/octet-stream",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": inventory_api_key
    },
    data='token=' + export_token
)
bad_response_handler(csv_export_data)
assets = list(csv.DictReader(csv_export_data.text.splitlines()))
asset_count = len(assets)
print('Found ' + str(asset_count) + ' assets.')

# Iterate through CSV
# If severity != none then pull the Severity Breakdown data
# Append Severity Breakdown to each asset
asset_counter = 0
for asset in assets:
    asset_counter += 1
    if asset_counter != asset_count:
        print('Appending Severity Breakdown data for asset ' + str(asset_counter) + '/' + str(asset_count) + '...', end='\r')
    else:
        print('Appending Severity Breakdown data for asset ' + str(asset_counter) + '/' + str(asset_count) + '...')
    if asset['Severity'] != 'none':
        response = requests.get(
            base_url + '/api/1.0/asset/' + asset['id'] + '/severity-breakdown',
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": inventory_api_key
            }
        )
        bad_response_handler(response)
        asset['Severity breakdown'] = str(response.json()['severity_breakdown'])
    else:
        asset['Severity breakdown'] = ''

# Write CSV report to disk
report_name = 'inventory-id-' + str(inventory_id) + '-report.csv'
with open(report_name, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=assets[0].keys())
    writer.writeheader()
    writer.writerows(assets)
print('Created file ' + report_name + '.')

print('Process complete.')
