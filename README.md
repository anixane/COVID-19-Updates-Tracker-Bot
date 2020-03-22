# COVID-19 Updates Tracker Bot for India

![Alt text](/Status.png "Optional Title")

## Features
- Sit back and relax - the coronavirus updates will come to you.
- Get Microsoft Teams notifications (picture above)
  -  New Corona Virus cases happening in India
  -  How many Indian nationals have Corona Virus per State?
  -  How many deaths happened per State?
  -  The new States entering the corona zone like Chattisgarh
- Too many updates? Subscribe only to the states that you want.
- Its reliable - the source of data is official Government site ([here](https://mohfw.gov.in/))
- Its ROBUST! 
  - What if script fails? What if the Govt website changes format?
  - You get Teams notifications about the exceptions too.
  - You have log files (check `bot.log`) too, to evaluate what went wrong
- Don't like a feature? Change it! Raise a Pull Request.

## Notification Screenshot when there is a change in count.
![Alt text](/Status_Updated.png "Optional Title")


## Installation
- You need Python
- You need a Microsoft Teams account + Microsoft Teams Webhook to send Teams notifications to your channel
- Install dependencies by running
```bash
pip install tabulate
pip install requests
pip install beautifulsoup4
pip install pymsteams
```
- Clone this repo and create auth.py
```bash
git clone git@github.com:anixane/COVID-19-Updates-Tracker-Bot.git
```
- Write your Teams Webhook into 'DEFAULT_TEAMS_WEBHOOK' variable or import it from external file (recommended).
```python
DEFAULT_TEAMS_WEBHOOK = '<Microsoft Teams Webhook URL>'
```
- Setup the cron job to receive updates whenever something changes
```bash
crontab -e # opens an editor like vim or nano
# now write the following to run the bot every 5 mins
*/5 * * * * cd $PATH_TO_CLONE_DIR; python3 corona_bot.py --states 'haryana,maharashtra'
# to receive updates for all states, ignore the --states flag
```
