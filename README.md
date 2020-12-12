# eTrf-Simplii
Python script to send Interac eTransfers programmatically via Simplii's website.

## :credit_card: Usage

You must have a Simplii account for this to work. I may write versions for other bank websites in the future.

The script ends before programmatically pressing the last Confirm button. This is to allow the user to check that everything was entered correctly and then confirm manually.

Uncommenting lines 78 to 84 would make this fully automatic.

Uncommenting lines 85 to 87 would exit the browser afterwards.

## :snake: Dependencies

This script uses selenium webdriver, as well as the following Python modules:  os, pyautogui, sys, datetime
