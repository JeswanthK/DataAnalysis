

"""
    Title:  FCA Competitive Messaging
    Class:  CSC 4996 Senior Project, Wayne State University
    Date:   November 25, 2019

"""


# Python Libraries
# -------------------------------------------------
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from datetime import date
import sys


sys.path.append('../')


# .env file for PATH to get the data location
# -------------------------------------------------
from common.path_to_use import *


# Function used to send the email to the end-user after alerts have been found.
# Parameters:
# @alert_values, dataType = Data Frame,
#   Data frame of all alerts for a specific type.
# @alert_type, dataType = String,
#   Type of alerts sent (I.E. OEM, Endemic, Dealer, etc.)
def send_email(alert_values, alert_type):
    # Used to initiate the connection to the smtp server to send emails online.
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(get_email(), get_email_password())

    # Used to receive values of users, emails, and regions for sending the correct emails to the correct users.
    email_df = pd.read_csv(getRegionalEmailLists())
    region_list = get_region_list(email_df)

    # Iterates through each region to ensure all regions are covered.
    for region in region_list:
        # Gathers only alerts from a specific region and formats them for readability
        region_alerts = get_region_df(alert_values, region)
        region_alerts = format_df(region_alerts)

        # If the data frame is not empty it should begin sending the email.
        # It will gather a list of all relevant end-users, emails, and create the regional message.
        if not region_alerts.empty:
            region_df = get_region_df(email_df, region)
            user_list = region_df['User'].tolist()
            email_list = region_df['Email'].tolist()
            message = get_message(region_alerts, alert_type)

            # Used to iterate through each user's name and email to send them the Email.
            for user_name, user_email in zip(user_list, email_list):
                msg = MIMEMultipart()
                msg['From'] = getEmail()
                msg['To'] = user_email
                msg['Subject'] = alert_type + ' Alerts for ' + region + ' on ' + str(date.today())

                msg.attach(MIMEText('Hello ' + user_name + ',\n\n' + message, 'plain'))

                s.send_message(msg)
                del msg
    # The connection to the smtp server for sending emails is closed.
    s.quit()


# Returns the email specified in the .env file to send the alerts from.
def get_email():
    return getEmail()


# Returns the email password specified in the .env file to send the alerts from.
def get_email_password():
    return getEmailPassword()


# Returns a data frame with alert values only within a single Region/Business Center.
# This will be used to separate values from different regions.
def get_region_df(region_df, region):
    return region_df[region_df['Business Center'].str.match(region, na=False)]


# Returns the list of Business Centers that there is a Representative for.
# These values are found within the regionUserList.CSV file.
def get_region_list(region_df):
    return region_df['Business Center'].unique().tolist()


# Returns the message (body) to be sent within the email with all alerts for the region
# Concatenated in the form of a String.
def get_message(df, alert_type):
    message_string = 'The following are the alerts for ' + alert_type + ' offers only. \n\n'
    message_string += 'Sent on: ' + str(date.today()) + '\n\n\n'
    columns = list(df.columns.values.tolist())
    alert_count = 1

    # Iterates through the data frame row by row to receive all values to send to each user
    # in the form of a String.
    for index, row in df.iterrows():
        message_string += '**************************************************\n'
        message_string += ('Alert #' + str(alert_count) + '\n')
        alert_count += 1

        # Iterates through each column and checks the value of the row.
        # If it is null it will not output the column/row value(s).
        # Outputs the field in the form of Column: Row Value
        for column in columns:
            if pd.notnull(row[column]):
                row_value = modify_row_values(row[column], column)
                message_string += (get_col_str(column) + ': ' + row_value + '\n')
    message_string += '**************************************************\n\n'

    return message_string


# Returns a data frame consisting of only the relevant columns for the user.
# The order is critical here to group them and maintain the flow of the message.
def format_df(df):
    return df[['thresholdsColumns', 'dateCaptured', 'startDate', 'endDate',
               'Zip', 'City', 'State', 'Business Center', 'modelYear', 'brand', 'segment',
               'nameplate', 'trim', 'Group Trim', 'campaignType', 'cashBonus', 'downPayment',
               'recurringPayment', 'apr', 'term', 'downPaymentCurrentLessees', 'msrpPercentOff',
               'securityDeposit', 'disclaimer', 'domain', 'pageUrl', 'imageUrl']]


# Returns a user-friendly representation of the column in the form of a string to be sent in the message.
def get_col_str(col):
    col_dict = {'thresholdsColumns': 'Reason for Alert',
                'dateCaptured': 'Date Captured',
                'Month': 'Month',
                'Week': 'Week of Month',
                'startDate': 'Start Date',
                'endDate': 'End Date',
                'Zip': 'Zip Code',
                'DMACity': 'City',
                'DMAState': 'State',
                'Business Center': 'Business Center',
                'modelYear': 'Model Year',
                'brand': 'Brand',
                'segment': 'Segment',
                'nameplate': 'Nameplate',
                'trim': 'Trim',
                'Group Trim': 'Trim Level',
                'campaignType': 'Campaign Type',
                'cashBonus': 'Cash Bonus',
                'downPayment': 'Down Payment',
                'recurringPayment': 'Recurring Payment',
                'apr': 'APR',
                'term': 'Term',
                'downPaymentCurrentLessees': 'Down Payment For Current Lessees',
                'msrpPercentOff': 'Percent Off MSRP',
                'securityDeposit': 'Security Deposit',
                'disclaimer': 'Disclaimer',
                'domain': 'Website Domain',
                'pageUrl': 'Page URL',
                'imageUrl': 'Image URL'}
    user_value = col_dict.get(col)

    if user_value is not None:
        return user_value
    else:
        return col


# Formats row values to be uniform and readable to the user.
def modify_row_values(row, col):
    if col == 'thresholdsColumns':
        row_val = modify_threshold_reason(row)
    elif col in ('cashBonus', 'Zip', 'downPayment', 'recurringPayment', 'term'):
        row_val = int(row)
    else:
        row_val = row

    # The list contains values that should not be altered.
    if col in ('State', 'disclaimer', 'domain', 'pageUrl', 'imageUrl'):
        return str(row_val)
    # Dates are ensured to be kept at a YYYY-MM-DD format.
    elif col in ('dateCaptured', 'startDate', 'endDate'):
        row_val = str(row_val)
        return str(row_val[:10])
    # Cash value rows are formatted to include commas and $.
    elif col in ('downPayment', 'recurringPayment', 'cashBonus', 'downPaymentCurrentLessees'):
        num = int(row_val)
        return '$' + '{:,}'.format(num)
    else:
        return str(row_val).capitalize()


# Used to modify the alert reason regarding the threshold that was crossed
def modify_threshold_reason(row_val):
    # Makes it more readable to the end user in the email by stripping Dataframe identifiers
    row_val = str(row_val).replace('[', '')
    row_val = str(row_val).replace(']', '')
    row_val = str(row_val).replace('\'', '')

    # Changes name of the type of threshold to give the user insight on the cause
    threshold_dict = {'cashBonusUpper': 'High Cash Bonus',
                      'cashBonusLower': 'Low Cash Bonus',
                      'downPaymentUpper': 'High Down Payment',
                      'downPaymentLower': 'Low Down Payment',
                      'recurringPaymentUpper': 'High Down Payment',
                      'recurringPaymentLower': 'Low Down Payment'}
    user_value = threshold_dict.get(row_val)

    if user_value is not None:
        return user_value
    else:
        return row_val
