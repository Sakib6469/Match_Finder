class Likes:
    DB = "match_finder1"
    def __init__(self,data):
        self.id = data['id']
        self.user_id_matcher = data['user_id_matcher']
        self.user_id_matchee = data['user_id_matchee']
        self.created_at = data['created_at']
