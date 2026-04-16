from poker.models import Vote

class VotesService:
    @staticmethod
    def create(item_id: int, roblox_user_id: int, value: str) -> Vote:
        try:
            existingVote = Vote.objects.get(item_id = item_id, roblox_user_id = roblox_user_id)
            if existingVote:
                existingVote.value = value
                existingVote.save()
                return existingVote
            else:
                vote = Vote.objects.create(
                    item_id = item_id,
                    roblox_user_id = roblox_user_id,
                    value = value,
                )
                return vote
        except Vote.DoesNotExist:
            raise ValueError('Vote not found')
    
    @staticmethod
    def update(vote_id: int, value: str) -> Vote:
        try:
            vote = Vote.objects.get(id=vote_id)
            vote.value = value
            vote.save()
            return vote
        except Vote.DoesNotExist:
            raise ValueError('Vote not found')
        
    @staticmethod
    def delete(vote_id: int) -> Vote:
        try:
            vote = Vote.objects.get(id=vote_id)
            vote.delete()
            return vote
        except Vote.DoesNotExist:
            raise ValueError('Vote not found')
