from django.db import models


class ContentProposalModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    record = models.ForeignKey("RecordModel", on_delete=models.CASCADE, related_name="content_proposals")
    proposed_by_id = models.CharField(max_length=255)
    proposed_by_kind = models.CharField(max_length=32)
    markdown = models.TextField()
    status = models.CharField(max_length=32)
