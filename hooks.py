import json, urllib2

def incoming(ui, repo, node, **kwargs):
    ctx = repo[node]
    if any(i[-3:] == ".cs" for i in ctx.files()) == False:
        return

    secrets = json.load(open("secrets.txt"))

    jsonObj = {
        "embeds": [
            {
                "title": "Someone, please review this change",
                "description": ctx.description(),
                "url": secrets["hgwebUrl"] + "rev/" + ctx.hex()[:12]
            }
        ]
    }

    request = urllib2.Request(secrets["webhookUrl"],
        json.dumps(jsonObj), { "Content-Type": "application/json", "User-Agent": "Mercurial/5.0.2" })
    urllib2.urlopen(request)
