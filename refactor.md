# Refactorinng Plan
Our goal is to entirely rewrite this web application. The web application is used at a small restaurant to cash up at the end of a shift Therefore it is important that the calculations we make here are correct and stay the same. However the app is terribly outdated in a technical way so we will change all this and introduce a nice architecture.
Specifically we do not want to be backwards compatible in terms of code. That means you can remove and delete the terrible code we have here and replace it with a nice version. Once again the only thing that is important is that the outcome of the calculation is the same AND that we don not change the look of the UI.

## Stage 0: Change the text stack 
We want to get rid of flask and use fast API instead. We do need a duplicate environment setup using the pixi.toml for local development and the requirements.txt for deployment. We're deploying to Google Cloud App Engine, which has a hardware client for the requirements.txt. Just ensure that they're in sync so I can use my nice Pixi environment locally 

## Stage 1: Modulatization and Typing
First of all we need to modularize the application and type everything strictly. That means no longer any dictionaries that fly around; we now use Pydantic models for everything. In the same vein we'll break up the calculation into functions, one for each calculation, and then these functions receive pydantic models as input and should be tested using individual unit tests. We'll also use Pydantic models to validate the user input. Note that we still want to allow the fuzzy inputs so the input parsing should be as lenient as it is now but we should put this in a separate module 

## Stage 2: writing a good test suite 
Next we want to write an exhaustive test using unit tests, especially concerning the calculations in particular.

## Stage 3: Removing hard codes 
There are a lot of constants in this code base that are hard coded. Pull all configuration, like the list of employee names, into a YAML file that is loaded from the code base. As a separate issue I observe that there are a lot of string mappings that map internal names to UI displayed names. Please remove that pattern and replace it with something nicer. I still want to explicitly be able to set what the UI displays but just come up with a suggestion for a better architecture than using a dictionary as a mapping between internal and external strings. These are actually different layers of our application 

# Constraints
1. Do not overcomplicate the design. The application is currently a single file. While I do need strict typing, a config file, and a bit more separation between UI and logic for testing purposes, I do not want you to write a fully architected web app with DTOs and many different layers spread across tens of files. I want to keep this application simple such that it allows me to make targeted changes to the future 
2. For now keep the UI exactly the same
