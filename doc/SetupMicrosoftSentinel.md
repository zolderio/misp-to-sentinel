# Setting up Microsoft Sentinel
To activate Microsoft Sentinel, an Azure Subscription is required in the applicable Microsoft 'tenant'. The subscription in itself will be free of charge, but configures if and how any payed Azure services may be incured. It is possible to activate a new subscription in test/trial mode to test a particular setup for a Month.

## Activating Sentinel
When the Subcription is available, Sentinel can be activated:
1. Go to https://portal.azure.com
2. Find the service "Microsoft Sentinel"
3. Click Create to generate a new Sentinel instance
4. Click Create a new workspace. A workspace serves to process logging within Azure. Connect the workspace to the appropriate Subscription. Create a new resource group, give the workspace a name (e.g. "Sentinel") and choose the region for the workspace (e.g. "West Europe")
5. After creation, select the new Workspace and click Add to create the Sentinel instance and open it

## Free Log Sources
Attention: only the below mentioned Data Types within said Data Connectors can be onboarded into Sentinel free of charge ([Source](https://docs.microsoft.com/en-us/azure/sentinel/billing?tabs=commitment-tier#free-data-sources)). This does not apply to any other Data Types.

| Data Connector | "Free" Data Type |
|:---------------|:-----------------|
| Azure Activity Logs | AzureActivity |
| Azure AD Idenity Protection | SecurityAlert (IPC) |
| Office 365 | OfficeActivity (SharePoint) |
| | OfficeActivity (Exchange) | 
| | OfficeActivity (Teams) |
| Microsoft Defender for Cloud | SecurityAlert (Defender for Cloud) |
| Microsoft Defender for IoT | SecurityAlert (Defender for IoT) |
| Microsoft 365 Defender | SecurityIncident |
| | SecurityAlert |
| Microsoft Defender for Endpoint | SecurityAlert (MDATP) |
| Microsoft Defender for Identity | SecurityAlert (AATP) |
| Microsoft Defender for Cloud Apps | SecurityAlert (Defender for Cloud Apps) |

## Payed Log Sources
Besides the free-of-charge log sources, it is possible to onboard all kinds of other log sources into Sentinel, also non-Microsoft ones, through which it might even serve as a full-blown SIEM. And just like with all SIEMs: more logs means more cost. Within the Microsoft realm, such additional cost might first of all orginate from required licens upgrades to unlock certain features. Besides that Microsoft will incure cost for storage of logs, quite similar to any SIEM.

Which log sources contain relevant data, really depends on the organisation AND in our set-up: the available threat information in the connected MISP server. And especially because of the extra cost that might arise from onboarding: first have a clear understanding of what data needs to be matcht or what other purpose a particular log source has, and do not connect log sources you don't really need.

| Data Connector | Data Type | Provides us with |
|:---------------|:----------|:-----------------|
| Azure Active Directory | SignInLogs | All login attempts into AzureAD, both human as programmatically, are logged including the IP-address from which it happens. Matching those IP-addresses to the CTI coming from MISP, provides exactly the alarms one envisions when connecting MISP to Microsoft365 |
| Microsoft 365 Defender | EmailUrlInfo, EmailEvents, EmailAttachmentInfo | Extra data types within the Microsoft 365 Defender connector, allowing us to match all relevant data coming from Exchange with the CTI from MISP. <ul><li>*EmailUrlInfo* > URLs that are part of the body of e-mails can be matched to known malicious websites.</li><li>*EmailEvents* > Emailaddress, Emaildomain, IP-address of sender, Subject all are datapoints that are logged in this data type and can be matched to CTI coming from the MISP source</li><li>*EmailAttachmentInfo* > Filenames and SHA256 filehashes of email attachments can be matched to known malware or otherwise malicious files</li></ul> |

## Connecting Log Sources
Log sources can be added to Microsoft Sentinel as follows:

1. Open Microsoft Sentinel
2. Go to Data Connectors
3. Add log sources that you deem relevant from above lists. Recommended are at least the 3 OfficeActivity logs, as they contain data (IP-addresses) that can easily be correlated to any MISP source

## Checking Data Coming In
After activating data connecters, it might take some time for data to actually flow into Sentinel. You may check data coming in, by:

1. Open Microsoft Sentinel
2. Go to Logs
3. Close the first popup bringing you to the Query screen
4. As a query, type: ```OfficeActivity```
5. Hit Run
6. If results are shown, the connector is working. Repoeat these steps for other connected log sources

