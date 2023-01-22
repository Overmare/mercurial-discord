import json, os, urllib.error, urllib.request
from mercurial import util

def EscapeMarkdown(str):
    return str # TODO

def incoming(ui, repo, node, **kwargs):
    ctx = repo[node]

    try:
        secretsPath = os.path.dirname(os.path.abspath(__file__)) + "/secrets.txt";
        secrets = json.load(open(secretsPath))
    except (IOError, ValueError) as ex:
        ui.write(("Discord incoming hook could not load secrets because " + str(ex) + "\n").encode("utf-8"))
        return

    shortId = ctx.hex()[:12].decode("utf-8")

    embed = {
        "url": secrets["hgwebUrl"] + "rev/" + shortId,
        "fields": [
            { "name": "Branch", "value": ctx.branch().decode("utf-8"), "inline": True },
            { "name": "Author", "value": ctx.user().decode("utf-8"), "inline": True },
            { "name": "Node", "value": shortId, "inline": True }
        ]
    }

    description = ctx.description().strip()
    lineBreak = description.find(b"\n")
    if lineBreak >= 0:
        title = description[:lineBreak].strip()
        description = description[lineBreak:].strip()
    else:
        title = description
        description = None

    if title:
        embed["title"] = title.decode("utf-8")
    if description:
        embed["description"] = description.decode("utf-8")

    request = urllib.request.Request(secrets["webhookUrl"],
        json.dumps({ "embeds": [embed] }).encode("utf-8"),
        { "Content-Type": "application/json", "User-Agent": "Mercurial/" + util.version().decode("utf-8") })

    try:
        urllib.request.urlopen(request)
    except urllib.error.URLError as ex:
        ui.write(("Discord incoming hook web request failed because " + str(ex) + "\n").encode("utf-8"))
        return