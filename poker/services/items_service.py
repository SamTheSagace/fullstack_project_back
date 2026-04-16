from typing import List, Optional

from poker.models import Item

class ItemService:
        @staticmethod
        def get_by_id(item_id: int) -> Item:
            try:
                return Item.objects.prefetch_related("votes").get(id=item_id)
            except Item.DoesNotExist:
                raise ValueError("Item not found")
            
        @staticmethod
        def get_by_session_id(session_id: int) -> List[Item]:
            items = Item.objects.filter(session_id=session_id).prefetch_related("votes")
            if not items.exists():
                raise ValueError('No items found')
            return list(items)
             
        @staticmethod
        def get_by_session_and_position(session_id: int, position: int) -> Item:
            try:
                return Item.objects.prefetch_related("votes").get(session_id = session_id, position = position)
            except Item.DoesNotExist:
                raise ValueError('Item not found')
            
        @staticmethod
        def create(
                title: str, 
                description: str, 
                session_id: int, 
                status: str, 
                created_by_roblox_user_id: int
            ) -> Item:
             session_items = Item.objects.filter(session_id=session_id)
             position = session_items.__len__() + 1
             item = Item.objects.create(
                title=title,
                description=description,
                session_id=session_id,
                position=position,
                status=status,
                created_by_roblox_user_id=created_by_roblox_user_id,
             )
             return item
        
        @staticmethod
        def update(
                item_id: int, 
                title: Optional[str] = None, 
                description: Optional[str] = None, 
                position: Optional[int] = None, 
                status: Optional[str] = None,
            ) -> Item:
                try:
                    item = Item.objects.get(id=item_id)
                    if title is not None:
                        item.title = title
                    if description is not None:
                        item.description = description
                    if position is not None:
                        item.position = position
                    if status is not None:
                        item.status = status
                    item.save()
                    return item
                except Item.DoesNotExist:
                    raise ValueError("Item not found")
                
        @staticmethod
        def delete(item_id: int, created_by_roblox_user_id: int) -> Item:
            try:
                item = Item.objects.get(id=item_id, created_by_roblox_user_id=created_by_roblox_user_id)
                if item.created_by_roblox_user_id != created_by_roblox_user_id:
                    raise ValueError("You do not have permission to delete this item")
                
                item.delete()
                return item
            except Item.DoesNotExist:
                raise ValueError("Item not found")
        
        
