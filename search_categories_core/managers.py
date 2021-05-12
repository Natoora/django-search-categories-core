from django.db import models, transaction
from django.db.models import F, Max


class SearchCategoryManager(models.Manager):
    """
    SearchCategory model manager.
    """

    def create(self, **kwargs):
        """
        When creating a SearchCategory
        Populate the hierarchy field with the max hierarchy + 1.
        """
        instance = self.model(**kwargs)
        with transaction.atomic():
            hierarchy_max = self.aggregate(Max('hierarchy')).get('hierarchy__max') or 0
            instance.hierarchy = hierarchy_max + 1
            instance.save()
            return instance

    def move(self, obj, old_pos, new_pos, save=True):
        """Insert at position in the hierarchy and adjust the
        rest of the search categories' hierarchies so they're  in sequence.

        For example:
          apples = SearchCategory.objects.get(name="apples")
          SearchCategories.objects.move(apples, 5)

        :param obj: SearchCategory to move.
        :param old_pos: Hierarchy moving from.
        :param new_pos: Hierarchy number to move to.
        :param save: Optionally disable the save, so this can be called in the pre save.
        """
        qs = self.get_queryset()
        with transaction.atomic():
            if old_pos > int(new_pos):
                qs.filter(hierarchy__lt=old_pos, hierarchy__gte=new_pos).exclude(pk=obj.pk).update(
                    hierarchy=F('hierarchy') + 1
                )
            elif old_pos < int(new_pos):
                qs.filter(hierarchy__lte=new_pos, hierarchy__gt=old_pos).exclude(pk=obj.pk).update(
                    hierarchy=F('hierarchy') - 1
                )
            obj.hierarchy = new_pos
            if save:
                obj.save()
