EXTENSIONS = [ "bat", "cginc", "compute", "cpp", "cs", "groovy", "h", "js", "lua", "py", "shader"]

import json, os, re, urllib.error, urllib.request

def EscapeMarkdown(str):
    return str.re

def incoming(ui, repo, node, **kwargs):
    ctx = repo[node]

    pattern = r"\.(?:" + "|".join(EXTENSIONS) + ")$"
    if not any(re.search(pattern, i) != None for i in ctx.files()):
        return

    try:
        secretsPath = os.path.dirname(os.path.abspath(__file__)) + "/secrets.txt";
        secrets = json.load(open(secretsPath))
    except (IOError, ValueError) as ex:
        ui.write("Discord incoming hook could not load secrets because " + str(ex))
        return

    shortId = ctx.hex()[:12]

    embed = {
        "url": secrets["hgwebUrl"] + "rev/" + shortId,
        "fields": [
            { "name": "Branch", "value": ctx.branch(), "inline": True },
            { "name": "Author", "value": ctx.user(), "inline": True },
            { "name": "Node", "value": shortId, "inline": True }
        ]
    }

    description = ctx.description().strip()
    lineBreak = description.find("\n")
    if lineBreak >= 0:
        title = description[:lineBreak].strip()
        description = description[lineBreak:].strip()
    else:
        title = description
        description = None

    if title:
        embed["title"] = title
    if description:
        embed["description"] = description

    request = urllib.request.Request(secrets["webhookUrl"],
        json.dumps({ "embeds": [embed] }).encode("utf-8"),
        { "Content-Type": "application/json", "User-Agent": "Mercurial/4.0" })

    try:
        urllib.request.urlopen(request)
    except urllib.error.URLError as ex:
        ui.write("Discord incoming hook web request failed because " + str(ex))
        return