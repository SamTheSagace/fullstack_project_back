from poker.models import Vote

class VotesService:
    @staticmethod
    def create(item_id: int, roblox_user_id: int, value: str):
        try:
            vote = Vote.objects.create(
                item_id = item_id,
                roblox_user_id = roblox_user_id,
                value = value,
            )
            return vote
        except Vote.DoesNotExist:
            raise ValueError('Vote not found')
    
    @staticmethod
    def update(vote_id: int, value: str):
        try:
            vote = Vote.objects.get(id=vote_id)
            vote.value = value
            vote.save()
        except Vote.DoesNotExist:
            raise ValueError('Vote not found')
        
    @staticmethod
    def delete(vote_id: int):
        try:
            vote = Vote.objects.get(id=vote_id)
            vote.delete()
        except Vote.DoesNotExist:
            raise ValueError('Vote not found')
