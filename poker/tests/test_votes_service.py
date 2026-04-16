from django.test import TestCase
from unittest.mock import patch, MagicMock
from poker.models import Vote
from poker.services.votes_service import VotesService


class VotesServiceCreateTest(TestCase):

    @patch("poker.services.votes_service.Vote.objects.update_or_create")
    def test_create_new_vote(self, mock_update_or_create):
        mock_vote = MagicMock(spec=Vote)
        mock_update_or_create.return_value = (mock_vote, True)

        result = VotesService.create(item_id=1, roblox_user_id=123, value="5")

        mock_update_or_create.assert_called_once_with(
            item_id=1,
            roblox_user_id=123,
            defaults={"value": "5"},
        )
        self.assertEqual(result, mock_vote)

    @patch("poker.services.votes_service.Vote.objects.update_or_create")
    def test_update_existing_vote(self, mock_update_or_create):
        mock_vote = MagicMock(spec=Vote)
        mock_update_or_create.return_value = (mock_vote, False)

        result = VotesService.create(item_id=1, roblox_user_id=123, value="8")

        mock_update_or_create.assert_called_once_with(
            item_id=1,
            roblox_user_id=123,
            defaults={"value": "8"},
        )
        self.assertEqual(result, mock_vote)


class VotesServiceUpdateTest(TestCase):

    @patch("poker.services.votes_service.Vote.objects.get")
    def test_update_vote_success(self, mock_get):
        mock_vote = MagicMock(spec=Vote)
        mock_get.return_value = mock_vote

        result = VotesService.update(vote_id=1, value="13")

        mock_get.assert_called_once_with(id=1)
        self.assertEqual(mock_vote.value, "13")
        mock_vote.save.assert_called_once()
        self.assertEqual(result, mock_vote)

    @patch("poker.services.votes_service.Vote.objects.get")
    def test_update_vote_not_found(self, mock_get):
        mock_get.side_effect = Vote.DoesNotExist

        with self.assertRaises(ValueError) as ctx:
            VotesService.update(vote_id=999, value="13")

        self.assertEqual(str(ctx.exception), "Vote not found")


class VotesServiceDeleteTest(TestCase):

    @patch("poker.services.votes_service.Vote.objects.get")
    def test_delete_vote_success(self, mock_get):
        mock_vote = MagicMock(spec=Vote)
        mock_get.return_value = mock_vote

        result = VotesService.delete(vote_id=1)

        mock_get.assert_called_once_with(id=1)
        mock_vote.delete.assert_called_once()
        self.assertEqual(result, mock_vote)

    @patch("poker.services.votes_service.Vote.objects.get")
    def test_delete_vote_not_found(self, mock_get):
        mock_get.side_effect = Vote.DoesNotExist

        with self.assertRaises(ValueError) as ctx:
            VotesService.delete(vote_id=999)

        self.assertEqual(str(ctx.exception), "Vote not found")