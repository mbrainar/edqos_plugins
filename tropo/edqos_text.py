import requests
import urllib.request
import urllib.parse
import sys
import json

app_url = "http://edqos-dev.apps.imapex.io"

def get_policy_tags():
    with urllib.request.urlopen(app_url+"/api/policy_tags/") as r:
        response = r.read()
        encoding = r.info().get_content_charset('utf-8')
        JSON_object = json.loads(response.decode(encoding))
        return JSON_object

def get_applications(search):
    if not search:
        return "Missing search string"
    else:
        with urllib.request.urlopen(app_url + "/api/applications/?search="+search) as r:
            response = r.read()
            encoding = r.info().get_content_charset('utf-8')
            JSON_object = json.loads(response.decode(encoding))
            return JSON_object

def get_relevance(app_name, policy_scope):
    if not app_name:
        return "Missing search string"
    elif not policy_scope:
        return "Missing policy tag"
    else:
        with urllib.request.urlopen(app_url + "/api/relevance/?app="+app_name+"&policy="+policy_scope) as r:
            response = r.read()
            encoding = r.info().get_content_charset('utf-8')
            JSON_object = json.loads(response.decode(encoding))
            return JSON_object

def set_relevance(app_name, policy_scope, target_relevance):
    valid_relevance = ["Business-Relevant", "Default", "Business-Irrelevant"]
    if not app_name:
        return "Missing search string"
    elif not policy_scope:
        return "Missing policy tag"
    elif target_relevance not in valid_relevance:
        return "Invalid or missing target relevance"
    else:
        data = urllib.parse.urlencode({'app': app_name, 'policy': policy_scope, 'relevance': target_relevance})
        data = data.encode('ascii')
        with urllib.request.urlopen(app_url+"/api/relevance/", data) as r:
            response = r.read()
            encoding = r.info().get_content_charset('utf-8')
            JSON_object = json.loads(response.decode(encoding))
            return JSON_object


def main():
    # Welcome message
    print("Welcome to the Event Driven QoS Tropo Plugin")
    # say("Welcome to the Event Driven QoS Tropo Plugin")

    # Get policy tags
    policy_tags = get_policy_tags()
    if not policy_tags:
        sys.exit("Unable to get policy tags")
    elif len(policy_tags) == 0:
        sys.exit("No policy tags defined in APIC EM")

    # Create string of policy tags
    policy_string = ', '.join(policy_tags)

    while True:
        # Ask what policy tag to use
        policy_scope = input("What Policy Tag should we use? Chose: "+policy_string)
        # policy_scope = ask("What Policy Tag should we use? Chose: "+policy_string, {
        #                    "choices":policy_string,
        #                    "timeout":30.0})

        if policy_scope not in policy_tags:
            print("Policy scope provided is not valid")
            # say("Policy scope provided is not valid")
        else:
            break

    # Ask for application search string
    app_search = input("What application do you wish to modify?")
    # todo Can ask() support open-ended SMS responses?
    # app_search = ask("What application do you wish to modify?", {
    #                  "choices":"[ANY]",
    #                  "timeout":30.0})

    app_names = get_applications(app_search)
    if len(app_names) == 1:
        app_name = app_names[0]
    elif len(app_names) > 1:
        app_string = ', '.join(app_names)
        while True:
            app_name = input("Multiple applications matched your search. Which app would you like to modify? Chose: "+app_string)
            # app_name = ask("Multiple applications matched your search. Which app would you like to modify? Chose: " + app_string, {
            #                "choices":app_string
            #                "timeout":30.0})

            if app_name not in app_names:
                print("Application name is not valid")
                # say("Application name is not valid")
            else:
                break
    else:
        print("Sorry, no applications matched your search")
        # say("Sorry, no applications matched your search")
        sys.exit("No applications matched search")

    # Print current relevance
    print("{} is currently listed as {}".format(app_name, get_relevance(app_name, policy_scope)))
    # say("{} is currently listed as {}".format(app_name, get_relevance(app_name, policy_scope)))

    # Ask what relevance we want to set
    valid_relevance = ["Business-Relevant", "Default", "Business-Irrelevant"]
    relevance_string = ', '.join(valid_relevance)
    while True:
        target_relevance = input("What relevance would you like to set? Chose: " + relevance_string)
        # target_relevance = ask("What relevance would you like to set? Chose: "+relevance_string, {
        #                        "choices":relevance_string,
        #                        "timeout":30.0})
        if target_relevance not in valid_relevance:
            print("Sorry, specified relevance level is not valid")
            # say("Sorry, specified relevance level is not valid")
        else:
            break

    # Reset relevance
    relevance_task = set_relevance(app_name, policy_scope, target_relevance)
    if relevance_task:
        print("Policy change was successful. {} is now set to {}".format(app_name, target_relevance))
        # say("Policy change was successful. {} is now set to {}".format(app_name, target_relevance))
    else:
        print("Sorry, there was a problem changing the policy.")
        # say("Sorry, there was a problem changing the policy.")


if __name__ == '__main__':
    sys.exit(main())
    #hangup()