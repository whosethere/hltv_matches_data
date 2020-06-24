def get_matchid_from_link(link):
    link = str(link)
    link = link.split("/")
    _id = link[4]
    _id = int(_id)
    return _id