from django.test import TestCase
from unittest.mock import patch, MagicMock
from poker.models import Item
from poker.services.items_service import ItemsService


class ItemsServiceGetByIdTest(TestCase):

    @patch("poker.services.items_service.Item.objects.prefetch_related")
    def test_get_by_id_success(self, mock_prefetch):
        mock_item = MagicMock(spec=Item)
        mock_prefetch.return_value.get.return_value = mock_item

        result = ItemsService.get_by_id(item_id=1)

        mock_prefetch.assert_called_once_with("votes")
        mock_prefetch.return_value.get.assert_called_once_with(id=1)
        self.assertEqual(result, mock_item)

    @patch("poker.services.items_service.Item.objects.prefetch_related")
    def test_get_by_id_not_found(self, mock_prefetch):
        mock_prefetch.return_value.get.side_effect = Item.DoesNotExist

        with self.assertRaises(ValueError) as ctx:
            ItemsService.get_by_id(item_id=999)

        self.assertEqual(str(ctx.exception), "Item not found")


class ItemsServiceGetBySessionIdTest(TestCase):

    @patch("poker.services.items_service.Item.objects.filter")
    def test_get_by_session_id_success(self, mock_filter):
        mock_item = MagicMock(spec=Item)
        mock_qs = MagicMock()
        mock_qs.exists.return_value = True
        mock_qs.prefetch_related.return_value = mock_qs
        mock_qs.__iter__ = MagicMock(return_value=iter([mock_item]))
        mock_filter.return_value = mock_qs

        result = ItemsService.get_by_session_id(session_id=1)

        mock_filter.assert_called_once_with(session_id=1)
        self.assertIsInstance(result, list)

    @patch("poker.services.items_service.Item.objects.filter")
    def test_get_by_session_id_not_found(self, mock_filter):
        mock_qs = MagicMock()
        mock_qs.exists.return_value = False
        mock_qs.prefetch_related.return_value = mock_qs
        mock_filter.return_value = mock_qs

        with self.assertRaises(ValueError) as ctx:
            ItemsService.get_by_session_id(session_id=999)

        self.assertEqual(str(ctx.exception), "No items found")


class ItemsServiceGetBySessionAndPositionTest(TestCase):

    @patch("poker.services.items_service.Item.objects.prefetch_related")
    def test_get_by_session_and_position_success(self, mock_prefetch):
        mock_item = MagicMock(spec=Item)
        mock_prefetch.return_value.get.return_value = mock_item

        result = ItemsService.get_by_session_and_position(session_id=1, position=2)

        mock_prefetch.assert_called_once_with("votes")
        mock_prefetch.return_value.get.assert_called_once_with(session_id=1, position=2)
        self.assertEqual(result, mock_item)

    @patch("poker.services.items_service.Item.objects.prefetch_related")
    def test_get_by_session_and_position_not_found(self, mock_prefetch):
        mock_prefetch.return_value.get.side_effect = Item.DoesNotExist

        with self.assertRaises(ValueError) as ctx:
            ItemsService.get_by_session_and_position(session_id=999, position=99)

        self.assertEqual(str(ctx.exception), "Item not found")


class ItemsServiceCreateTest(TestCase):

    @patch("poker.services.items_service.Item.objects.create")
    @patch("poker.services.items_service.Item.objects.filter")
    def test_create_success(self, mock_filter, mock_create):
        mock_qs = MagicMock()
        mock_qs.__len__ = MagicMock(return_value=2)
        mock_filter.return_value = mock_qs

        mock_item = MagicMock(spec=Item)
        mock_create.return_value = mock_item

        result = ItemsService.create(
            title="Test item",
            description="A description",
            session_id=1,
            status="pending",
            created_by_roblox_user_id=123,
        )

        mock_filter.assert_called_once_with(session_id=1)
        mock_create.assert_called_once_with(
            title="Test item",
            description="A description",
            session_id=1,
            position=3,
            status="pending",
            created_by_roblox_user_id=123,
        )
        self.assertEqual(result, mock_item)


class ItemsServiceUpdateTest(TestCase):

    @patch("poker.services.items_service.Item.objects.get")
    def test_update_all_fields(self, mock_get):
        mock_item = MagicMock(spec=Item)
        mock_get.return_value = mock_item

        result = ItemsService.update(
            item_id=1,
            title="New title",
            description="New description",
            position=2,
            status="voting",
        )

        self.assertEqual(mock_item.title, "New title")
        self.assertEqual(mock_item.description, "New description")
        self.assertEqual(mock_item.position, 2)
        self.assertEqual(mock_item.status, "voting")
        mock_item.save.assert_called_once()
        self.assertEqual(result, mock_item)

    @patch("poker.services.items_service.Item.objects.get")
    def test_update_partial_fields(self, mock_get):
        mock_item = MagicMock(spec=Item)
        mock_get.return_value = mock_item

        ItemsService.update(item_id=1, title="Only title updated")

        self.assertEqual(mock_item.title, "Only title updated")
        mock_item.save.assert_called_once()

    @patch("poker.services.items_service.Item.objects.get")
    def test_update_not_found(self, mock_get):
        mock_get.side_effect = Item.DoesNotExist

        with self.assertRaises(ValueError) as ctx:
            ItemsService.update(item_id=999, title="Ghost")

        self.assertEqual(str(ctx.exception), "Item not found")


class ItemsServiceDeleteTest(TestCase):

    @patch("poker.services.items_service.Item.objects.get")
    def test_delete_success(self, mock_get):
        mock_item = MagicMock(spec=Item)
        mock_get.return_value = mock_item

        result = ItemsService.delete(item_id=1)

        mock_get.assert_called_once_with(id=1)
        mock_item.delete.assert_called_once()
        self.assertEqual(result, mock_item)

    @patch("poker.services.items_service.Item.objects.get")
    def test_delete_not_found(self, mock_get):
        mock_get.side_effect = Item.DoesNotExist

        with self.assertRaises(ValueError) as ctx:
            ItemsService.delete(item_id=999)

        self.assertEqual(str(ctx.exception), "Item not found")