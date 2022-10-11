# Examples

## Example KQL statements
The following queries are examples on how to match MISP to Microsoft 365 data.

### Identify Office activity from a malicious IP
```
let TI=ThreatIntelligenceIndicator
| where TimeGenerated > ago (24h)
| where NetworkSourceIP != ""
| summarize by NetworkSourceIP;
OfficeActivity
| where TimeGenerated > ago (5m)
| where ClientIP in (TI)
```

### Identify mails with malicious URLs
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

### Identify mails originating from malicious senders
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

### Identify mails with malicious attachments
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

## Sentinel Playbook
Playbooks are automatic workflows Sentinel can initiate followin for instance an alarm. Such a playbook can be quite a complex set of actions, like resetting passwords or disabling accounts. But in it's simplest from a playbook serves to send an email if a rule triggers. In order to correctly configure a Sentinel rule, first a playbook should be created.

1. Open Microsoft Sentinel
2. Under Configuration go to Automation
3. Click Create and choose *Playbook with incident trigger*
4. Give the playbook a name, e.g. 'mail-me'
5. Go to the final step, click Create and continue in the Designer
6. In the Logic App Designer, add a new action. Choose *Office 365 Outlook*, than *Send an email*
7. Now probably a connection needs to be made with a mailbox to be able to send emails on behalf of that mailbox. This mailbox will become the sender of alarmmails, which might be a reason to create a service account or shared mailbox for this purpose
8. Enter the recipient(s) of the alertmail, the Subject and the Body of the mail. In doing so, it is possible to make use of several variables coming from the future incidents. E.g.: ![Send An Email V2](/doc/img/SendAnEmailV2.png)
9. Click Save

This playbook (or Logic App) can now be connected to any Sentinel Rules for which an alarmmail should be send if it triggers.

## Sentinel Rule
Follow these steps to create a new Sentinel (Analytics) Rule:

1. Open Microsoft Sentinel
2. Go to Analytics
3. Click Create and choose *Scheduled query rule*
4. Give the rule a name and go to the next step: *Set rule logic*
5. Write the KQL syntax in the *Rule Query* field
6. Define how often you want the rule to be executed (and possibly generating an alarm)
7. Go to the next step: *Incident settings*
8. Go to the next step: *Automated response*
9. Make a new automation rule by clicking *Add new*
- Give the rule a descriptive name
- At Actions choose *Run Playbook*
- Select the playbook you have created before
- Click Apply
10. Go to the final step: *Review* and click *Create*

## Validation
To validate whether rules and playbooks are working as expected, you might want to created a rule which you can trigger easily. For instance, a rule that triggers when you receive an email with a particular value in the subject.

But as there always should remain something to figure out yourselves, this one we will not write out for you. Good luck ;)