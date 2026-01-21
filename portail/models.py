from admin.functions import est_installe

# création de la classe objet
class Carte:
    def __init__(self, title, short_desc, icon, subjects):
        self.title = title
        self.short_desc = short_desc
        self.icon = icon
        self.subjects = subjects

class Page_Ressources:
    def __init__(self, title, url, packet_name, long_desc, icon, featured_image, illustrations, subjects, content_type, comments):
        self.title = title
        self.url = url
        self.packet_name = packet_name
        self.long_desc = long_desc
        self.icon = icon
        self.featured_image = featured_image
        self.illustrations = illustrations
        self.subjects = subjects
        self.content_type = content_type
        self.comments = comments

