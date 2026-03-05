from typing import Optional

from poker.models import Item

class ItemService:
        @staticmethod
        def get_by_id(item_id: int) -> Item:
            try:
                return Item.objects.get(id=item_id)
            except Item.DoesNotExist:
                raise ValueError("Item not found")
            
        @staticmethod
        def create(title: str, description: str, session_id: int, position: int, status: str, created_by_roblox_user_id: int):
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
                print("test", description)
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
        
        
