# Sendbird Random User Generator
Simple python script for creating random users into a Sendbird application using Sendbird's [Platform API](https://docs.sendbird.com/platform) and the [Random User Generator](https://randomuser.me) by [Aaron Hunt](https://twitter.com/arronhunt) and [Keith Armstrong](https://twitter.com/solewolf1993)

## Requirements
- A valid [Sendbird account](https://dashboard.sendbird.com/auth/signup)
- A Sendbird application with an Application ID

## Features
- Saves Sendbird Application id and token to an .env file for faster re-runs

## Usage
From terminal run: `python3 random_users.py`

## Options
| Flag | Description                                                                                                                                  | Argument Type | Default |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------- |
| c    | How many randomly generated users do you want                                                                                                | number        | 2       |
| n    | Nationalities of users. Available options: AU, BR, CA, CH, DE, DK, ES, FI, FR, GB, IE, IR, NO, NL, NZ, TR, US - which can be comma separated | String        | US      |