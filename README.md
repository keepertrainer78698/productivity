# Automation
I use Airtable as an organization and tabular tool but I am not using it as a File based storage tool. I have chosen the Swiss Cloud solution from Infomaniak *kdrive* for storaging Files. In order to organize my files and do some referencing and calculation I want to automatically upload saved Files to Airtable.

## Prerequisits
* Get a Airtable Account and API Key
* Create a kDrive Account and an API Key
* Add API URI to your config File to each of the automated File Directory and Base in Airtable

## How To
1. Upload File to kDrive Directory
2. Run python class i.e. 
```python
import kdriveairtable as ka
ka.UploadFiles("Invoices").upload_to_airtable()
```
