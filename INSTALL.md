# Step-by-Step Azure Function Setup
This step-by-step instruction guides you through the process of setting up a complete Azure Function that will acquire Threat Intelligence from a MISP source, sanitize it, than writes it to 1 or multiple Microsoft Sentinel instances.

The complete setup consists of several Azure components:

1. **App Registration** - This app will get the permissions to write data to the ThreatIndicatores table of Sentinel
2. **Keyvault** - contains the keys to automatically authenticate with the app registration
3. **Function** - contains the scripts to retrieve information from a MISP source in interval, rewrite it to useful data and than place it in Sentinel through the app registration
4. **NAT Gateway** - Optional component allowing the Azure Function to connect to MISP from a fixed IP-address, allowing it to be added to an access control list that might be protecting the MISP server

## Prerequisities
- An Azure Subscription 
- A Microsoft Sentinel Instance (see [/doc/SetupMicrosoftSentinel.md](/doc/SetupMicrosoftSentinel.md))
- API and URL of your MISP instance

## App Registration
This is how to create and configure the app registration:

1. Open Azure via https://portal.azure.com
2. Go to the service App Registrations
3. Make a new registration
4. Give the new app a descriptive name, for instance: *misp2sentinel*. Other settings can be left to default values.
5. Click ofter creating the app registration in the overview page under CLient credentials on *add a certificate or secret*
6. Click under Client secrets on *New client secret*
7. Give a description, for instance *M2S Azure Function* and leave the recommeded expiry value
8. Copy the value of the new Client Secret, which need to be stored in an Azure Vault

## Formatting the Secret value
From above App Registration, 3 elements are required to store in Keyvault a value in the correct format to make the script able to properly make use of the app.

- **TENANT_ID** = the value stated at _Directory (tenant) ID_ in the App Registration overview
- **APP_ID** = the value stated at _Application (client) ID_ in the App Registration overview
- **APP_SECRET** = the value you copied in the last step in creating the App Registration

The combined value that should be stored in the Keyvault, is as follows, where the variable names including the <> should be replaced by above 3 values.

```
{"<TENANT_ID>": {"id": "<APP_ID>", "secret": "<APP_SECRET>"}}
```

The format of the key value makes it possible for the Azure Function to write Threat Intel data to multiple Sentinel instances. This is useful for instance if there is a testing environment, or for any other reason multiple Sentinel instances exist.

## Keyvault
This is how to create a Key Vault and store the secret value in it:

1. Go to the service *Key vaults*
2. Click *Create key vault*
3. Configure the Key vault as you wish, pay attention to the region in which it is stored, for instance "West Europe"
4. After creating the Key vault, under Objects click Keys and create a new key
5. Enter the values that were copied from App Registration Secrets above
- the name of the key **MUST** be "tenants"
- The *Secret Value* will be the formatted secret value you created above
- Other settings can be left to default values

## Function
This is how the create the Azure Function:

1. Go to the service *Function App*
2. Click *Create* to generate a new Azure Function
- Give the function a descriptive name
- Choose at Publish for *Code*, and *Python* as the Runtime Stack. Again pay attention to the Region ("West Europe")
- OS can remain Linux
- At plan type choose *App service plan*
- Other settings can be left to default values. Click *Review + Create*

## Function Code
This is how to place the code into the Function:

1. Download all files from directory [/m2s](/m2s) in this repo
2. Open **config.py** in your text editor and insert these values:
- **misp_key** = the API key that you have obtained from the MISP web portal in the preparation
- **misp_domain** = the URL of the MISP server 
3. In the Azure Function go to *Functions* and click *Create*
4. As the template choose *Time trigger*
- Choose a name for your function, for instance "m2s"
- Enter a schedule based on [CRON-syntax](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=in-process&pivots=programming-language-csharp#ncrontab-expressions). For instance to make it run daily at 0:00 o'clock: ```0 0 0 * * *```
- Click *Create*
5. In the new function go to *Code + Test*
6. Upload the Function code 

## Extra Setup for Fixed IP
Some MISP servers maybe protected by an access control list, making it only accessible from certain listed IP-addresses. In such cases it may be necessary for the Azure Function to be configured to connect to MISP from a fixed IP address. This is possible by making the Function to run through an Azure NAT Gateway. How to do this, has been inspired by [this description from Microsoft](https://learn.microsoft.com/en-us/azure/azure-functions/functions-how-to-use-nat-gateway), and goes as follows:

### Virtual Network
1. Go to the service *Virtual Networks*
2. Click *Create*
- Connect the network to the same resource group as the Azure Function
- Give a name to your network, for instance "m2s-vnet", and again pay attention to the region ("West Europe")
- The rest of the settings can be left to default values
3. Open the Azure Function and go to *Networking*
4. At Outbound Traffic click *VNet Integration*
5. Click *Add VNet*
- Select the just created Virtual Network and the *default* subnet, than click *Create*

### Public IP
1. Go to the service *Public IP Addresses*
2. Click *Create*
- Choose a name for the IP-address, for instance "m2s-publicip"
- Connect the IP-address to the same resource group as the Azure Function
- The rest of the settings can be left to default values
3. Under *Overview* the reseved IP-address can be found, save it to be send to the administrator of the MISP access control list later on

### NAT Gateway
1. Go to the service *NAT gateways*
2. Click *Create*
- Connect the NAT gateway to the same resource group as the Azure Function
- Give a name to the NAT gateway, for instance "mws-nat", and pay attention to the region ("West Europe")
- Go to the next step: *Outbound IP*
- Select the Public IP Address from previous step. Leave Public IP prefixes unchecked.
- Go to the next step: *Subnet*
- Select the Virtual Network from previous step
- Choose *default* as subnect
- Go to *Review + Create* and click *Create*
3. Open the Azure Function
4. Verify under Networking that at *Outbound Network Features* the NAT Gateway now is enabled. Now we only need to reroute all the traffic through the gateway
5. In the left-hand menu go to Configuration
6. Under *Application Settings* click *New application setting*
- **Name** = ```WEBSITE_VNET_ROUTE_ALL```
- **Value** = ```1```
- Click *OK*
7. Click *Save* to save the configuration

### Access Control List
Send the IP-address you copied earlier to the administrator of the MISP access control list, and wait for their confirmation.

## Validation
Once all above steps are completed, the Azure Function will retrieve data next time it turns 0:00 o'clock (or at the time you have scheduled your function to run). In the morning afterwards, this can be validated in Sentinel.

1. Go to the service *Microsoft Sentinel*
2. At the left-hand side click *Threat Intelligence*
3. You should now get a list of thousands threat indicators, with *SecurityGraph* as the source