# MISP to Microsoft Sentinel
This code can be used to create an Azure Function that writes threat intelligence from a MISP instance to Microsoft Sentinel. The code is a modified version of the following repository: https://github.com/microsoftgraph/security-api-solutions/tree/master/Samples/MISP

## Installation
### Prerequisities
- An Azure Subscription 
- A Microsoft Sentinel Instance (see [/doc/SetupMicrosoftSentinel.md](/doc/SetupMicrosoftSentinel.md))
- API and URL of your MISP instance

### Summary
In summary:
1) Create an App in the same Microsoft tenant where the Sentinel instance resides. The app requires the *ThreatIndicators.ReadWrite.OwnedBy* (Application type) permission.
2) Create a Keyvault in your Azure subscription
3) Add a new secret with the name "tenants" and the following value (its possible to add multiple Sentinel instances, it will loop all occurences):

```
{"<TENANT_ID_WITH_APP>": {"id": "<APP_ID>", "secret": "APP_SECRET"} }
```

4) Create an Azure Function in your Azure subscription
5) Modify config.py to your needs (misp instance domain, API key, event filter etc). Upload the code to your Azure Function.
6) Add a "New application setting" (env variable) to your Azure Function named "tenants". Create a reference to the key vault previously created

Full instruction in [INSTALL.md](INSTALL.md)

## Usage

If the installation was successful, the MISP data should be written to your Sentinel instance on 00:00 every day. Use the following query to test if the data was written successfully:

```
ThreatIntelligenceIndicator
```

## Examples
Find examples of KQL queries and Azure Playbooks in [/doc/ExampleKQLandPlaybooks.md](/doc/ExampleKQLandPlaybooks.md)