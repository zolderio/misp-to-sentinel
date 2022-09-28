# Misp to Sentinel
This code can be used to create a Azure Function that writes threat intelligence from a MISP instance to Azure Sentinel. The code is a modified version of the following repository: https://github.com/microsoftgraph/security-api-solutions/tree/master/Samples/MISP

## Installation
1) Create a App in the Microsoft tenant with the Sentinel instance. The app requires the ThreatIndicators.ReadWrite.OwnedBy (Application type) permission.
2) Create a Keyvault in your Azure subscription
3) Add a new secret with the name "tenants" and the following value (its possible to add multiple Sentinel instances, it will loop all occurences):

```
{"<TENANT_ID_WITH_APP>": {"id": "<APP_ID>", "secret": "APP_SECRET"} }
```

4) Create a Azure Function in your Azure subscription
5) Modify config.py to your needs (misp instance domain, API key, event filter etc). Upload the code to your Azure Function.
6) Add a "New application setting" (env variable) to your Azure Function named "tenants". Create a reference to the key vault previously created

## Usage

If the installation was successful, the MISP data should be written to your Sentinel instance on 00:00 every day. Use the following query to test if the data was written successfully:

```
ThreatIntelligenceIndicator
```

## Examples

The following queries are examples on how to match MISP to Microsoft 365 data.

Identify mails with malicious URL's
```
let TI=ThreatIntelligenceIndicator
| where TimeGenerated > ago (24h)
| summarize by Url;
EmailUrlInfo
| where TimeGenerated > ago (5m)
| where Url in (TI)
| join (EmailEvents) on NetworkMessageId
| join (ThreatIntelligenceIndicator) on Url
| where TimeGenerated2 > ago (24h)
```

Identify mails originating from malicious senders:
```
let TI=ThreatIntelligenceIndicator
| where TimeGenerated > ago (24h)
| where EmailSenderAddress != ""
| summarize by EmailSenderAddress;
EmailEvents
| where TimeGenerated > ago (5m)
| where SenderFromAddress in (TI)
| where EmailDirection == "Inbound"
| join (ThreatIntelligenceIndicator) on $left.SenderFromAddress == $right.EmailSenderAddress
| where TimeGenerated1 > ago (24h)
```

Identify mails with malicious attachmenets:
```
let TI=ThreatIntelligenceIndicator
| where FileHashType == "SHA256"
| where TimeGenerated > ago (24h)
| summarize by FileHashValue;
EmailAttachmentInfo
| where TimeGenerated > ago (5m)
| where SHA256 in (TI)
| join (EmailEvents) on NetworkMessageId
| join (ThreatIntelligenceIndicator) on $left.SHA256 == $right.FileHashValue
| where TimeGenerated2 > ago (24h)
```

Identify Office activity from a malcious IP
```
let TI=ThreatIntelligenceIndicator
| where TimeGenerated > ago (24h)
| where NetworkSourceIP != ""
| summarize by NetworkSourceIP;
OfficeActivity
| where TimeGenerated > ago (5m)
| where ClientIP in (TI)
```