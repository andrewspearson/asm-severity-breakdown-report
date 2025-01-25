# asm-severity-breakdown-report
Creates a report from Tenable ASM that contains all assets in a specified inventory and appends Severity Breakdown information. Report is in CSV format.
## Requirements
* python3
## Configuration
* Make sure your Tenable ASM user account has [access to the inventories](https://docs.tenable.com/attack-surface-management/Content/Topics/AdministratorUI/EditInventoryDetails.htm) you want to report on.
* [Generate a Tenable ASM API key for all your inventories](https://docs.tenable.com/attack-surface-management/Content/Topics/UserProfile/GenerateAPIKeys.htm). Copy the API key and paste it in as the [value in line 6](https://github.com/andrewspearson/asm-severity-breakdown-report/blob/fd79cb3c080d2e65f41093fcf742f38ca52a506f/asm-severity-breakdown-report.py#L6).
## Usage
View the help menu
```
$ python3 asm-severity-breakdown-report.py -h
usage: asm-severity-breakdown-report.py [-h] -i 1234

This script creates a CSV report containing all assets in a specified inventory and appends Severity Breakdown data for each asset.

options:
  -h, --help            show this help message and exit
  -i 1234, --inventory-id 1234
                        Generate a report on this inventory ID
```
Run the script
```
$ python3 asm-severity-breakdown-report.py -i 9470
Exporting inventory data as a CSV...
Found 352 assets.
Appending Severity Breakdown for asset 352/352...
Created file inventory-id-9470-report.csv.
Process complete.
```
