# eTrf-Simplii
Python script to send Interac eTransfers programmatically via Simplii's website, and saves a screenshot of the confirmation to the user's hard drive.

## :credit_card: Usage

You must have a Simplii account for this to work. I may write versions for other bank websites in the future.

Make sure to customize the desired file path to save the screenshot (line 104).

Customize the required arguments to pass to eTrf function (line 117), then run the script.

## :snake: Dependencies

Must have Firefox browser installed.

This script uses selenium (geckodriver), as well as the following Python modules:  os, pyautogui, sys, datetime.
