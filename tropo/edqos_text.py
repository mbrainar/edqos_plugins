import requests

app_url = "http://edqos-dev.apps.imapex.io"

def get_policy_tags():
    r = requests.get(app_url+"/api/policy_tags/")
    if r.status_code == 200:
        return r.json()
    
def get_applications(search):
    if not search:
        return "Missing search string"
    else:
        r = requests.get(app_url+"/api/applications/?search="+search)
        if r.status_code == 200:
            return r.json()

def get_relevance(app_name, policy_scope):
    if not app_name:
        return "Missing search string"
    elif not policy_scope:
        return "Missing policy tag"
    else:
        r = requests.get(app_url+"/api/relevance/?app="+app_name+"&policy="+policy_scope)
        if r.status_code == 200:
            return r.text

# Welcome message
print("Welcome to the Event Driven QoS Tropo Plugin")
# say("Welcome to the Event Driven QoS Tropo Plugin")

# Get policy tags
policy_tags = get_policy_tags()

# Create string of policy tags
policy_string = ', '.join(policy_tags)

while True:
    # Ask what policy tag to use
    policy_scope = input("What Policy Tag should we use? Chose: "+policy_string)
    # policy_scope = ask("What Policy Tag should we use? Chose: "+policy_string, {
    #     "choices":policy_string})

    if policy_scope not in policy_tags:
        print("Policy scope provided is not valid")
        # say("Policy scope provided is not valid")
    else:
        break


# Ask for application search string
app_search = input("What application do you wish to modify?")

app_names = get_applications(app_search)
if len(app_names) == 1:
    print("{} is currently listed as {}".format(app_names[0], get_relevance(app_names[0], policy_scope)))
    # say("{} is currently listed as {}".format(app_names[0], get_relevance(app_names[0], policy_scope)))
else:
    app_string = ', '.join(app_names)

